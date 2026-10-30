Proof Sans / Proof Serif — version 0.101

Experimental regular-weight fonts for design review, derived from Inter and STIX Two Text respectively. These are working names.

Proof Sans changes
- Raise positive A–Z outline coordinates by 3%, retaining widths and lowercase height.
- Shorten the inner Q tail and extend its outer end.
- Flatten the upper a terminal slightly.
- Shorten the g descender below the baseline by 6%.

Proof Serif changes
- Raise positive A–Z outline coordinates by 3%.
- Deepen the Q tail by 10% below the baseline.
- Reduce basic Latin letter advances by approximately 1.2%, distributing the reduction across both sidebearings.
- Reduce space width by approximately 3%.

These are localized outline and spacing experiments, not a completed type family. Existing OpenType layout features are retained. Obsolete TrueType hints have been removed; production hinting is not finished. Composite accents inherit base changes, but accent offsets and mark anchors have not been finalized. Other scripts, italics and heavier weights have not been redesigned. Proofs use HarfBuzz shaping and FreeType rendering.

The original fonts are unchanged. No Klim outline data is incorporated in either font. Installed Klim trial fonts are used only to render visual references.

Both derivatives remain under the SIL Open Font License 1.1. Keep each accompanying OFL file with its font. Original authorship and copyright notices are retained. These studies are not endorsed by the original font authors or Klim.

Rebuild in the project workspace:
  .venv/bin/python prototypes/build.py
The build expects output/Inter.ttf, output/STIX-Two-Text.ttf and their licences under output/licenses. Source hashes and per-glyph edits are recorded in changes.json. The build does not read any Klim font.

Review before use in production. These fonts have not been installed automatically.
