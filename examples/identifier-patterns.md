# Identifier and Manifest Patterns

This file records known identifier conventions used by the integration. Examples are intended to document patterns, not to define every possible digital-resource structure.

## Alma MMS ID

The Alma MMS ID is used as the principal Library resource identifier in the manifest naming convention.

Example:

```text
99682013504896
```

## Standard Manifest

```text
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}.json
```

Example:

```text
https://libraryimage.nga.gov/manifest/mms/99682013504896.json
```

## Multi-Volume Manifest

```text
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}-1.json
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}-2.json
```

The number of manifests depends on the intended digital representation of the bibliographic resource.


## IIIF Image Services

With the eDAM support, image/service references inside the manifest structure toward UUID-based Gallery API resources under:

```text
https://api.nga.gov/...
```
Example:
https://api.nga.gov/iiif/d29a5c29-7d2a-417c-aef1-64c710a6e184/full/full/0/default.jpg
```text

```
