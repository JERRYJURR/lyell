from pathlib import Path
from PIL import Image
from shaped_raster import ShapedFont
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import json,base64,io
p=Path(__file__).parent
paths={'Söhne Buch':Path.home()/'Library/Fonts/TestSöhne-Buch.otf','Martina Plantijn Regular':Path.home()/'Library/Fonts/TestMartinaPlantijn-Regular.otf',**{n:p/(n.replace(' ','-')+'.ttf') for n in ['Inter','Libre Caslon Text','STIX Two Text']}}
text='The quiet character of everyday things becomes clearer when we take the time to look. A well-made book, a familiar street, a small shop on the corner. Ordinary details give a place its identity.\n\nReading is a conversation between the eye and the page. Letters need enough room to breathe, yet enough closeness to form a steady rhythm. Strong shapes can feel gentle, delicate details can remain clear. The best choice is the one that makes a long passage feel natural, without asking the reader to notice the type.'
glyphs='a g e s r t n o R G Q f'.split()
def encode(im):
 rgba=Image.new('RGBA',im.size,(255,255,255,0));rgba.putalpha(im)
 out=io.BytesIO();rgba.quantize(colors=16,method=Image.Quantize.FASTOCTREE).save(out,format='PNG',optimize=True)
 return 'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
data={}
print('Shaping: HarfBuzz; raster: FreeType, unhinted')
for name,path in paths.items():
 tf=TTFont(path);cmap=tf.getBestCmap();assert set(text.replace('\n','')+''.join(glyphs))<=set(map(chr,cmap)),repr(set(text.replace('\n','')+''.join(glyphs))-set(map(chr,cmap)))
 gs=tf.getGlyphSet();pen=BoundsPen(gs);gs[cmap[ord('x')]].draw(pen);ratio=pen.bounds[3]/tf['head'].unitsPerEm
 # Render each glyph independently at its own origin, so spacing cannot accumulate.
 font=ShapedFont(path,80/ratio)
 sheet=Image.new('L',(960,560))
 for i,char in enumerate(glyphs):font.draw(sheet,(i%6*160+20,i//6*280+180),char)
 bodyfont=ShapedFont(path,20/ratio);lines=[]
 for para in text.split('\n\n'):
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if bodyfont.getlength(trial)>650:lines.append(line);line=word
   else:line=trial
  lines.extend([line,''])
 lines=lines[:-1]
 im=Image.new('L',(680,1000))
 for i,line in enumerate(lines):bodyfont.draw(im,(10,48+i*52),line)
 assert 48+(len(lines)-1)*52<980,(name,len(lines))
 data[name]={'glyphs':encode(sheet),'paragraph':encode(im),'lines':len(lines),'xheightRatio':ratio}
 print(name,'xheight ratio',round(ratio,4),'lines',len(lines),'phrase width',round(bodyfont.getlength('Hamburgefontsiv'),2))
(p/'close-study-data.json').write_text(json.dumps(data))
print('bytes',(p/'close-study-data.json').stat().st_size)
