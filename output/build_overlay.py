from pathlib import Path
import re, urllib.request, json, base64, io
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
root=Path(__file__).parent
css=(root/'fonts.css').read_text()
paths={'Söhne Buch':Path.home()/'Library/Fonts/TestSöhne-Buch.otf','Martina Plantijn Regular':Path.home()/'Library/Fonts/TestMartinaPlantijn-Regular.otf'}
for name in ['Inter','Work Sans','Source Serif 4','Newsreader']:
    block=next(b for b in css.split('@font-face') if "font-family: '%s'"%name in b and 'font-style: normal;' in b and 'font-weight: 400;' in b)
    url=re.search(r'url\((.*?)\)',block).group(1)
    path=root/(name.replace(' ','-')+'.ttf')
    if not path.exists(): urllib.request.urlretrieve(url,path)
    paths[name]=path
samples=['Hamburgefontsiv','a','g','e','s','r','R','G','Q','0123456789']
data={}
for name,path in paths.items():
    tf=TTFont(path)
    print(name, 'internal:',tf['name'].getDebugName(4))
    missing=set(''.join(samples))-set(map(chr,tf.getBestCmap()))
    assert not missing,(name,missing)
    # Measure the actual rasterized x rather than relying on optional metadata.
    test=ImageFont.truetype(str(path),1000)
    bb=test.getbbox('x',anchor='ls'); ratio=(bb[3]-bb[1])/1000
    font=ImageFont.truetype(str(path),round(90/ratio))
    data[name]={}
    for sample in samples:
        w=1600 if len(sample)>1 else 300
        im=Image.new('RGBA',(w,280)); draw=ImageDraw.Draw(im)
        draw.text((20,200),sample,font=font,fill=(0,0,0,255),anchor='ls')
        out=io.BytesIO(); im.save(out,format='PNG')
        data[name][sample]='data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
(root/'overlay-data.json').write_text(json.dumps(data))
