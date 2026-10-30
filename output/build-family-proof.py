from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from shaped_raster import ShapedFont
import io,base64,json
ROOT=Path(__file__).resolve().parent.parent;p=ROOT/'output'
styles=[('Regular',400,False),('Italic',400,True),('Medium',500,False),('MediumItalic',500,True),('Semibold',600,False),('SemiboldItalic',600,True),('Bold',700,False),('BoldItalic',700,True)]
body='The quiet character of everyday things becomes clearer when we take the time to look. A well-made book and a familiar street give a place its identity.\n\nQuiet gardens, rare arrangements and little details make the ordinary memorable.'
def encode(im):
 rgba=Image.new('RGBA',im.size,(255,255,255,0));rgba.putalpha(im);out=io.BytesIO();rgba.quantize(colors=16,method=Image.Quantize.FASTOCTREE).save(out,format='PNG',optimize=True)
 return 'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
def samples(path):
 f=TTFont(path);ratio=f['OS/2'].sxHeight/f['head'].unitsPerEm;font=ShapedFont(path,65/ratio);glyphs=Image.new('L',(1100,220));font.draw(glyphs,(25,150),'a g r t f R Q')
 assert font.getlength('a g r t f R Q')<1050
 font=ShapedFont(path,18/ratio);lines=[]
 for para in body.split('\n\n'):
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if font.getlength(trial)>640:lines.append(line);line=word
   else:line=trial
  lines.extend([line,''])
 lines=lines[:-1];im=Image.new('L',(680,700))
 for i,line in enumerate(lines):font.draw(im,(18,42+i*48),line)
 assert len(lines)*48<690,(path,len(lines))
 thumb=Image.new('L',(720,100));font=ShapedFont(path,28/ratio);font.draw(thumb,(12,65),'Quiet reading')
 return {'glyphs':encode(glyphs),'body':encode(im),'thumb':encode(thumb)}
for kind in ['Sans','Serif']:
 data={}
 for style,w,italic in styles:
  proof=ROOT/f'prototypes/v0.200/Proof{kind}-{style}.ttf'
  if kind=='Sans':
   wt={400:'Buch',500:'Kräftig',600:'Halbfett',700:'Dreiviertelfett'}[w];rn='TestSöhne-'+wt+('Kursiv'if italic else'')+'.otf';ref=Path.home()/'Library/Fonts'/rn;label='Söhne '+wt+(' Kursiv'if italic else'')
  elif w==600:
   ref=ROOT/('sources/family/STIXTwoText-'+('Italic'if italic else'Roman')+'-600.ttf');label='Unmodified STIX Two Text Semibold'+(' Italic'if italic else'')
  else:
   wt={400:'',500:'Medium',700:'Bold'}[w];rn='TestMartinaPlantijn-'+(('Italic'if not wt else wt+'Italic')if italic else(wt or'Regular'))+'.otf';ref=Path.home()/'Library/Fonts'/rn;label='Martina Plantijn '+(('Italic'if not wt else wt+' Italic')if italic else(wt or'Regular'))
  data[style]={'weight':w,'italic':italic,'referenceLabel':label,'reference':samples(ref),'proof':samples(proof)}
 out=p/f'family-{kind.lower()}-data.json';out.write_text(json.dumps(data));print(kind,out.stat().st_size,flush=True)
