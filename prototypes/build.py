"""Build reversible, regular-weight design studies from OFL source fonts.
No Klim font is read by this build. The installed references are used only by proof rendering.
"""
from pathlib import Path
from copy import deepcopy
import json,hashlib,shutil
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'prototypes'

def build(source,family,kind):
 font=TTFont(source);cmap=font.getBestCmap();glyf=font['glyf'];changed={}
 def edit(name,operation,description):
  g=glyf[name];assert not g.isComposite(),name
  old=list(g.coordinates);g.coordinates=GlyphCoordinates([tuple(round(v) for v in operation(i,x,y)) for i,(x,y) in enumerate(old)])
  if list(g.coordinates)!=old:changed.setdefault(name,[]).append(description)
 # A modest cap-height experiment, preserving widths and lowercase height.
 caps={cmap[ord(c)]for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
 for n in caps:edit(n,lambda i,x,y:(x,y*1.03 if y>0 else y),'Raise positive capital coordinates 3%; retain advance widths')
 if kind=='sans':
  # Shorten the intrusive upper end of the Q tail along its existing diagonal.
  edit(cmap[ord('Q')],lambda i,x,y:(x+82,y-108) if i in [0,1] else (x+50,y-70) if i in [4,5] else (x,y),'Shorten the inside end and extend the outside end of the Q tail')
  # Flatten the cut on a slightly, without changing the bowl skeleton.
  edit(cmap[ord('a')],lambda i,x,y:(x,y+18 if i==22 else y-18 if i==23 else y),'Reduce the slope of the upper a terminal')
  # Shorten the open descender, tapering the adjustment at baseline.
  edit(cmap[ord('g')],lambda i,x,y:(x,y*.94 if y<0 else y),'Shorten the g descender 6% below baseline')
 else:
  # Retain STIX's drawn forms and give the Q tail slightly more depth.
  edit(cmap[ord('Q')],lambda i,x,y:(x,y*1.10 if 17<=i<=29 and y<0 else y),'Increase the depth of the Q tail 10%')
  # Half the advance reduction comes from each sidebearing, rather than scaling outlines.
  basic={cmap[ord(c)]for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'}
  for n in basic:
   advance,lsb=font['hmtx'][n];reduction=round(advance*.012);shift=-(reduction//2)
   edit(n,lambda i,x,y:(x+shift,y),'Shift outline left to share 1.2% advance reduction across sidebearings')
   font['hmtx'][n]=(advance-reduction,lsb+shift)
  for c in [' ','\u00a0']:
   if ord(c) in cmap:
    n=cmap[ord(c)];a,l=font['hmtx'][n];font['hmtx'][n]=(round(a*.97),l)
 # Existing composites inherit base-outline edits. Accent/mark positioning is not finalized.
 for name in font.getGlyphOrder():glyf[name].removeHinting()
 for tag in ['prep','fpgm','cvt ','hdmx','LTSH','STAT']:
  if tag in font:del font[tag]
 for name in font.getGlyphOrder():
  glyf[name].recalcBounds(glyf)
  if glyf[name].numberOfContours!=0:
   a,_=font['hmtx'][name];font['hmtx'][name]=(a,glyf[name].xMin)
 font['OS/2'].sCapHeight=round(font['OS/2'].sCapHeight*1.03)
 font['head'].fontRevision=.101
 font['head'].flags &= ~16 # No instructions may alter advance widths.
 if 'gasp' in font:font['gasp'].gaspRange={65535:10}
 licence=(ROOT/'output/licenses'/('inter-OFL.txt' if kind=='sans' else 'stixtwotext-OFL.txt')).read_text()
 names=font['name']
 replacement={1:family,2:'Regular',3:family.replace(' ','')+'-Regular-0.101',4:family+' Regular',5:'Version 0.101; experimental study',6:family.replace(' ','')+'-Regular',16:family,17:'Regular',13:licence,14:'https://openfontlicense.org/'}
 names.names=[n for n in names.names if n.nameID not in set(replacement)|{21,22}]
 for ident,value in replacement.items():names.setName(value,ident,3,1,0x409)
 path=OUT/(family.replace(' ','')+'-Regular.ttf');font.save(path)
 shutil.copyfile(ROOT/'output/licenses'/('inter-OFL.txt' if kind=='sans' else 'stixtwotext-OFL.txt'),OUT/(family.replace(' ','')+'-OFL.txt'))
 reopened=TTFont(path,checkChecksums=2)
 assert reopened.getBestCmap()==cmap
 for n in reopened.getGlyphOrder():
  g=reopened['glyf'][n]
  if not g.isComposite() and g.numberOfContours>0:assert len(g.coordinates)==len(g.flags) and g.endPtsOfContours[-1]==len(g.coordinates)-1
 assert reopened['name'].getDebugName(1)==family
 return {'font':path.name,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changed_outlines':changed,'glyph_count':len(reopened.getGlyphOrder()),'status':'Basic Latin regular proof; accents, mark positioning, italics, other weights and hinting not finalized'}
manifest=[build(ROOT/'output/Inter.ttf','Proof Sans','sans'),build(ROOT/'output/STIX-Two-Text.ttf','Proof Serif','serif')]
(OUT/'changes.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps([{k:v for k,v in m.items() if k!='changed_outlines'}for m in manifest],indent=2))
