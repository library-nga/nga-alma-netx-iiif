# Primo IIIF Viewer Integration

## Purpose

Primo provides the patron-facing presentation layer for the Library's remotely managed digital resources.

## Primo VE Implementation

The Primo VE implementation embeds an IIIF viewer within the Primo full-record experience.

The customization uses:

- AngularJS.
- JavaScript.
- HTML templates.
- IIIF Presentation manifests.
- Universal Viewer for Main Library resources.
- Mirador for Image Collection resources.

**Source code:** [`sourcecode/primo-ve/image-viewer.js`](../sourcecode/primo-ve/image-viewer.js)  
**Implementation notes:** [`sourcecode/primo-ve/README.md`](../sourcecode/primo-ve/README.md)

### Viewer Routing

The customization reads the Primo PNX `control.sourcerecordid` and uses it to construct the IIIF manifest URL. The local display field `display.lds01` controls whether the viewer is enabled.

For Main Library resources, the default route is:

```text
Primo PNX source record ID
      ↓
libraryimage.nga.gov/manifest/mms/{ID}.json
      ↓
Universal Viewer
```

For Image Collection records, when the Primo best-location library code is `IMAGES`, the customization switches both the manifest collection and viewer:

```text
Primo record — libraryCode = IMAGES
      ↓
libraryimage.nga.gov/manifest/ic/{ID}.json
      ↓
Mirador
```

The implementation also distinguishes records delivered through Alma Digital (`Alma-D`) so the viewer can be inserted in the appropriate Primo component.

### Primo Component Placement

The source code uses two Primo VE extension points:

- `prmActionListAfter` — displays the viewer for applicable titles outside the Alma Digital View It section.
- `prmAlmaViewitAfter` — displays the viewer for records whose delivery category includes `Alma-D`.

See the [Primo VE source code](../sourcecode/primo-ve/image-viewer.js) for the implemented controller and component templates.

## Separation from Repository Logic

The viewer does not manage or store the images.

It consumes the IIIF Presentation manifest, which references image services delivered from the Gallery infrastructure. This means viewer replacement does not require a redesign of the DAM integration.

Conceptually:

```text
Primo full record
      ↓
PNX / Alma Digital delivery information
      ↓
Construct IIIF manifest reference
      ↓
Universal Viewer or Mirador
      ↓
Manifest + IIIF Image API
```

## Primo NDE

Primo NDE uses a different customization framework from the Primo VE AngularJS customization package.

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

The existing [Primo VE implementation](../sourcecode/primo-ve/) provides the functional reference for the NDE redevelopment while the underlying Alma–NetX–IIIF architecture remains unchanged.
