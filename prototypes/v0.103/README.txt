Proof Sans / Proof Serif — version 0.103

A contour refinement pass on the preserved version 0.102 proofs. These are experimental regular-weight derivatives of Inter and STIX Two Text, under the SIL Open Font License 1.1.

Changes from 0.102
Proof Sans
- Constructed a curved exit foot on the a and refined its upper opening and terminal.
- Raised the g hook terminal and reshaped the approach, retaining descender depth.
- Raised the R bowl-to-leg junction, moved the leg attachment left and refined the lower counter.
- Added a little advance width to a to accommodate its new exit stroke.

Proof Serif
- Replaced the Q flourish with an independently constructed diagonal tail and flat end.
- Redrew the r head serif, shoulder and oblique terminal.
- Replaced the upturned t foot with a curved foot and upright end cut; extended and leveled its crossbar.
- Adjusted r and t advance widths.
- Added small positive kerning corrections to Qj, rw and vt, including canonical accented equivalents, after the inherited kerning lookups.

Dependent forms
Composite descendants inherit the contour changes. Changed advances are propagated through those composites. Affected canonical accented forms were checked in precomposed and decomposed text. No standard/discretionary letter ligature in these fonts directly substitutes the six edited base glyphs in the inspected liga/dlig/clig features. Older f-related ligature differences from prior passes are outside this pass.

Validation
- Preserved character maps; checked font loading/checksums, naming, licences and simple-glyph contour/point consistency.
- Rendered every glyph in each font at 16 and 64 pixels using FreeType.
- Checked 303 surrounding ASCII letter pairs per font for substantial raster overlap at 128 pixels. No collisions remained with kerning enabled.
- Checked 45 affected accented characters in the sans and 15 in the serif, including decomposed sequences.
- Visually reviewed enlarged letters, words, paragraph proofs, and accented samples.
- Full machine-readable results are in validation.json. These checks establish basic font integrity and the inspected cases; they are not a complete typographic or multilingual certification.

Scope and limitations
This regular-weight contour pass is ready for design review. Full production hinting, complete character-set review, all mark placement, other weights and italics remain unfinished. The six changed letters retain independent constructions; they are not traced or extracted Klim outlines. Installed Klim trial fonts are used only for reference rendering and measurement, never by the build script.

Previous versions remain unchanged. The fonts have not been installed automatically. Both files retain their Proof Sans / Proof Serif family names with updated internal versions, so installing a version may replace an earlier installed proof.

Licensing
Keep the included OFL notices with their corresponding fonts. Original authorship and copyright notices are preserved. These studies are not endorsed by Klim or the original font authors.

Rebuild and validation in this workspace:
  .venv/bin/python prototypes/build_v3.py
  .venv/bin/python prototypes/verify_v3.py
Inputs are the preserved files in prototypes/v0.102. Their SHA-256 hashes and the change summary are recorded in changes.json.
