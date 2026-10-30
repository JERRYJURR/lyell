from pathlib import Path
import sys,json,unicodedata
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'output'))
from shaped_raster import ShapedFont
from PIL import Image,ImageChops
from fontTools.ttLib import TTFont
import freetype,uharfbuzz as hb
ROOT=Path(__file__).resolve().parent;report={}
for kind,chars in [('Sans','agR'),('Serif','Qrt')]:
 path=ROOT/'v0.103'/f'Proof{kind}-Regular.ttf';f=TTFont(path,checkChecksums=2);old=TTFont(ROOT/'v0.102'/path.name)
 assert f.getBestCmap()==old.getBestCmap()
 assert '0.103' in f['name'].getDebugName(5)
 assert f['name'].getDebugName(13).startswith('Copyright')
 face=freetype.Face(str(path))
 for size in [16,64]:
  face.set_pixel_sizes(0,size)
  for index,name in enumerate(f.getGlyphOrder()):
   g=f['glyf'][name]
   if not g.isComposite() and g.numberOfContours>0:assert len(g.coordinates)==len(g.flags) and g.endPtsOfContours[-1]==len(g.coordinates)-1
   face.load_glyph(index,freetype.FT_LOAD_RENDER)
 shaper=ShapedFont(path,128);pairs={a+b for a in chars for b in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'}|{b+a for a in chars for b in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'}
 overlaps=[]
 for pair in sorted(pairs):
  infos,positions=shaper.shape(pair)
  if len(infos)!=2:continue
  masks=[];x,y=40,210
  for info,pos in zip(infos,positions):
   mask=Image.new('L',(500,400));face=shaper.face;face.load_glyph(info.codepoint,freetype.FT_LOAD_RENDER|freetype.FT_LOAD_NO_HINTING);slot=face.glyph;b=slot.bitmap
   if b.width and b.rows:
    bm=Image.frombytes('L',(b.width,b.rows),bytes(b.buffer),'raw','L',b.pitch)
    mask.paste(bm,(round(x+pos.x_offset/64+slot.bitmap_left),round(y-pos.y_offset/64-slot.bitmap_top)))
   masks.append(mask);x+=pos.x_advance/64;y-=pos.y_advance/64
  if ImageChops.multiply(*masks).point(lambda x:255 if x>64 else 0).getbbox():overlaps.append(pair)
 assert not overlaps,(kind,overlaps)
 cm=f.getBestCmap();accented=[chr(c)for c in cm if len(d:=unicodedata.normalize('NFD',chr(c)))>1 and d[0] in chars]
 h=hb.Font(hb.Face(path.read_bytes()));hb.ot_font_set_funcs(h)
 for text in [''.join(chr(i)for i in range(32,127)),''.join(accented),unicodedata.normalize('NFD',''.join(accented)),'ragged garden Rare arrangements Quarterly retreat Quiet returns']:
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(h,b);assert all(i.codepoint for i in b.glyph_infos)
 # Accented bases must inherit edited outlines rather than retain an old standalone drawing.
 for c in accented:assert f['glyf'][cm[ord(c)]].isComposite()
 report[kind]={'glyphs_rendered_at_each_size':len(f.getGlyphOrder()),'raster_sizes':[16,64],'letter_pairs_checked':len(pairs),'collisions':overlaps,'accented_characters_checked':len(accented),'checks':['cmap preserved','font reload and checksums','names and licence','glyph topology','all-glyph rendering','pair collision scan','precomposed and decomposed accent shaping']}
 print(kind,report[kind],flush=True)
(ROOT/'v0.103/validation.json').write_text(json.dumps(report,indent=2))
