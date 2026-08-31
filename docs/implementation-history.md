# Implementation History

## Background

The NGA Library's IIIF integration predates the move to NetX/eDAM.

The earlier architecture used a local Library image server that supported several functions:

- Digital asset storage.
- IIIF Image API/services.
- IIIF viewer delivery.
- Integrated IIIF manifest generation.
- Delivery of digital content into the Library discovery experience.

The Library documented the earlier Alma/Primo and IIIF implementation in a *Computers in Libraries* article published in December 2020. The implementation included Primo customization for embedding an IIIF viewer.

## 2021: Migration to NetX/eDAM

In 2021 the Library began moving digital assets from the local image repository into the Gallery's NetX/eDAM environment.

The planned production date for the new workflow was **June 1, 2021**.

The target workflow was:

```text
New digitization
    ↓
Images + metadata loaded into eDAM
    ↓
Web Publish
    ↓
UUID-based IIIF delivery
    ↓
New/rebuilt IIIF manifest
    ↓
Library discovery
```

At the same time, more than 1,000 existing digital titles were expected to migrate in batches.

## Persistent Manifest Strategy

The Library had already distributed IIIF manifest URLs to external partners and projects. Because of those dependencies, the migration was designed to keep the public manifest links stable.

The significant change happened **inside the manifest**:

### Earlier IIIF image API service pattern

```text
libraryimage.nga.gov/.../ptif/...
```

### New eDAM-based pattern for IIIF Image API service

```text
api.nga.gov/{UUID}/...
```

The public manifest URL could therefore remain stable while its canvases and image services were updated to use eDAM-backed UUID resources.

## Manifest Naming

During the migration, the Library standardized manifest naming around Alma MMS IDs.

Example:

```text
https://libraryimage.nga.gov/manifest/mms/99682013504896.json
```
For multi-volume titles, individual manifests may be generated:

```text
99682093504896-1.json
99682093504896-2.json
99682093504896-3.json
```

Some multipart resources may instead remain represented by one manifest depending on the cataloging and digital-object structure.

## Alma Integration

By 2023, the Library described the Alma/NetX implementation as having two major components.

### 1. Alma digital inventory

To make Primo display **View Online**, the Alma bibliographic resource must have appropriate digital inventory.

The Library uses:

- Alma Collections.
- Digital representations.
- A Remote Digital Repository.

Because NetX was not one of the predefined DAM types used by the Library, the repository was configured as **Other** and custom code/scripts were used to communicate with the NetX API.

### 2. Primo presentation

Primo's presentation layer was customized to embed an IIIF viewer using the IIIF manifest associated with the resource.

The current implementation used the Primo customization package with:

- AngularJS.
- JavaScript.
- HTML.
- CSS.
- An existing IIIF viewer such as Mirador or Universal Viewer.

## 2022–2023: Sharing the Architecture

The Library shared this approach with other research libraries investigating external IIIF manifests and Alma/Primo integration.

The key message was that **We use remote digital repository (e.g. NetX) to store the original files**. The Library could maintain its digital assets externally while Alma represented the digital inventory and Primo provided discovery and presentation.

## 2026: Primo NDE Transition

The move to Primo NDE changes the front-end customization framework.

The IIIF viewer customization must therefore be rewritten for the NDE environment. However, the fundamental integration remains unchanged.

This demonstrates one of the original architecture's strengths: the discovery interface can evolve without requiring the digital asset repository or IIIF delivery model to be redesigned.
