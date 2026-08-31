# Digital Publishing Workflow

## Purpose

This document describes the operational path from digitized Library content to public discovery and IIIF delivery.

## Workflow Summary

```text
Digitize resource
      ↓
Create/load images and metadata in NetX/eDAM
      ↓
Web Publish assets
      ↓
Verify IIIF Image API delivery
      ↓
Generate or regenerate IIIF manifest
      ↓
Maintain Alma digital representation
      ↓
Publish/index resource to Primo
      ↓
User opens View Online / IIIF viewer
```

## 1. Digitization and Asset Preparation

Digital images are created through the Library's digitization workflow.

Before public delivery, the images and required metadata are loaded into NetX/eDAM.

The DAM is the authoritative environment for the digital assets; Alma does not need duplicate master image files.

## 2. eDAM Web Publishing

Assets must be web-published before downstream IIIF delivery can succeed.

Publishing makes the asset available to the Gallery's web/IIIF infrastructure.

Operationally, publishing should be treated as a prerequisite for manifest generation and Primo delivery.

## 3. Verify IIIF Image Delivery

After publishing, verify that the affected image is actually available through the IIIF Image API.

This step is important because an asset can occasionally appear published in eDAM while its IIIF image delivery fails.

For multi-image objects, validate more than the first image when practical.

## 4. Generate / Regenerate the Manifest

The manifest describes the digital object and points to the relevant IIIF image services.

Standard conceptual manifest URL:

```text
https://libraryimage.nga.gov/manifest/mms/{MMS_ID}.json
```

For multi-volume resources:

```text
{MMS_ID}-1.json
{MMS_ID}-2.json
```

Manifest processing may occur through scheduled/nightly processing depending on the workflow.

## 5. Alma Digital Representation

The Alma bibliographic record must have the appropriate digital inventory so Primo can expose online access.

The implementation uses:

- Alma Collection relationship.
- Digital representation.
- Remote Digital Repository configuration.

The representation points outward to the remote digital environment rather than storing the master images in Alma.

## 6. Primo Discovery

Once the Alma resource is available to discovery, Primo presents the bibliographic description and **View Online** service.

The custom viewer integration consumes the IIIF manifest and displays the digital object within the Primo full-record experience.

## Republishing / Reprocessing

When an individual image fails through the IIIF Image API, the current recovery workflow is commonly:

```text
Identify failed image
      ↓
Unpublish in eDAM
      ↓
Republish in eDAM
      ↓
Verify IIIF Image API
      ↓
Repeat manifest processing if necessary
      ↓
Verify Primo viewer
```

This can create extra work because an image-level publishing problem may require both eDAM republishing and Alma/manifest reprocessing.

## Operational Dependency Chain

Troubleshooting should follow the dependency order rather than starting with Primo:

```text
NetX/eDAM asset
      ↓
Web-publishing state
      ↓
IIIF Image API
      ↓
IIIF Manifest
      ↓
Alma representation
      ↓
Primo viewer
```

If the direct IIIF Image API fails, the problem is upstream of Alma and Primo.

If the image API works but the manifest fails, investigate manifest generation/content.

If the manifest works directly but Primo does not display it, investigate Alma representation and Primo customization.