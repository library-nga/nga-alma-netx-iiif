# NGA Library Alma–NetX–IIIF Integration

Technical documentation for the National Gallery of Art Library integration connecting **Ex Libris Alma**, **Primo VE**, **NetX/eDAM**, and **IIIF services**.

## Purpose

This project enables the Library to manage descriptive and discovery relationships in Alma/Primo while keeping master digital assets in the Gallery's eDAM/NetX environment. IIIF provides the standards-based delivery layer between the digital asset repository and the Library discovery interface.

The implementation was designed around a clear separation of responsibilities:

- **Alma** — bibliographic metadata, collections, digital representations, and remote digital repository relationships.
- **NetX/eDAM** — authoritative storage and management of digital image assets and associated metadata.
- **IIIF** — image delivery, manifests, canvases, and interoperable presentation services.
- **Primo VE** — public discovery and embedded IIIF viewing experience.

## High-Level Architecture

```text
                         Primo VE
                    Discovery / Viewer
                           |
                  Custom IIIF Viewer
                           |
                           v
                    IIIF Manifest
             libraryimage.nga.gov/manifest
                           |
             +-------------+-------------+
             |                           |
             v                           v
           Alma                       NetX/eDAM
 Remote Digital Repository         Asset repository
 Digital Representation            Metadata + images
 Collection hierarchy              Web publishing
             |                           |
             |                     custom NetX API
             |                           |
             |                           v
             |                     IIIF Image API
             |                     api.nga.gov/UUID
             |                           |
             +---------------------------+
```

See [System Architecture](docs/architecture.md) for details.

## Core Workflow

```text
Digitization
    ↓
Image + metadata loaded to NetX/eDAM
    ↓
Web Publish
    ↓
IIIF Image API available
    ↓
Manifest generated / regenerated
    ↓
Alma Remote Digital Representation
    ↓
Primo "View Online"
    ↓
Embedded IIIF viewer
```

See [Digital Publishing Workflow](docs/digital-publishing-workflow.md).

## Repository Documentation

- [System Architecture](docs/architecture.md)
- [Implementation History](docs/implementation-history.md)
- [Digital Publishing Workflow](docs/digital-publishing-workflow.md)
- [Alma Configuration](docs/alma-configuration.md)
- [Primo IIIF Viewer](docs/primo-iiif-viewer.md)
- [Troubleshooting and Operations](docs/troubleshooting.md)
- [Identifier and Manifest Patterns](examples/identifier-patterns.md)

## Key Design Decisions

1. **Do not duplicate master images in Alma.** NetX/eDAM remains the authoritative digital asset repository.
2. **Use Alma Remote Digital Repository.** Alma manages the digital representation and discovery relationship while content remains remote.
3. **Use IIIF as the interoperability layer.** Primo and other applications consume manifests and image services rather than proprietary image delivery interfaces.
4. **Preserve public manifest URLs.** During the 2021 migration to eDAM, existing manifest URLs were retained while the image identifiers and IIIF services inside the manifests moved to UUID-based delivery.
5. **Keep presentation independent from storage.** Primo customization can change, including migration to Primo NDE, without fundamentally changing the Alma–NetX–IIIF architecture.

## Historical Context

The Library originally used a local image server that handled digital asset storage, IIIF APIs/services, viewer delivery, and manifest generation. In 2021 the Library began moving digital assets into the Gallery's NetX/eDAM environment.

The target date for the new eDAM workflow was **June 1, 2021**. The workflow moved newly digitized images and metadata into eDAM, web-published them, and delivered them through UUID-based IIIF services. Existing digital titles were migrated in batches.

By 2023, the integration was documented as having two principal implementation areas:

1. Alma configuration using a Remote Digital Repository and digital representations so Primo could expose **View Online**.
2. Primo customization using HTML/JavaScript/CSS and AngularJS to embed an IIIF viewer and manifest in the full record display.

## Current Evolution

The underlying architecture remains valid for Primo NDE. The primary change is at the presentation layer: the legacy Primo customization package must be rewritten for the NDE framework to continue embedding the IIIF viewer.

## License

See [LICENSE](LICENSE).