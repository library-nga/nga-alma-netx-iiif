# Primo IIIF Viewer Integration

## Purpose

Primo provides the patron-facing presentation layer for the Library's remotely managed digital resources.

## Legacy Primo VE Implementation

The original Primo VE implementation embeds an existing IIIF viewer within the Primo full-record experience.

Historical implementation notes describe the customization as using:

- AngularJS.
- JavaScript.
- HTML.
- CSS.
- An IIIF viewer such as Mirador or Universal Viewer.
- The IIIF manifest associated with the Alma resource.

Conceptually:

```text
Primo full record
      ↓
View Online section
      ↓
Read/construct IIIF manifest reference
      ↓
Embedded IIIF viewer
      ↓
Manifest + IIIF Image API
```

## Separation from Repository Logic

The viewer does not need to manage or store the images.

It consumes the IIIF Presentation manifest, which in turn references the image services delivered from the Gallery infrastructure.

This means viewer replacement should not require a redesign of the DAM integration.

## Primo NDE

Primo NDE uses a different customization framework from the legacy Primo VE AngularJS customization package.

The Library therefore needs to **rewrite the IIIF viewer customization for NDE**.

The underlying flow remains:

```text
Alma record
    ↓
Digital representation
    ↓
IIIF manifest
    ↓
NDE custom component
    ↓
IIIF viewer
```
