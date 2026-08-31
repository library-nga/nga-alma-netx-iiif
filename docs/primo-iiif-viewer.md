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
Local customization package
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

## NDE Development Goals

The new component should:

1. Detect when a Primo record has the Library's remote IIIF digital representation.
2. Resolve the correct IIIF manifest.
3. Embed the selected IIIF viewer within the appropriate NDE extension point.
4. Handle single- and multi-volume resources.
5. Fail gracefully if a manifest or image service is unavailable.
6. Avoid embedding repository-specific assumptions that belong in the manifest/integration layer.
7. Meet accessibility and responsive-design requirements.

## Troubleshooting Viewer Problems

Before debugging the Primo customization, test the resource outside Primo:

1. Does the IIIF Image API return the image?
2. Does the IIIF manifest load as valid JSON?
3. Does the manifest open directly in a standard IIIF viewer?
4. Does Alma expose the expected digital representation?
5. Only then inspect the Primo/NDE customization.

This isolates front-end problems from repository or manifest-generation failures.