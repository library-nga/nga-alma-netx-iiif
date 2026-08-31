# Alma Configuration

## Purpose

Alma provides the library-management and digital-inventory layer for the integration. The original images remain in NetX/eDAM.

## Requirement for Primo View Online

For Primo to expose **View Online**, the Alma bibliographic resource needs appropriate electronic or digital inventory.

For the NGA Library implementation, this is accomplished through a **digital representation** associated with an Alma Collection and a Remote Digital Repository.

## Remote Digital Repository

The Library configured a Remote Digital Repository for the external digital asset environment.

NetX was configured using repository type **Other**, with custom integration logic/scripts communicating with the NetX API.

Conceptually:

```text
Bibliographic record
      ↓
Alma Collection
      ↓
Digital representation
      ↓
Remote Digital Repository
      ↓
NetX/eDAM / IIIF resource
```

## Why Remote Rather Than Alma-Managed Storage

The architecture intentionally keeps storage responsibility with the Gallery's DAM.

Benefits include:

- No duplicate master image storage in Alma.
- eDAM remains the authoritative asset-management environment.
- Existing Gallery image-publishing infrastructure is reused.
- IIIF provides a standards-based delivery interface.
- Primo can change independently of image storage.

## Collection Requirement

Historical implementation notes indicate that digital representations were associated with a Collection umbrella. Staff creating new digital resources should therefore verify both the representation and the expected Collection relationship.

## Integration Logic

The NetX integration is not simply an OAI metadata harvest. Custom logic is required to associate the Alma resource with the appropriate external digital object and IIIF services.

Implementation-specific scripts and API credentials should not be documented in public-facing Markdown. Code and configuration should be stored separately with appropriate access controls.

## Validation Checklist

When a new resource is configured, confirm:

- Bibliographic record exists and is correct.
- Resource is associated with the expected Alma Collection.
- Digital representation exists.
- Representation uses the correct Remote Digital Repository.
- External identifier/resource information resolves correctly.
- Primo displays View Online.
- IIIF manifest loads.
- Viewer displays all expected images.

## Primo NDE

The Alma configuration and Remote Digital Repository model are not expected to change fundamentally because of Primo NDE. NDE primarily affects the discovery/presentation customization used to render the IIIF viewer.