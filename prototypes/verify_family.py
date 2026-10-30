from pathlib import Path
import sys,json,unicodedata,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'output'))
from shaped_raster import ShapedFont
from fontTools.ttLib import TTFont
import freetype,uharfbuzz as hb
ROOT=Path(__file__).resolve().parent/(sys.argv[1]if len(sys.argv)>1 else'v0.201');report=[];names=set()
texts=['ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789','office affinity fluff efficient flight','Quiet reading and rare arrangements.','Á À Â Ä Ã Å Ă Ą á à â ä ã å ă ą ĝ ğ ġ Ŕ Ř ŕ ř ṙ ť ṫ ţ','a\u0301 a\u0308 g\u0306 R\u0301 r\u030c t\u0307']
for path in sorted(ROOT.glob('*.ttf')):
 f=TTFont(path,checkChecksums=2);ps=f['name'].getDebugName(6);assert ps not in names;names.add(ps)
 isitalic='Italic'in path.stem;assert bool(f['OS/2'].fsSelection&1)==isitalic and bool(f['head'].macStyle&2)==isitalic
 assert (f['post'].italicAngle<0)==isitalic
 assert f['OS/2'].usWeightClass in [400,500,600,700]
 assert f['name'].getDebugName(16)in ['Proof Sans','Proof Serif','Lyell Sans','Lyell Serif']
 assert f['name'].getDebugName(13).startswith('Copyright')
 face=freetype.Face(str(path))
 for size in [16,64]:
  face.set_pixel_sizes(0,size)
  for i,n in enumerate(f.getGlyphOrder()):
   g=f['glyf'][n]
   if not g.isComposite() and g.numberOfContours>0:assert g.endPtsOfContours[-1]==len(g.coordinates)-1 and len(g.coordinates)==len(g.flags)
   face.load_glyph(i,freetype.FT_LOAD_RENDER)
 h=hb.Font(hb.Face(path.read_bytes()));hb.ot_font_set_funcs(h)
 for text in texts:
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(h,b);assert all(i.codepoint for i in b.glyph_infos),(path,text)
 report.append({'file':path.name,'glyphs_rendered_at_each_size':len(f.getGlyphOrder()),'sizes':[16,64],'style_metadata':'passed','shaping_and_accent_samples':'passed','topology_and_reload':'passed'})
 print(path.name,'passed',flush=True)
assert len(report)==16
(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
