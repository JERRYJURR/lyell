from pathlib import Path
from PIL import Image,ImageDraw
from shaped_raster import ShapedFont
from fontTools.ttLib import TTFont
for kind,ref,chars in [('Sans','TestSöhne-Buch.otf','agR'),('Serif','TestMartinaPlantijn-Regular.otf','Qrt')]:
 im=Image.new('RGB',(1200,700),'white');d=ImageDraw.Draw(im)
 for row,path in enumerate([Path.home()/'Library/Fonts'/ref,Path('prototypes/v0.103')/f'Proof{kind}-Regular.ttf']):
  tf=TTFont(path);ratio=tf['OS/2'].sxHeight/tf['head'].unitsPerEm;font=ShapedFont(path,130/ratio)
  d.text((10,row*350+8),str(path.name),fill='black')
  mask=Image.new('L',im.size)
  for i,c in enumerate(chars):font.draw(mask,(50+i*390,260+row*350),c)
  im.paste('black',(0,0),mask)
 im.save(f'output/{kind.lower()}-six-after.png')
