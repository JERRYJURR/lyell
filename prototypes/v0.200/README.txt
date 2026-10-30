Proof Sans / Proof Serif — version 0.200

Initial family proof release: 16 static TrueType fonts.
Each family includes Regular (400), Medium (500), Semibold (600), and Bold (700), with matching italics. Earlier proof versions remain preserved in the project workspace.

Construction
The upright designs carry the accepted 0.103 contour changes into compatible real source weights from Inter and STIX Two Text. Existing source-node displacements drive the weight changes; new contour points use local displacement interpolation. This is a proof-building method, not a manually finished variable family.
The regular upright drawings are retained from 0.103, with additional family spacing corrections.

The italics use actual italic sources, not a globally slanted copy of the upright family. Proof Sans uses native italic forms with selected upright-derived a, R, Q and f drawings to retain the revised double-storey a and family construction. Its inclination is 8 degrees.
Proof Serif retains the native italic a, g, r and t constructions, with an 18-degree inclination, a redrawn Q tail, and a new sloped f descender. The f refinement also covers the contextual forms used in office, affinity and fluff. Weight-specific outline fitting and advance adjustments improve the italic text rhythm. Mark anchors and component transformations follow the global shear.

Spacing
Selected letter pairs were scanned for unintended substantial raster overlap. Repairs are specific to each style, and canonical accented equivalents receive the same corrections. Designed contextual f/i/l joins were excluded from the automated collision scan and inspected in word samples. The audit records the tested cases and corrections in spacing-validation.json; it is not a complete kerning review.

Naming and use
Family and style metadata, weight classes, italic flags, caret slopes and unique PostScript names are set. Regular/Bold/Italic/Bold Italic use conventional legacy style linking; Medium and Semibold use legacy subfamilies plus common typographic-family names. Menu grouping can vary by application.
The fonts have not been installed automatically. They use the same Proof Sans / Proof Serif names as previous proofs, so installing them may replace an older installed proof.

Validation
Every glyph in all 16 fonts was rasterized at 16 and 64 pixels. Reload/checksum, simple-contour topology, character shaping, precomposed and decomposed accent samples, style metadata and licence checks passed. Word and paragraph samples were visually reviewed, including contextual f forms. Results are in validation.json.
The installed Klim trials provide comparisons at corresponding named weights. There is no installed matching Martina Plantijn Semibold, so that proof comparison uses the unmodified STIX Two Text Semibold source. Numeric weight labels do not guarantee identical visual weight across families.

Limitations
These are reviewable family proofs, not final production releases. Full manual master refinement, production hinting, exhaustive multilingual and mark-positioning review, all kerning pairs, and every alternate remain unfinished. Light, Black and variable-font builds are not included in this initial range. The degree of visual similarity varies by style; no exact-match claim is made.

Licensing and attribution
Both families remain under the SIL Open Font License 1.1. Keep the supplied OFL notices with their corresponding fonts. Original copyright/author notices are retained in the font metadata. Neither Klim nor the original open-font authors endorse these derivatives. No Klim outlines or font binaries are included in the builds or this archive.

Rebuild in the project workspace
  .venv/bin/python sources/family/download.py
  .venv/bin/python prototypes/build_family.py
  .venv/bin/python prototypes/family_spacing.py
  .venv/bin/python prototypes/expand_family_kerning.py
  .venv/bin/python prototypes/verify_family.py
The build also requires the preserved 0.103 regular proofs. Input versions and hashes are recorded in sources.json; final font hashes and styles are in manifest.json.
