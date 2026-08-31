# Alma Configuration

## Purpose

Alma provides the library-management and digital-inventory layer for the integration. The original images remain in NetX/eDAM.

## Requirement for Primo View Online

For Primo to expose **View Online**, the Alma bibliographic resource needs appropriate electronic or digital inventory. For Alma NetX integration, this is accomplished through a **digital representation** of bib title associated with an Alma Collection and a Remote Digital Repository.

## Remote Digital Repository

The Library configured Alma with a Remote Digital Repository for NetX (external digital asset environment).

NetX is configured using repository type **Other**, with custom integration logic/scripts communicating with the NetX API and IIIF Image API.

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

## Collection Requirement

Historical implementation notes indicate that digital representations were associated with a Collection umbrella. All newly created digital representations are created automatically with the process of auto creating IIIF manifest, as well as put under default library collections.

## Integration Logic

The NetX integration is not simply an OAI metadata harvest. Custom logic is required to associate the Alma resource with the appropriate external digital object and IIIF services.

Implementation-specific scripts, code and configurations are stored separately with the appropriate access control.

## Validation Checklist

When a new resource is configured, confirm:

- Bibliographic record exists and is correct.
- Resource is associated with the expected Alma Collection.
- Digital representation exists.
- Primo displays View Online.
- IIIF manifest loads.
- Viewer displays all expected images.

## Primo NDE

The Alma configuration and Remote Digital Repository model are not expected to change fundamentally because of Primo NDE. 
NDE primarily affects the discovery/presentation customization used to render the IIIF viewer. 
