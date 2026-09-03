# Primo VE IIIF Viewer

This folder contains the NGA Library Primo VE customization used to display digitized Library resources through the IIIF viewer.

## Viewer Logic

The customization reads two values from the Primo PNX record:

- `control.sourcerecordid` — used as the Alma source/MMS record identifier when constructing the IIIF manifest URL.
- `display.lds01` — local display field used as a switch; when its value is `viewer`, the custom IIIF viewer is displayed.

The manifest follows this pattern:

```text
https://libraryimage.nga.gov/manifest/mms/{sourceRecordId}.json
```

The manifest is passed to the NGA Library Universal Viewer endpoint:

```text
https://libraryimage.nga.gov/uv/?manifest={manifestUrl}
```

## Flow

```text
Primo PNX record
      |
      +-- control.sourcerecordid
      |          |
      |          v
      |    IIIF Manifest URL
      |
      +-- display.lds01
                 |
                 +-- viewer
                       |
                       v
               Custom IIIF Viewer
```

## Source

`image-viewer.js` contains the AngularJS controller used by the Primo VE customization package.

The Primo NDE implementation uses a different front-end framework and should be maintained separately from this Primo VE implementation.
