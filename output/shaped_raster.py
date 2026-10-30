import freetype,uharfbuzz as hb
from PIL import Image,ImageChops
class ShapedFont:
 def __init__(self,path,size):
  self.face=freetype.Face(str(path));self.face.set_char_size(round(size*64))
  self.font=hb.Font(hb.Face(open(path,'rb').read()));self.font.scale=(round(size*64),round(size*64));hb.ot_font_set_funcs(self.font)
 def shape(self,text):
  if not text:return [],[]
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(self.font,b);return b.glyph_infos,b.glyph_positions
 def getlength(self,text):return sum(p.x_advance for p in self.shape(text)[1])/64
 def draw(self,im,xy,text):
  x,y=xy
  for info,pos in zip(*self.shape(text)):
   self.face.load_glyph(info.codepoint,freetype.FT_LOAD_RENDER|freetype.FT_LOAD_NO_HINTING)
   slot=self.face.glyph;b=slot.bitmap
   if b.width and b.rows:
    mask=Image.frombytes('L',(b.width,b.rows),bytes(b.buffer),'raw','L',b.pitch)
    px,py=round(x+pos.x_offset/64+slot.bitmap_left),round(y-pos.y_offset/64-slot.bitmap_top)
    region=im.crop((px,py,px+b.width,py+b.rows));im.paste(ImageChops.lighter(region,mask),(px,py))
   x+=pos.x_advance/64;y-=pos.y_advance/64
