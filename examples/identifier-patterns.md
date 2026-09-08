# Identifier and Manifest Patterns

This file records known identifier conventions used by the integration.

## Alma MMS ID

The Alma MMS ID is used as the principal Library resource identifier in the manifest naming convention.

Example:

```text
99682013504896
```

## Primo Display

```text
https://library.nga.gov/permalink/01NGA_INST/pdr574/alma99682013504896
```

## IIIF Manifest

With the metadata retrieval via Alma API and NetX API, manifest in json format is created using IIIF-Prezi library, check main-netxjson-to-manifest.py in sourcecode.

```text
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}.json
```

Example:

```text
https://libraryimage.nga.gov/manifest/mms/99682013504896.json
```


## IIIF Image

Image/service references inside the manifest is delivered via Gallery developed UUID-based API service under:

```text
https://api.nga.gov/...
```
Example:
https://api.nga.gov/iiif/d29a5c29-7d2a-417c-aef1-64c710a6e184/full/full/0/default.jpg
```text

```
