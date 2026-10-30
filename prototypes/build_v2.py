"""Second independent design pass on the OFL proofs. No Klim files are read."""
from pathlib import Path
from copy import deepcopy
import json,shutil,hashlib
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'v0.102';OUT.mkdir(exist_ok=True)
manifest=[]
for kind in ['Sans','Serif']:
 source=ROOT/f'Proof{kind}-Regular.ttf';f=TTFont(source);cm=f.getBestCmap();glyf=f['glyf'];changes=[]
 def edit(char,fn,desc):
  n=cm[ord(char)];g=glyf[n];assert not g.isComposite()
  g.coordinates=GlyphCoordinates([(round(a),round(b))for a,b in (fn(x,y)for x,y in g.coordinates)])
  g.recalcBounds(glyf);changes.append({'glyph':char,'edit':desc})
 def width(char,pct):
  g=glyf[cm[ord(char)]];lo,hi=g.xMin,g.xMax;delta=(hi-lo)*pct
  # Smooth displacement is flat at the extremes, limiting distortion of side stems.
  def transform(x,y):
   t=max(0,min(1,(x-lo)/(hi-lo)));return x+delta*(t*t*(3-2*t)-.5),y
  edit(char,transform,f'Adjust ink width {pct:+.1%} with smooth displacement, preserving vertical coordinates')
 def advance(char,pct):
  n=cm[ord(char)];a,l=f['hmtx'][n];f['hmtx'][n]=(round(a*(1+pct)),l);changes.append({'glyph':char,'advance_change':pct})
 if kind=='Sans':
  for char,pct in {'a':.06,'s':.04,'o':.015,'O':.035,'Q':.035,'R':.04,'G':.02,'t':.04,'f':-.08}.items():width(char,pct)
  edit('t',lambda x,y:(x,y+max(0,y-1118)*.15),'Raise the t ascender above x-height, retaining its crossbar')
  for char,pct in {'a':-.015,'s':-.02,'o':-.01,'O':-.005,'Q':-.005,'R':.03,'t':.05,'f':-.08}.items():advance(char,pct)
  space=-.17
 else:
  for char,pct in {'a':-.02,'e':-.02,'r':.04,'t':.07,'f':.05,'g':.03,'G':.02}.items():width(char,pct)
  edit('t',lambda x,y:(x,y-max(0,y-473)*.16),'Lower the pointed t ascender while retaining the crossbar')
  edit('f',lambda x,y:(x,y+max(0,y-473)*.12),'Lift the f ascender above x-height')
  for char,pct in {'a':-.015,'e':-.015,'r':.04,'t':.06,'f':.04,'g':.015,'n':-.008,'u':-.02,'O':-.015,'Q':-.015}.items():advance(char,pct)
  space=-.22
 seen=set()
 for c in [' ','\u00a0']:
  if ord(c) in cm and cm[ord(c)] not in seen:advance(c,space);seen.add(cm[ord(c)])
 for n in f.getGlyphOrder():
  g=glyf[n];g.removeHinting();g.recalcBounds(glyf)
  if g.numberOfContours!=0:
   a,_=f['hmtx'][n];f['hmtx'][n]=(a,g.xMin)
 f['head'].fontRevision=.102
 for ident,value in {3:f'Proof{kind}-Regular-0.102',5:'Version 0.102; experimental study'}.items():
  f['name'].names=[n for n in f['name'].names if n.nameID!=ident];f['name'].setName(value,ident,3,1,0x409)
 path=OUT/source.name;f.save(path)
 shutil.copyfile(ROOT/f'Proof{kind}-OFL.txt',OUT/f'Proof{kind}-OFL.txt')
 manifest.append({'font':path.name,'base_version':'0.101','base_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changes':changes,'limitations':'Regular basic Latin study. Accent offsets, mark anchors, derived ligature forms, other scripts and hinting are not finalized.'})
(OUT/'changes.json').write_text(json.dumps(manifest,indent=2))
print('Built version 0.102; version 0.101 preserved.')
