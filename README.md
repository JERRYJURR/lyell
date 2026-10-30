# Lyell Sans & Lyell Serif

Custom font development based on Inter and STIX Two Text, under the SIL Open Font License 1.1.

The latest proofs are in `prototypes/v0.200/`: four weights with matching italics for each family (16 static TTFs). Their internal names are still **Proof Sans** and **Proof Serif**; the Lyell naming update has not yet been applied.

## Project contents

- `prototypes/`: build scripts, preserved iterations, font licences, and validation reports.
- `sources/family/`: open-source font inputs and their download script.
- `output/`: comparison scripts, proof pages, rendered studies, and open-font references.

See `prototypes/v0.200/README.txt` for construction details, rebuilding instructions, validation, and outstanding production work. Keep the corresponding OFL notices with distributed fonts.

Comparison scripts may require separately installed Klim trial fonts. Those proprietary font binaries are not included. The family build uses the open-source inputs and preserved modified regular proofs.

The local Python virtual environment is excluded from Git and must be recreated on another computer. The scripts use fontTools, Pillow, freetype-py, and uharfbuzz.
