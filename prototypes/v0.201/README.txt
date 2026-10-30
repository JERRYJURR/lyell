Lyell Sans / Lyell Serif — version 0.201

Naming release: 16 static TrueType fonts. This is version 0.200 (Proof Sans / Proof Serif) renamed to Lyell Sans / Lyell Serif.
Only the name table and head.fontRevision differ from 0.200. Outlines, metrics, kerning, features and style flags are unchanged. Every other table is byte-identical. See ../v0.200/README.txt for construction, spacing and limitations.

Families
Lyell Sans (from Inter) and Lyell Serif (from STIX Two Text). Each has Regular (400), Medium (500), Semibold (600) and Bold (700), with matching italics.

Installation
The family names differ from earlier proofs, so installing these does not replace an installed Proof Sans / Proof Serif. Uninstall the old proofs to avoid duplicate menu entries.

Validation
The verify_family.py checks were re-run on these files: rasterization of every glyph at 16 and 64 pixels, reload/checksum, contour topology, shaping and accent samples, style metadata and licence. Results are in validation.json. manifest.json maps each file to its 0.200 source.

Licensing and attribution
Both families remain under the SIL Open Font License 1.1. Keep the supplied OFL notices with their corresponding fonts. Original copyright/author notices are retained in the font metadata. Neither Klim nor the original open-font authors endorse these derivatives. No Klim outlines or font binaries are included.

Rebuild in the project workspace
  .venv/bin/python sources/family/download.py
  .venv/bin/python prototypes/build_family.py
  .venv/bin/python prototypes/family_spacing.py
  .venv/bin/python prototypes/expand_family_kerning.py
  .venv/bin/python prototypes/rename_family.py
  .venv/bin/python prototypes/verify_family.py v0.201
