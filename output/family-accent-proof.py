from pathlib import Path
from PIL import Image,ImageDraw
from fontTools.ttLib import TTFont
from shaped_raster import ShapedFont
im=Image.new('RGB',(1500,1000),'white');d=ImageDraw.Draw(im)
for i,(kind,style) in enumerate([(k,s)for k in ['Sans','Serif']for s in ['Regular','Italic','Bold','BoldItalic']]):
 path=Path(f'prototypes/v0.200/Proof{kind}-{style}.ttf');f=TTFont(path);font=ShapedFont(path,21/(f['OS/2'].sxHeight/f['head'].unitsPerEm));mask=Image.new('L',im.size)
 d.text((15,i*120+5),kind+' '+style,fill='black');font.draw(mask,(25,i*120+70),'á ä ą ğ Ŕ Ř ř ṫ ţ   office affinity fluff   a\u0301 r\u030c t\u0307');im.paste('black',(0,0),mask)
im.save('output/family-accents.png')
