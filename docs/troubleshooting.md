# Operations and Troubleshooting

## Troubleshooting Principle

Follow the service dependency chain from the source outward:

```text
NetX/eDAM
   ↓
Web Publish
   ↓
IIIF Image API
   ↓
IIIF Manifest
   ↓
Alma Digital Representation
   ↓
Primo Viewer
```

Do not begin with Primo if the image itself cannot be delivered through IIIF.

## Scenario: One Image in a Manifest Does Not Display

### Symptoms

- Manifest loads.
- Most images display.
- One individual image returns an error.

### Likely area

NetX/eDAM publishing or IIIF Image API delivery for the individual asset.

### Recovery

1. Identify the affected eDAM asset.
2. Test its IIIF Image API directly.
3. If delivery fails, unpublish the asset.
4. Republish the asset.
5. Verify the Image API again.
6. Repeat manifest/Alma processing if required.
7. Verify the object in Primo.

This has historically resolved intermittent asset-level publishing failures, although recurring cases should be investigated with the eDAM/NetX development team rather than treated only as an operational workaround.

## Scenario: Manifest Returns JSON Error

Check:

- Manifest URL and MMS ID.
- Whether the expected manifest has been generated.
- Whether a multi-volume suffix is required.
- Whether all referenced canvas IDs are valid.
- Whether all referenced image services resolve.
- Whether a recent republish requires manifest regeneration.

## Scenario: Image API Works but Primo Viewer Is Empty

Check in this order:

1. Open manifest URL directly.
2. Validate manifest JSON.
3. Open manifest in an independent IIIF viewer.
4. Verify Alma digital representation.
5. Confirm Primo exposes View Online.
6. Inspect browser developer console/network activity.
7. Inspect the Primo customization/component.

## Scenario: View Online Is Missing

Investigate Alma rather than the viewer first.

Confirm:

- Digital representation exists.
- Correct Remote Digital Repository is assigned.
- Expected Alma Collection relationship exists.
- Resource has been indexed/published to discovery.

## Scenario: Multi-Volume Resource

Manifest naming may follow:

```text
{MMS_ID}-1.json
{MMS_ID}-2.json
{MMS_ID}-3.json
```

However, not every multipart bibliographic record uses separate manifests. Verify how the resource was intentionally modeled before assuming a missing `-1`/`-2` manifest is an error.

## Scenario: External Project Uses Old Canvas IDs

The 2021 eDAM migration preserved manifest URLs but changed canvas/image identifiers to UUID-based values.

An external project that references a manifest URL should normally continue to find the manifest, but projects that stored individual canvas IDs may require updates.

## Information to Capture for Escalation

When reporting an issue, capture:

- Alma MMS ID.
- Primo permalink.
- eDAM/NetX asset ID or UUID.
- Manifest URL.
- Failing canvas/image-service URL.
- Time of failure.
- Whether unpublish/republish resolved it.
- Browser/network error if presentation is involved.

This makes it easier to determine whether the failure belongs to eDAM publishing, IIIF delivery, manifest generation, Alma configuration, or Primo presentation.