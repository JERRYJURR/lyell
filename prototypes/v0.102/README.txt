Proof Sans / Proof Serif — version 0.102

Second experimental regular-weight studies, derived from the preserved version 0.101 proofs of Inter and STIX Two Text. The first-version fonts and archive remain in the parent directory.

Changes from 0.101
Proof Sans: narrow word spaces; make a, s, o, O, Q, R and G fuller; narrow f; widen and raise t; adjust selected letter advances. The first pass's cap-height, a-terminal, g-descender and Q-tail changes remain.
Proof Serif: narrow word spaces; narrow a and e slightly; broaden r, t, f, g and G; lower the t ascender and raise f; adjust selected letter advances. First-pass capital proportions and Q-tail changes remain.

Horizontal outline edits use smooth displacement with zero displacement slope at the outer extrema, to reduce changes to side-stem weight. They are adjustments to the open fonts' own contours. No Klim outlines are incorporated. The build script reads only version 0.101 fonts; locally installed Klim trial fonts are used for reference rendering and measurements.

Validation
- Both fonts reload with checksums checked and preserve simple-glyph point/contour consistency.
- Names, version metadata and embedded OFL notices checked.
- Printable ASCII and test sentences shape without missing glyphs and rasterize through HarfBuzz/FreeType.
- Mean absolute relative line-width difference on eight held-out sentences, normalized to a common lowercase x-height:
  Sans: 3.06% in 0.101, 1.22% in 0.102.
  Serif: 1.33% in 0.101, 0.56% in 0.102.
  These are spacing diagnostics for this small sample, not overall similarity scores or a guarantee of matching layout.

Limitations
Regular basic Latin design proofs, not production-ready families. Accent offsets, mark anchors, derived ligature outlines, other scripts, other weights, italics and hinting are not finalized. Some detailed letter constructions still differ visibly from the references. Existing ligatures retain their inherited drawings, so f refinements are not yet propagated to every ligature. Some composites inherit modified base outlines without finalized spacing or positioning.

Both derivatives remain under the SIL Open Font License 1.1. Keep each accompanying OFL file with its font. Original notices are preserved. These studies are not endorsed by the original authors or Klim. They have not been installed automatically.

Rebuild from the workspace:
  .venv/bin/python prototypes/build_v2.py
A complete parameter log is in changes.json. Existing version 0.101 inputs and their SHA-256 hashes are recorded there.
