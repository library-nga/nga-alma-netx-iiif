#!/usr/bin/env python3

import logging
import subprocess
import sys
from datetime import date
from pathlib import Path


BASE_DIR = Path("/opt/iiif-prezi")
FILES_DIR = BASE_DIR / "files"
LOG_DIR = BASE_DIR / "logs"
TODAY = date.today().isoformat()


def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIR / f"auto-process-{TODAY}.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def run_script(script_name: str, step_name: str) -> bool:
    """Run a Python script and log success or failure."""
    try:
        subprocess.run(
            [sys.executable, script_name],
            cwd=BASE_DIR,
            check=True,
        )
        logging.info("%s completed successfully.", step_name)
        return True
    except subprocess.CalledProcessError as exc:
        logging.error(
            "%s failed with exit code %s.",
            step_name,
            exc.returncode,
        )
    except Exception:
        logging.exception("%s failed with an unexpected error.", step_name)

    return False


def process_collection(prefix: str, step_start: int) -> None:
    """Process one Alma output collection when today's MARC file exists."""
    marc_file = FILES_DIR / f"{prefix}-{TODAY}.mrc"

    if not marc_file.is_file():
        logging.info("No %s MARC file found: %s", prefix, marc_file)
        return

    logging.info("Found %s MARC file: %s", prefix, marc_file)

    run_script(
        f"{prefix}-netx-json.py",
        f"Step {step_start} - {prefix.title()}: Retrieve NetX attribute metadata",
    )

    run_script(
        f"{prefix}-netxjson-to-manifest.py",
        f"Step {step_start + 1} - {prefix.title()}: Generate IIIF manifest",
    )

    run_script(
        f"{prefix}-alma-api-post-job-957.py",
        f"Step {step_start + 2} - {prefix.title()}: Update Alma 957 via API",
    )


def main() -> None:
    configure_logging()
    logging.info("main-process.py triggered by crontab")

    run_script(
        "get-file-from-sftp.py",
        "Step 1 - Retrieve Alma output file from SFTP",
    )

    process_collection("image", step_start=2)
    process_collection("main", step_start=5)

    logging.info("main-process.py completed")


if __name__ == "__main__":
    main()
