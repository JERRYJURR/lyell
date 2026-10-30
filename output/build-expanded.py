from pathlib import Path
import re,urllib.request,urllib.parse,json,base64,io,concurrent.futures
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
root=Path(__file__).parent
sans=['Inter','Work Sans','Geist','Roboto','Arimo','Public Sans','Libre Franklin','IBM Plex Sans','DM Sans','Archivo']
serif=['Source Serif 4','Newsreader','Libre Baskerville','Libre Caslon Text','Crimson Pro','Crimson Text','EB Garamond','Lora','Literata','Vollkorn','Spectral','Alegreya','Gentium Book Plus','STIX Two Text']
(root/'licenses').mkdir(exist_ok=True)
def get(name):
 slug=name.lower().replace(' ',''); lic=root/'licenses'/(slug+'-OFL.txt')
 if not lic.exists(): urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/'+slug+'/OFL.txt',lic)
 path=root/(name.replace(' ','-')+'.ttf')
 if not path.exists():
  url='https://fonts.googleapis.com/css2?family='+urllib.parse.quote(name)+':wght@400'
  css=urllib.request.urlopen(url).read().decode()
  block=next(b for b in css.split('@font-face') if 'font-style: normal;' in b and 'font-weight: 400;' in b)
  url=re.search(r'url\((.*?)\)',block).group(1);urllib.request.urlretrieve(url,path)
 font=TTFont(path)
 if 'fvar' in font:
  loc={a.axisTag:400 if a.axisTag=='wght' else a.defaultValue for a in font['fvar'].axes}
  font=instantiateVariableFont(font,loc,inplace=False);path=root/(name.replace(' ','-')+'-instance.ttf');font.save(path)
 return name,path
paths={'Söhne Buch':Path.home()/'Library/Fonts/TestSöhne-Buch.otf','Martina Plantijn Regular':Path.home()/'Library/Fonts/TestMartinaPlantijn-Regular.otf'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for name,path in pool.map(get,sans+serif): paths[name]=path;print('Ready:',name,flush=True)
samples=['Hamburgefontsiv','a','g','e','s','r','R','G','Q']
data={}
for name,path in paths.items():
 tf=TTFont(path);assert set(''.join(samples))<=set(map(chr,tf.getBestCmap()))
 test=ImageFont.truetype(str(path),1000);bb=test.getbbox('x',anchor='ls');ratio=(bb[3]-bb[1])/1000
 font=ImageFont.truetype(str(path),round(55/ratio));data[name]={}
 for sample in samples:
  w=1100 if len(sample)>1 else 190
  bbox=font.getbbox(sample,anchor='ls');assert bbox[2]+8<w,(name,sample,bbox)
  im=Image.new('L',(w,180));draw=ImageDraw.Draw(im);draw.text((8,125),sample,font=font,fill=255,anchor='ls')
  rgba=Image.new('LA',im.size,255);rgba.putalpha(im)
  out=io.BytesIO();rgba.convert("RGBA").quantize(colors=16,method=Image.Quantize.FASTOCTREE).save(out,format='PNG',optimize=True)
  data[name][sample]='data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
payload={'sans':sans,'serif':serif,'images':data}
(root/'expanded-data.json').write_text(json.dumps(payload))
print('Data bytes:',(root/'expanded-data.json').stat().st_size)
