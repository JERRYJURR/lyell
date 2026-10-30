from pathlib import Path
from PIL import Image,ImageDraw
from fontTools.ttLib import TTFont
from shaped_raster import ShapedFont
for kind in ['Sans','Serif']:
 im=Image.new('RGB',(1600,1450),'white');d=ImageDraw.Draw(im)
 for i,style in enumerate(['Regular','Italic','Medium','MediumItalic','Semibold','SemiboldItalic','Bold','BoldItalic']):
  path=Path(f'prototypes/v0.200/Proof{kind}-{style}.ttf');f=TTFont(path);ratio=f['OS/2'].sxHeight/f['head'].unitsPerEm;font=ShapedFont(path,48/ratio)
  d.text((20,i*180+8),style,fill='black');mask=Image.new('L',im.size)
  font.draw(mask,(35,i*180+115),'a g r t f R Q');font.draw(mask,(700,i*180+115),'Quiet reading')
  im.paste('black',(0,0),mask)
 im.save(f'output/family-{kind.lower()}.png')
