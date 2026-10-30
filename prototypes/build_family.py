"""Build a 16-style OFL proof family from real weight/italic sources.
Uprights transport edited regular contours through source weight displacements.
Italics retain native italic construction, with explicitly selected roman-derived sans forms.
No proprietary font is read by this build.
"""
from pathlib import Path
from copy import deepcopy
from array import array
import math,json,hashlib,shutil,unicodedata
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.otlLib.builder import buildPairPosGlyphsSubtable,buildLookup,buildValue
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'prototypes/v0.200';OUT.mkdir(exist_ok=True)
WEIGHTS={400:'Regular',500:'Medium',600:'Semibold',700:'Bold'}

def setcoords(g,coords):g.coordinates=GlyphCoordinates([(round(x),round(y))for x,y in coords]);g.removeHinting()
def contours(g):
 result=[];start=0
 for end in g.endPtsOfContours:
  result.append([(int(g.coordinates[i][0]),int(g.coordinates[i][1]),int(g.flags[i])&1)for i in range(start,end+1)]);start=end+1
 return result
def setcontours(g,cs):
 setcoords(g,[(x,y)for c in cs for x,y,flag in c]);g.flags=array('B',[flag for c in cs for x,y,flag in c]);g.endPtsOfContours=[];n=0
 for c in cs:n+=len(c);g.endPtsOfContours.append(n-1)
 g.numberOfContours=len(cs)
def displace_point(point,base,weighted):
 # Exact source nodes retain their corresponding master displacement.
 x,y=point;ds=[]
 for (a,b),(c,d)in zip(base,weighted):
  dist=(x-a)**2+(y-b)**2
  if dist<.01:return x+c-a,y+d-b
  ds.append((dist,c-a,d-b))
 ds=sorted(ds)[:6];den=sum(1/d for d,dx,dy in ds)
 return x+sum(dx/d for d,dx,dy in ds)/den,y+sum(dy/d for d,dx,dy in ds)/den

def addkern(font,rules):
 cm=font.getBestCmap();pairs={}
 def fam(c):return {n for code,n in cm.items()if unicodedata.normalize('NFD',chr(code))[0]==c}
 for a,b,v in rules:
  for left in fam(a):
   for right in fam(b):pairs[(left,right)]=(buildValue({'XAdvance':v}),None)
 if not pairs:return
 t=font['GPOS'].table;i=len(t.LookupList.Lookup);t.LookupList.Lookup.append(buildLookup([buildPairPosGlyphsSubtable(pairs,font.getReverseGlyphMap())],table='GPOS'));t.LookupList.LookupCount=len(t.LookupList.Lookup)
 for rec in t.FeatureList.FeatureRecord:
  if rec.FeatureTag=='kern':rec.Feature.LookupListIndex.append(i);rec.Feature.LookupCount=len(rec.Feature.LookupListIndex)

def shear(font,s):
 for name in font.getGlyphOrder():
  g=font['glyf'][name]
  if g.isComposite():
   for c in g.components:
    if hasattr(c,'x'):c.x=round(c.x+s*c.y)
    if hasattr(c,'transform'):
     # Conjugate component transform by the global shear.
     a,b=c.transform[0];c0,d=c.transform[1]
     c.transform=[[a+s*b,b],[c0+s*d-s*a-s*s*b,d-s*b]]
  elif g.numberOfContours>0:setcoords(g,[(x+s*y,y)for x,y in g.coordinates])
 seen=set()
 def anchors(obj):
  if obj is None or isinstance(obj,(str,int,float,bytes))or id(obj)in seen:return
  seen.add(id(obj))
  if obj.__class__.__name__=='Anchor' and hasattr(obj,'XCoordinate'):obj.XCoordinate=round(obj.XCoordinate+s*obj.YCoordinate)
  if isinstance(obj,(list,tuple)):
   for v in obj:anchors(v)
  elif hasattr(obj,'__dict__'):
   for v in vars(obj).values():anchors(v)
 if 'GPOS'in font:anchors(font['GPOS'].table)

def upright(kind,w):
 stem='Inter'if kind=='Sans'else'STIXTwoText'
 base=TTFont(ROOT/f'sources/family/{stem}-Roman-400.ttf');target=TTFont(ROOT/f'sources/family/{stem}-Roman-{w}.ttf');proof=TTFont(ROOT/f'prototypes/v0.103/Proof{kind}-Regular.ttf')
 if w==400:return proof
 for name in proof.getGlyphOrder():
  b,p,t=base['glyf'][name],proof['glyf'][name],target['glyf'][name]
  if not b.isComposite() and b.numberOfContours>0:
   assert b.endPtsOfContours==t.endPtsOfContours,name
   if list(b.coordinates)!=list(p.coordinates) or b.endPtsOfContours!=p.endPtsOfContours:
    g=deepcopy(p);setcoords(g,[displace_point(pt,b.coordinates,t.coordinates)for pt in p.coordinates]);target['glyf'][name]=g
  da=proof['hmtx'][name][0]-base['hmtx'][name][0]
  if da:a,l=target['hmtx'][name];target['hmtx'][name]=(a+da,l)
 target['OS/2'].sCapHeight=round(target['OS/2'].sCapHeight*1.03)
 if kind=='Serif':addkern(target,[('Q','j',20),('r','w',18),('v','t',18)])
 return target

def italic(kind,w,roman):
 stem='Inter'if kind=='Sans'else'STIXTwoText'
 f=TTFont(ROOT/f'sources/family/{stem}-Italic-{w}.ttf');glyf=f['glyf'];cm=f.getBestCmap();oldmetrics=dict(f['hmtx'].metrics)
 native=abs(f['post'].italicAngle);angle=8 if kind=='Sans'else 18
 slope=math.tan(math.radians(angle))-math.tan(math.radians(native));shear(f,slope)
 def width(char,amount):
  n=cm[ord(char)];g=glyf[n];g.recalcBounds(glyf);lo,hi=g.xMin,g.xMax;delta=(hi-lo)*amount
  def tx(x,y):
   t=max(0,min(1,(x-lo)/(hi-lo)));return x+delta*(t*t*(3-2*t)-.5),y
  setcoords(g,[tx(x,y)for x,y in g.coordinates])
 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
  g=glyf[cm[ord(char)]]
  if not g.isComposite():setcoords(g,[(x,y*1.03 if y>0 else y)for x,y in g.coordinates])
 f['OS/2'].sCapHeight=round(f['OS/2'].sCapHeight*1.03)
 if kind=='Sans':
  # Selected upright-derived forms make the sans cursive coherent with its revised roman.
  for char in ['a','R','Q','f']:
   rn=roman.getBestCmap()[ord(char)];n=cm[ord(char)];g=deepcopy(roman['glyf'][rn]);assert not g.isComposite()
   setcoords(g,[(x+math.tan(math.radians(angle))*y,y)for x,y in g.coordinates]);glyf[n]=g;f['hmtx'][n]=roman['hmtx'][rn]
  for char,pct in {'s':.035,'o':.015,'O':.035,'G':.02,'t':.035}.items():width(char,pct)
  g=glyf[cm[ord('g')]];setcoords(g,[(x,y*.94 if y<0 else y)for x,y in g.coordinates])
  for char,pct in {'s':-.02,'o':-.01,'O':-.005,'t':.04}.items():n=cm[ord(char)];a,l=f['hmtx'][n];f['hmtx'][n]=(round(a*(1+pct)),l)
  spacing=.83
 else:
  # Keep genuine italic a/g/r/t constructions. Redraw only the tail of italic Q.
  g=glyf[cm[ord('Q')]];cs=contours(g);base=TTFont(ROOT/'sources/family/STIXTwoText-Italic-400.ttf')['glyf']['Q'];weighted=TTFont(ROOT/f'sources/family/STIXTwoText-Italic-{w}.ttf')['glyf']['Q']
  tail=[(550,-190,1),(445,-190,1),(285,18,1),(385,28,1),(550,-164,1)]
  out=[]
  for x,y,flag in tail:
   x,y=displace_point((x,y),base.coordinates,weighted.coordinates);out.append((round(x+slope*y),round(y*1.03 if y>0 else y),flag))
  cs[1]=out;setcontours(g,cs)
  for char,pct in {'a':-.015,'e':-.015,'r':.025,'t':.025,'g':.02}.items():width(char,pct)
  # Replace the italic f hook with a sloped descender on every contextual f form.
  raw=TTFont(ROOT/f'sources/family/STIXTwoText-Italic-{w}.ttf');regular=TTFont(ROOT/'sources/family/STIXTwoText-Italic-400.ttf')
  for n in ['f','f._f','f._ij','f._asc']:
   g=deepcopy(raw['glyf'][n]);cs=contours(g);b=regular['glyf'][n];t=raw['glyf'][n]
   ends=[displace_point(pt,b.coordinates,t.coordinates)for pt in [(5,-215),(88,-185)]]
   cs[0]=[(round(ends[0][0]),round(ends[0][1]),1)]+cs[0][17:-5]+[(round(ends[1][0]),round(ends[1][1]),1)]
   setcontours(g,cs);setcoords(g,[(x+slope*y,y+max(0,y-f['OS/2'].sxHeight)*.06)for x,y in g.coordinates]);glyf[n]=g
  for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
   n=cm[ord(char)];a,l=f['hmtx'][n];f['hmtx'][n]=(round(a*.99),l)
  spacing=.76
  addkern(f,[('Q','j',25),('r','w',15),('v','t',15)])
 for c in [' ','\u00a0']:
  if ord(c)in cm:
   n=cm[ord(c)];a,l=oldmetrics[n];f['hmtx'][n]=(round(a*spacing),l)
 if kind=='Serif':
  # Weight-specific italic fitting: adjust in desheared coordinates to retain the slant.
  ink={400:.985,500:.984,600:.980,700:.975}[w];fit={400:.985,500:.984,600:.977,700:.970}[w];slant=math.tan(math.radians(angle))
  for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
   n=cm[ord(char)];g=glyf[n]
   if not g.isComposite():
    vals=[x-slant*y for x,y in g.coordinates];lo,hi=min(vals),max(vals);delta=(hi-lo)*(ink-1)
    coords=[]
    for x,y in g.coordinates:
     u=x-slant*y;t=max(0,min(1,(u-lo)/(hi-lo)))if hi>lo else .5;coords.append((x+delta*(t*t*(3-2*t)-.5),y))
    setcoords(g,coords)
   a,l=f['hmtx'][n];f['hmtx'][n]=(round(a*fit),l)
  for char in [' ','\u00a0']:
   if ord(char)in cm:n=cm[ord(char)];a,l=f['hmtx'][n];f['hmtx'][n]=(round(a*.95),l)
 # Synchronize canonical accented advances with any edited base advance.
 for code,n in cm.items():
  dec=unicodedata.normalize('NFD',chr(code))
  if len(dec)>1 and ord(dec[0])in cm:
   bn=cm[ord(dec[0])];delta=f['hmtx'][bn][0]-oldmetrics[bn][0]
   if glyf[n].isComposite():a,l=oldmetrics[n];f['hmtx'][n]=(a+delta,l)
 f['post'].italicAngle=-angle;f['hhea'].caretSlopeRise=1000;f['hhea'].caretSlopeRun=round(math.tan(math.radians(angle))*1000);f['hhea'].caretOffset=0
 return f

def finish(f,kind,w,isitalic):
 family='Proof '+kind;weight=WEIGHTS[w];style=('Italic'if w==400 else weight+' Italic')if isitalic else weight
 legacyfamily=family if w in [400,700]else family+' '+weight
 legacystyle=('Bold Italic'if isitalic else'Bold')if w==700 else('Italic'if isitalic else'Regular')
 ps='Proof'+kind+'-'+style.replace(' ','');licence=(ROOT/f'prototypes/Proof{kind}-OFL.txt').read_text()
 replacements={1:legacyfamily,2:legacystyle,3:ps+'-0.200',4:family+' '+style,5:'Version 0.200; family proof',6:ps,13:licence,14:'https://openfontlicense.org/',16:family,17:style}
 f['name'].names=[n for n in f['name'].names if n.nameID not in set(replacements)|{21,22}]
 for i,v in replacements.items():f['name'].setName(v,i,3,1,0x409)
 f['OS/2'].usWeightClass=w;f['OS/2'].fsSelection&=~(1|32|64|512);f['OS/2'].fsSelection|=(1 if isitalic else 0)|(32 if w==700 else 0)|(64 if not isitalic and w!=700 else 0)
 f['head'].macStyle=(1 if w==700 else 0)|(2 if isitalic else 0);f['head'].fontRevision=.200;f['head'].flags&=~16
 for n in f.getGlyphOrder():
  g=f['glyf'][n];g.removeHinting();g.recalcBounds(f['glyf'])
  if g.numberOfContours!=0:a,_=f['hmtx'][n];f['hmtx'][n]=(a,g.xMin)
 for tag in ['prep','fpgm','cvt ','hdmx','LTSH','STAT']:
  if tag in f:del f[tag]
 if'gasp'in f:f['gasp'].gaspRange={65535:10}
 path=OUT/(ps+'.ttf');f.save(path)
 return {'file':path.name,'family':family,'style':style,'weight':w,'italic':isitalic,'glyphs':len(f.getGlyphOrder()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
manifest=[]
for kind in ['Sans','Serif']:
 for w in WEIGHTS:
  roman=upright(kind,w);it=italic(kind,w,roman)
  for f,isit in [(roman,False),(it,True)]:
   item=finish(f,kind,w,isit);manifest.append(item);print(item['file'],flush=True)
 shutil.copyfile(ROOT/f'prototypes/Proof{kind}-OFL.txt',OUT/f'Proof{kind}-OFL.txt')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
