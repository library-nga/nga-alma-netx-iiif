# System Architecture

## Overview

The NGA Library digital-resource architecture separates **library resource management**, **digital asset management**, **standards-based image delivery**, and **public discovery** across specialized systems.

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

## System Responsibilities

### Alma

Alma is the Library's resource-management system and manages:

- Bibliographic records.
- Digital representations.
- Remote Digital Repository configuration.
- Discovery relationships exposed to Primo.

Alma does **not** need to store the master image files in this architecture.

### NetX / eDAM

NetX/eDAM is the authoritative digital asset environment and manages:

- Master digital images.
- Asset metadata.
- Asset identifiers.
- Web-publishing status.
- Delivery of published assets to downstream services.

For the Alma integration, NetX is treated as an external/other remote repository rather than an Alma-managed digital repository.

### IIIF Services

IIIF provides the interoperability layer.

The architecture uses IIIF concepts including:

- Image API services.
- Presentation manifests.
- Canvases.
- Stable manifest URLs.
- UUID-based image identifiers/services.

This allows the same digital resources to be reused by Primo, Mirador, Universal Viewer, research projects, and other IIIF-aware applications.

### Primo VE

Primo VE is the public discovery layer.

The Library customized Primo so that a resource with an Alma digital representation can expose **View Online** and display the associated IIIF resource through an embedded viewer.

## Alma Remote Digital Repository Pattern

The integration uses an Alma **Remote Digital Repository** because the images live outside Alma.

Conceptually:

```text
Alma bibliographic record
        |
        v
Alma collection
        |
        v
Digital representation
        |
        v
Remote Digital Repository
        |
        v
NetX/eDAM + IIIF services
```

NetX was not used as a predefined Ex Libris repository type. The repository type was configured as **Other**, with custom integration logic calling the NetX API.

## Identifier Strategy

Stable identifiers are essential because the same resources may be referenced from Alma, Primo, Gallery websites, external research projects, Getty-related projects, and other consumers.

Key identifiers include:

| Layer | Identifier example/purpose |
| --- | --- |
| Alma | MMS ID for the bibliographic resource |
| NetX/eDAM | Asset identifier / UUID |
| IIIF Manifest | Stable public manifest URL |
| IIIF Canvas | UUID-based canvas identifier |
| IIIF Image API | UUID-based image service |

A major 2021 design decision was to preserve the **existing manifest URL** while changing the image and service identifiers contained within the manifest. This minimized downstream disruption for external consumers that had already stored NGA manifest URLs.

## Manifest Pattern

A standard manifest follows the conceptual pattern:

```text
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}.json
```

Multi-volume resources may use:

```text
{MMS_ID}-1.json
{MMS_ID}-2.json
{MMS_ID}-3.json
```

The exact representation depends on how the bibliographic resource and volumes are modeled.

## Architectural Principle

The core principle is **separation of responsibility**:

```text
Alma       = library metadata and digital-resource relationships
NetX/eDAM  = digital asset management
IIIF       = interoperable image/presentation delivery
Primo      = discovery and user experience
```

This separation allows any one layer to evolve without requiring the entire architecture to be replaced. Primo NDE, for example, requires a new viewer customization but does not fundamentally change the repository and IIIF integration.
