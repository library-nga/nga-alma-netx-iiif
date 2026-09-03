#!/usr/bin/env python3
"""Generate IIIF manifests from NetX JSON exports and update Alma.

Required environment variables:
    ALMA_API_KEY
    ALMA_SET_ID
    ALMA_COLLECTION_ID

Optional environment variables:
    ALMA_API_BASE
    ALMA_LIBRARY
    ALMA_REMOTE_REPOSITORY
    IIIF_PREZI_ROOT
    MANIFEST_OUTPUT_DIR
    LOG_DIR
"""

import json
import logging
import os
import re
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from iiif_prezi.factory import ManifestFactory
from pymarc import marcxml


TODAY = date.today().isoformat()

ALMA_API_KEY = os.environ.get("ALMA_API_KEY")
ALMA_API_BASE = os.environ.get(
    "ALMA_API_BASE",
    "https://api-na.hosted.exlibrisgroup.com/almaws/v1",
).rstrip("/")

ALMA_SET_ID = os.environ.get("ALMA_SET_ID", "")
ALMA_COLLECTION_ID = os.environ.get("ALMA_COLLECTION_ID", "")
ALMA_LIBRARY = os.environ.get("ALMA_LIBRARY", "MAIN")
ALMA_REMOTE_REPOSITORY = os.environ.get("ALMA_REMOTE_REPOSITORY", "NGA")

IIIF_PREZI_ROOT = Path(os.environ.get("IIIF_PREZI_ROOT", "/opt/iiif-prezi"))
NETX_JSON_DIR = IIIF_PREZI_ROOT / "files" / "main-netx-json" / TODAY
MANIFEST_OUTPUT_DIR = Path(
    os.environ.get("MANIFEST_OUTPUT_DIR", "/var/www/html/manifest/mms")
)
LOG_DIR = Path(
    os.environ.get("LOG_DIR", "/var/www/html/doc/iiif-logs/library")
)

MANIFEST_BASE_URI = "https://libraryimage.nga.gov/manifest/mms/"
IMAGE_BASE_URI = "https://api.nga.gov/iiif/"
CATALOG_BASE_URL = "https://library.nga.gov/discovery/fulldisplay"


def configure_logging() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"main-{TODAY}.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    return log_file


def require_config() -> None:
    missing = []

    if not ALMA_API_KEY:
        missing.append("ALMA_API_KEY")
    if not ALMA_SET_ID:
        missing.append("ALMA_SET_ID")
    if not ALMA_COLLECTION_ID:
        missing.append("ALMA_COLLECTION_ID")

    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): " + ", ".join(missing)
        )


def alma_url(path: str, **query) -> str:
    params = {"apikey": ALMA_API_KEY, **query}
    return f"{ALMA_API_BASE}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"


def post_json(url: str, body: dict) -> None:
    payload = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        response.read()


def update_alma_set(mms_id: str, operation: str) -> None:
    body = {
        "members": {
            "total_record_count": "",
            "member": [{"id": mms_id}],
        }
    }

    post_json(
        alma_url(f"conf/sets/{ALMA_SET_ID}", op=operation),
        body,
    )


def replace_alma_set(mms_id: str) -> None:
    update_alma_set(mms_id, "replace_members")


def add_to_alma_set(mms_id: str) -> None:
    update_alma_set(mms_id, "add_members")


def create_alma_representation(
    mms_id: str,
    thumbnail_uuid: str,
    public_note: str,
) -> None:
    collection_body = {"mms_id": mms_id}

    try:
        post_json(
            alma_url(f"bibs/collections/{ALMA_COLLECTION_ID}/bibs"),
            collection_body,
        )
    except Exception as exc:
        logging.error(
            "Alma: failed to add MMS ID %s to collection: %s",
            mms_id,
            exc,
        )

    representation_body = {
        "is_remote": "true",
        "library": {"value": ALMA_LIBRARY},
        "public_note": public_note,
        "usage_type": {"value": "PRESERVATION_MASTER"},
        "active": {"value": "true"},
        "access_rights_policy_id": {"value": ""},
        "repository": {"value": ALMA_REMOTE_REPOSITORY},
        "originating_record_id": mms_id,
        "linking_parameter_1": thumbnail_uuid,
    }

    try:
        post_json(
            alma_url(
                f"bibs/{mms_id}/representations",
                generate_label="false",
            ),
            representation_body,
        )
    except Exception as exc:
        logging.error(
            "Alma: failed to create digital representation for MMS ID %s: %s",
            mms_id,
            exc,
        )


def field_as_text(field) -> str:
    """Preserve the legacy script's MARC display-string cleanup behavior."""
    if field is None:
        return ""

    text = str(field)
    parts = text.split("  ", 1)
    if len(parts) < 2:
        return text.strip()

    text = parts[1][2:]
    text = re.sub(r"\$\S", " ", text)
    return text.strip()


def get_bib_metadata(mms_id: str) -> dict:
    try:
        with urllib.request.urlopen(
            alma_url(f"bibs/{mms_id}", view="full", expand="None"),
            timeout=60,
        ) as response:
            records = marcxml.parse_xml_to_array(response)
    except Exception as exc:
        raise RuntimeError(
            f"Alma bib API call failed for MMS ID {mms_id}"
        ) from exc

    if not records:
        raise RuntimeError(f"No Alma bib record returned for MMS ID {mms_id}")

    record = records[0]

    title = ""
    author = ""
    publisher = ""
    description = ""
    note = ""
    dcl = ""
    cicognara = ""
    viewing_hint = ""
    volume_name = ""
    volume_count = 0

    for field in record.get_fields("024"):
        if field.indicator1 == "8" and field["a"]:
            dcl += f"{field['a']}; "

    for field in record.get_fields("510"):
        if field.indicator1 == "4" and field["a"] and field["c"]:
            cicognara += f"{field['a']}{field['c']}; "

    field_240 = record["240"]
    field_245 = record["245"]

    if field_240:
        title = field_240["a"] or ""
        if field_240["l"]:
            title += f" {field_240['l']}"
    elif field_245:
        title = field_as_text(field_245)

    field_100 = record["100"]
    if field_100:
        author = field_as_text(field_100)
    else:
        authors = []
        for field in record.get_fields("700"):
            text = field_as_text(field)
            if text:
                authors.append(text)
        author = " ".join(authors)

    if record["260"]:
        publisher = field_as_text(record["260"])

    if record["300"]:
        description = field_as_text(record["300"])

    for field in record.get_fields("590"):
        if field["a"]:
            note += field["a"]

    if record["956"] and record["956"]["x"]:
        viewing_hint = record["956"]["x"]

    for field in record.get_fields("856"):
        value = field["3"]
        if not value or "." not in value:
            continue

        name, number = value.split(".", 1)
        try:
            number = int(number)
        except ValueError:
            logging.warning(
                "Ignoring non-numeric 856 $3 volume value for MMS ID %s: %s",
                mms_id,
                value,
            )
            continue

        volume_name = name
        volume_count = max(volume_count, number)

    return {
        "title": title,
        "author": author,
        "dcl": dcl,
        "cicognara": cicognara,
        "publisher": publisher,
        "description": description,
        "note": note,
        "viewing_hint": viewing_hint,
        "volume_count": volume_count,
        "volume_name": volume_name,
    }


def attribute_value(attributes: dict, name: str, default: str = "") -> str:
    values = attributes.get(name) or []
    return str(values[0]) if values else default


def build_factory() -> ManifestFactory:
    factory = ManifestFactory()
    factory.set_base_prezi_uri(MANIFEST_BASE_URI)
    factory.set_base_image_uri(IMAGE_BASE_URI)
    factory.set_iiif_image_info(2.0, 2)
    return factory


def write_manifest(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")
    path.chmod(0o664)


def build_catalog_link(mms_id: str) -> str:
    return (
        f"<a href='{CATALOG_BASE_URL}"
        f"?docid=alma{mms_id}&vid=01NGA_INST:NGA'>"
        "View in NGA Library Catalog</a>"
    )


def create_manifest(json_path: Path, factory: ManifestFactory) -> dict:
    with json_path.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    result = data.get("result", {})
    assets = result.get("results", [])

    if not assets:
        raise ValueError(f"No NetX assets found in {json_path.name}")

    bib_volume_id = attribute_value(
        assets[0].get("attributes", {}),
        "PL Bib ID",
    )
    if not bib_volume_id:
        raise ValueError(f"Missing PL Bib ID in {json_path.name}")

    mms_id = bib_volume_id.split("-", 1)[0]
    metadata = get_bib_metadata(mms_id)

    first_attributes = assets[0].get("attributes", {})
    credit = attribute_value(first_attributes, "Credit")
    rights = attribute_value(first_attributes, "Asset Rights")
    digitization_date = attribute_value(
        first_attributes,
        "Image Capture Date",
    )

    manifest = factory.manifest(
        ident=bib_volume_id,
        label=metadata["title"],
    )

    manifest.set_metadata(
        {
            "Title": metadata["title"],
            "Author": metadata["author"],
            "Imprint": metadata["publisher"],
        }
    )
    manifest.description = metadata["description"]
    manifest.set_metadata(
        {"Bibliographic Information": build_catalog_link(mms_id)}
    )

    if metadata["cicognara"]:
        manifest.set_metadata({"Local Identifier": metadata["cicognara"]})
    if metadata["dcl"]:
        manifest.set_metadata({"Local Identifier": metadata["dcl"]})
    if metadata["note"]:
        manifest.set_metadata({"Notes": metadata["note"]})
    if credit:
        manifest.set_metadata({"Credit line": credit})
    if rights:
        manifest.set_metadata({"Copyright": rights})
    if digitization_date:
        manifest.set_metadata({"Digitization date": digitization_date})

    viewing_hint = metadata["viewing_hint"]
    if "paged" in viewing_hint:
        manifest.viewingHint = "paged"
    if "right-to-left" in viewing_hint:
        manifest.viewingDirection = "right-to-left"

    sequence = manifest.sequence()
    thumbnail_uuid = ""
    public_note = ""

    for asset in assets:
        image_height = asset.get("file", {}).get("height")
        image_width = asset.get("file", {}).get("width")
        attributes = asset.get("attributes", {})

        image_description = "".join(
            attributes.get("Image View Description") or []
        )
        image_uuid = "".join(
            attributes.get("Web-Enterprise UUID") or []
        )
        index = "".join(attributes.get("PL Index") or [])
        asset_rights = "".join(attributes.get("Asset Rights") or [])

        if not image_uuid:
            logging.error(
                "MMS ID %s: missing Web-Enterprise UUID",
                mms_id,
            )
            continue

        if not image_description:
            logging.error(
                "MMS ID %s, image %s: missing Image View Description",
                mms_id,
                image_uuid,
            )
            image_description = "n/a"

        if asset_rights != "Public Domain":
            public_note = "High-resolution image only available at NGA on-site."

        if index.lower() == "thumb":
            thumbnail_uuid = image_uuid
        elif index == "TITLE PAGE" and not thumbnail_uuid:
            thumbnail_uuid = image_uuid

        try:
            canvas = sequence.canvas(
                ident=image_uuid,
                label=image_description,
            )
            canvas.set_hw(image_height, image_width)
            canvas.set_metadata({"View": image_description})
        except Exception as exc:
            logging.error(
                "MMS ID %s, image %s: canvas creation failed: %s",
                mms_id,
                image_uuid,
                exc,
            )
            continue

        if index and index.lower() != "thumb":
            try:
                manifest_range = manifest.range(
                    ident=index,
                    label=index,
                )
                manifest_range.add_canvas(canvas)
            except Exception:
                logging.error(
                    "MMS ID %s, image %s: duplicate/invalid index value: %s",
                    mms_id,
                    image_uuid,
                    index,
                )

        annotation = canvas.annotation(ident=image_uuid)
        image = annotation.image(ident=image_uuid, iiif=True)
        image.set_hw(image_height, image_width)

    if public_note:
        manifest.attribution = public_note

    output_path = MANIFEST_OUTPUT_DIR / f"{bib_volume_id}.json"
    write_manifest(output_path, manifest.toString(compact=False))

    logging.info("Manifest created: %s", bib_volume_id)

    create_alma_representation(
        mms_id,
        thumbnail_uuid,
        public_note,
    )

    return {
        "mms_id": mms_id,
        "bib_volume_id": bib_volume_id,
        "volume_count": metadata["volume_count"],
        "volume_name": metadata["volume_name"],
    }


def create_collection_manifest(
    factory: ManifestFactory,
    mms_id: str,
    volume_count: int,
    volume_name: str,
) -> None:
    if volume_count <= 0:
        return

    volume_numbers = []

    for json_path in NETX_JSON_DIR.iterdir():
        if not json_path.is_file():
            continue

        stem = json_path.stem
        prefix = f"netx-{mms_id}-"
        if not stem.startswith(prefix):
            continue

        volume_text = stem[len(prefix):]
        try:
            volume_numbers.append(int(volume_text))
        except ValueError:
            continue

    if not volume_numbers:
        return

    volume_numbers.sort()

    collection = factory.collection(ident="top", label="Collection")

    for volume_number in volume_numbers:
        label = (
            f"{volume_name}.{volume_number}"
            if volume_name
            else f"Volume {volume_number}"
        )
        volume_manifest = factory.manifest(
            ident=f"{mms_id}-{volume_number}",
            label=label,
        )
        collection.add_manifest(volume_manifest)

    write_manifest(
        MANIFEST_OUTPUT_DIR / f"{mms_id}.json",
        collection.toString(compact=False),
    )
    logging.info("Collection-level manifest created: %s", mms_id)


def main() -> None:
    log_file = configure_logging()
    require_config()

    if not NETX_JSON_DIR.is_dir():
        logging.error("NetX JSON directory not found: %s", NETX_JSON_DIR)
        raise SystemExit(1)

    factory = build_factory()
    processed_bibs = 0

    for json_path in sorted(NETX_JSON_DIR.iterdir()):
        if not json_path.is_file() or json_path.suffix.lower() != ".json":
            continue

        try:
            result = create_manifest(json_path, factory)
        except Exception:
            logging.exception("Failed processing %s", json_path.name)
            continue

        mms_id = result["mms_id"]

        if (
            result["volume_count"] > 0
            and result["bib_volume_id"]
            == f"{mms_id}-{result['volume_count']}"
        ):
            create_collection_manifest(
                factory,
                mms_id,
                result["volume_count"],
                result["volume_name"],
            )

        try:
            if processed_bibs == 0:
                replace_alma_set(mms_id)
            else:
                add_to_alma_set(mms_id)
        except Exception:
            logging.exception("Failed updating Alma set for MMS ID %s", mms_id)

        processed_bibs += 1

    try:
        log_file.chmod(0o644)
    except OSError:
        logging.warning("Unable to update log-file permissions.")

    logging.info("Processing complete. %d record(s) processed.", processed_bibs)


if __name__ == "__main__":
    main()
