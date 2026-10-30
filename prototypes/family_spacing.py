"""Audit and repair unintended overlaps in selected ASCII pairs in the family proofs."""
from pathlib import Path
import sys,json,math,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'output'))
from shaped_raster import ShapedFont
from PIL import Image,ImageChops
import freetype
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildPairPosGlyphsSubtable,buildLookup,buildValue
ROOT=Path(__file__).resolve().parent/'v0.200'
chars='agRQrtf';letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
pairs=sorted({a+b for a in chars for b in letters}|{b+a for a in chars for b in letters})
def scan(path):
 font=ShapedFont(path,128);tt=TTFont(path);names=tt.getGlyphOrder();upm=tt['head'].unitsPerEm;found={};intentional=[]
 for pair in pairs:
  infos,positions=font.shape(pair)
  if len(infos)!=2:continue
  ns=tuple(names[i.codepoint]for i in infos)
  # Contextual f/i/l connections are designed joining forms, inspected separately.
  if any(n.startswith(('f.','i.f_','l.f_'))for n in ns):intentional.append(pair);continue
  masks=[];x,y=50,200
  for info,pos in zip(infos,positions):
   m=Image.new('L',(500,350));font.face.load_glyph(info.codepoint,freetype.FT_LOAD_RENDER|freetype.FT_LOAD_NO_HINTING);slot=font.face.glyph;b=slot.bitmap
   if b.width and b.rows:
    bm=Image.frombytes('L',(b.width,b.rows),bytes(b.buffer),'raw','L',b.pitch);m.paste(bm,(round(x+pos.x_offset/64+slot.bitmap_left),round(y-pos.y_offset/64-slot.bitmap_top)))
   masks.append(m);x+=pos.x_advance/64;y-=pos.y_advance/64
  def hit(a,b):return ImageChops.multiply(a,b).point(lambda v:255 if v>64 else 0).getbbox()
  if hit(*masks):
   for shift in range(1,41):
    if not hit(masks[0],ImageChops.offset(masks[1],shift,0)):break
   else:raise ValueError((path.name,pair,'overlap exceeds repair range'))
   found[ns]={'pair':pair,'units':math.ceil((shift+1)*upm/128)}
 return found,intentional
records=[]
for path in sorted(ROOT.glob('*.ttf')):
 found,joins=scan(path)
 if found:
  f=TTFont(path);mapping={ns:(buildValue({'XAdvance':v['units']}),None)for ns,v in found.items()};t=f['GPOS'].table;i=len(t.LookupList.Lookup)
  t.LookupList.Lookup.append(buildLookup([buildPairPosGlyphsSubtable(mapping,f.getReverseGlyphMap())],table='GPOS'));t.LookupList.LookupCount=len(t.LookupList.Lookup)
  for r in t.FeatureList.FeatureRecord:
   if r.FeatureTag=='kern':r.Feature.LookupListIndex.append(i);r.Feature.LookupCount=len(r.Feature.LookupListIndex)
  f.save(path)
  remaining,_=scan(path);assert not remaining,(path,remaining)
 record={'file':path.name,'pairs_examined':len(pairs),'contextual_join_pairs_excluded':joins,'repairs':[{'glyphs':ns,**v}for ns,v in found.items()],'remaining_unintended_overlaps':0}
 records.append(record);print(path.name,'spacing fixes',len(found),[v['pair']for v in found.values()],flush=True)
(ROOT/'spacing-validation.json').write_text(json.dumps(records,indent=2))
m=json.loads((ROOT/'manifest.json').read_text())
for item in m:item['sha256']=hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()
(ROOT/'manifest.json').write_text(json.dumps(m,indent=2))
