from pathlib import Path
from PIL import Image,ImageDraw
from shaped_raster import ShapedFont
from fontTools.ttLib import TTFont
rows={'Sans':['ragged garden / Rare arrangements','aerial cargo / Regular gatherings','á à â ä ã å ă ą / ĝ ğ ġ / Ŕ Ř','a\u0301 a\u0308 g\u0306 R\u0301'], 'Serif':['Quarterly retreat / Quiet returns','A rare treat / Three quarters','ŕ ř ṙ / ť ṫ ţ / Q Q Q','r\u0301 r\u030c t\u0307 t\u0327']}
im=Image.new('RGB',(1400,1050),'white');d=ImageDraw.Draw(im)
for k,kind in enumerate(['Sans','Serif']):
 for col,version in enumerate(['102','103']):
  p=Path(f'prototypes/v0.{version}/Proof{kind}-Regular.ttf');tf=TTFont(p);f=ShapedFont(p,21/(tf['OS/2'].sxHeight/tf['head'].unitsPerEm));mask=Image.new('L',im.size)
  d.text((col*700+15,k*500+20),f'{kind} 0.{version}',fill='black')
  for j,line in enumerate(rows[kind]):f.draw(mask,(col*700+15,k*500+90+j*80),line)
  im.paste('black',(0,0),mask)
im.save('output/reading-contours.png')
