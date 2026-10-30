from pathlib import Path
from PIL import Image,ImageDraw
from shaped_raster import ShapedFont
from fontTools.ttLib import TTFont
im=Image.new('RGB',(1400,1000),'white');d=ImageDraw.Draw(im)
paths=[Path.home()/'Library/Fonts/TestSöhne-BuchKursiv.otf',Path('sources/family/Inter-Italic-400.ttf'),Path.home()/'Library/Fonts/TestMartinaPlantijn-Italic.otf',Path('sources/family/STIXTwoText-Italic-400.ttf')]
for i,path in enumerate(paths):
 tf=TTFont(path);font=ShapedFont(path,60/(tf['OS/2'].sxHeight/tf['head'].unitsPerEm));mask=Image.new('L',im.size)
 d.text((20,i*240+10),path.name,fill='black');font.draw(mask,(20,i*240+150),'a g f r t R Q');font.draw(mask,(600,i*240+150),'Quiet reading')
 im.paste('black',(0,0),mask)
im.save('output/italic-start.png')
