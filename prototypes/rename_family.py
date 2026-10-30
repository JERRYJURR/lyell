from pathlib import Path
import json,hashlib,shutil,zipfile
from fontTools.ttLib import TTFont
# Renames the 0.200 Proof families to Lyell as release 0.201. Outlines, metrics, kerning and features are unchanged.
ROOT=Path(__file__).resolve().parent;SRC=ROOT/'v0.200';OUT=ROOT/'v0.201';OUT.mkdir(exist_ok=True)
VERSION='0.201'
manifest=[]
for path in sorted(SRC.glob('Proof*.ttf')):
 f=TTFont(path);name=f['name']
 for rec in name.names:
  if rec.nameID in [1,3,4,6,16]:
   s=rec.toUnicode().replace('Proof Sans','Lyell Sans').replace('Proof Serif','Lyell Serif').replace('ProofSans','LyellSans').replace('ProofSerif','LyellSerif').replace('-0.200','-'+VERSION)
   rec.string=s
  elif rec.nameID==5:rec.string=f'Version {VERSION}; family proof'
 assert not any('Proof'in r.toUnicode()for r in name.names if r.nameID!=13),path
 f['head'].fontRevision=float(VERSION)
 out=OUT/path.name.replace('Proof','Lyell');f.save(out)
 manifest.append({'file':out.name,'family':name.getDebugName(16),'style':name.getDebugName(17),'weight':f['OS/2'].usWeightClass,'italic':bool(f['OS/2'].fsSelection&1),'glyphs':len(f.getGlyphOrder()),'renamed_from':path.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 print(out.name,flush=True)
assert len(manifest)==16
for kind in ['Sans','Serif']:shutil.copyfile(SRC/f'Proof{kind}-OFL.txt',OUT/f'Lyell{kind}-OFL.txt')
for n in ['sources.json']:shutil.copyfile(SRC/n,OUT/n)
spacing=(SRC/'spacing-validation.json').read_text().replace('ProofSans','LyellSans').replace('ProofSerif','LyellSerif').replace('Proof Sans','Lyell Sans').replace('Proof Serif','Lyell Serif')
(OUT/'spacing-validation.json').write_text(spacing)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
