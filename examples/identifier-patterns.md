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

## Migration-Era Manifest

During the 2021 eDAM transition, temporary manifests could use:

```text
{MMS_ID}-edam.json
```

The production workflow removed the `-edam` suffix and retained the stable MMS-based manifest URL.

## Canvas IDs

The older system could derive canvas identifiers from PTIF/file-system paths.

The eDAM workflow migrated canvases toward UUID-based identifiers, for example conceptually:

```text
https://libraryimage.nga.gov/manifest/mms/canvas/{UUID}.json
```

Human-readable labels such as `leaf 1 recto` remain separate from the machine identifier.

## IIIF Image Services

With the eDAM migration, image/service references inside the manifest moved away from the old `libraryimage.nga.gov/.../ptif/...` structure toward UUID-based Gallery API resources under:

```text
https://api.nga.gov/...
```

## Persistence Rule

Where possible:

- Preserve public manifest URLs.
- Treat canvas and image-service identifiers as persistent machine identifiers.
- Do not build integrations from display labels or filenames.
- Document intentional identifier migrations because downstream IIIF consumers may store canvas IDs as well as manifest URLs.