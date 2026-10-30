"""Local contour construction on OFL proofs; never reads Klim font files."""
from pathlib import Path
from array import array
import hashlib,json,shutil,unicodedata
from fontTools.otlLib.builder import buildPairPosGlyphsSubtable,buildLookup,buildValue
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'v0.103';OUT.mkdir(exist_ok=True)
def contours(g):
 result=[];start=0
 for end in g.endPtsOfContours:
  result.append([(int(g.coordinates[i][0]),int(g.coordinates[i][1]),int(g.flags[i])&1)for i in range(start,end+1)]);start=end+1
 return result
def set_contours(g,cs):
 g.coordinates=GlyphCoordinates([(x,y)for c in cs for x,y,flag in c]);g.flags=array('B',[flag for c in cs for x,y,flag in c]);g.endPtsOfContours=[];n=0
 for c in cs:n+=len(c);g.endPtsOfContours.append(n-1)
 g.numberOfContours=len(cs);g.removeHinting()
manifest=[]
for kind in ['Sans','Serif']:
 source=ROOT/'v0.102'/f'Proof{kind}-Regular.ttf';f=TTFont(source);glyf=f['glyf'];changes=[];deltas={}
 def points(char,updates):
  g=glyf[char]
  for i,p in updates.items():g.coordinates[i]=p
 if kind=='Sans':
  # Retain a's bowl and upper arch; construct a curved exit at the stem foot.
  g=glyf['a'];cs=contours(g)
  cs[0]=cs[0][:33]+[(1019,220,1),(1019,142,0),(1064,142,1),(1095,142,0),(1120,147,1),(1120,-4,1),(1072,-18,0),(1025,-18,1),(945,-18,0),(867,18,0),(845,128,1),(837,152,1),(824,152,1)]+cs[0][37:]
  # Restore a deliberate oblique upper terminal and open the shoulder locally.
  cs[0][21]=(286,861,0);cs[0][22]=(270,820,1);cs[0][23]=(93,865,1);cs[0][24]=(135,978,0)
  set_contours(g,cs);deltas['a']=20
  points('g',{2:(306,-345),3:(186,-214),4:(151,-95),5:(297,-30),6:(330,-130),7:(392,-205),8:(513,-268)})
  points('R',{6:(1239,1061),7:(1239,949),8:(1120,755),9:(874,644),10:(689,644),11:(266,644),12:(266,818),13:(680,818),14:(805,818),15:(968,873),16:(1035,985),17:(1035,1061),25:(618,726),26:(845,726)})
  changes=['a: constructed curved exit foot; refined upper aperture and terminal','g: raised hook terminal and reshaped its approach while retaining overall descender depth','R: raised lower bowl junction, moved leg attachment left, refined lower counter']
 else:
  g=glyf['Q'];cs=contours(g)
  cs[1]=[(630,-195,1),(520,-195,1),(306,30,1),(435,38,1),(630,-166,1)]
  set_contours(g,cs)
  # Replace the round r terminal with a drawn shoulder and oblique end.
  g=glyf['r'];cs=contours(g);c=cs[0]
  c[8:17]=[(95,399,0),(85,418,0),(58,430,1),(42,437,0),(26,443,0),(26,443,1),(26,465,1),(174,493,1),(180,493,1)]
  cs[0]=c[:19]+[(218,428,0),(269,483,0),(305,493,0),(324,493,1),(354,493,0),(380,461,0),(389,421,1),(329,388,1),(310,416,0),(284,436,0),(266,430,1),(238,424,0),(201,360,0)]+c[35:]
  set_contours(g,cs)
  points('t',{0:(326,76),1:(326,21),2:(300,3),3:(252,-10),4:(223,-10),5:(197,-10),6:(137,-10),10:(14,426),11:(14,449),16:(173,473),17:(303,473),18:(303,426),22:(194,45),23:(226,45),24:(265,45),25:(299,66)})
  deltas['r']=10;deltas['t']=8
  changes=['Q: replaced curved flourish with an independent diagonal tail and flat termination','r: constructed a sloped head serif, curved shoulder and oblique terminal','t: replaced upturned foot with a curved foot and upright end cut; extended crossbar']
 # Propagate changed advances through composite descendants; drawings inherit their base.
 affected=set('agR' if kind=='Sans' else 'Qrt');propagated=[]
 oldmetrics=dict(f['hmtx'].metrics)
 for name,d in deltas.items():a,l=oldmetrics[name];f['hmtx'][name]=(a+d,l)
 pending=True
 while pending:
  pending=False
  for name in f.getGlyphOrder():
   g=glyf[name]
   if name in affected or not g.isComposite():continue
   bases=[c.glyphName for c in g.components if c.glyphName in affected]
   if len(bases)==1:
    base=bases[0];affected.add(name);propagated.append(name);d=deltas.get(base,0);deltas[name]=d
    a,l=oldmetrics[name];f['hmtx'][name]=(a+d,l);pending=True
 for name in f.getGlyphOrder():
  g=glyf[name];g.removeHinting();g.recalcBounds(glyf)
  if g.numberOfContours!=0:a,_=f['hmtx'][name];f['hmtx'][name]=(a,g.xMin)
 if kind=='Serif':
  # Add narrowly scoped positive kerning after the inherited kerning lookups.
  cm=f.getBestCmap()
  def family(char):return {n for code,n in cm.items() if unicodedata.normalize('NFD',chr(code))[0]==char}
  pairs={}
  for left,right,amount in [('Q','j',20),('r','w',18),('v','t',18)]:
   for a in family(left):
    for b in family(right):pairs[(a,b)]=(buildValue({'XAdvance':amount}),None)
  sub=buildPairPosGlyphsSubtable(pairs,f.getReverseGlyphMap())
  lookup=buildLookup([sub],table='GPOS');table=f['GPOS'].table;index=len(table.LookupList.Lookup)
  table.LookupList.Lookup.append(lookup);table.LookupList.LookupCount=len(table.LookupList.Lookup)
  for record in table.FeatureList.FeatureRecord:
   if record.FeatureTag=='kern':record.Feature.LookupListIndex.append(index);record.Feature.LookupCount=len(record.Feature.LookupListIndex)
  changes.append('Add positive kerning: Qj +20, rw +18, vt +18 font units, including canonical accented equivalents')
 f['head'].fontRevision=.103
 for ident,value in {3:f'Proof{kind}-Regular-0.103',5:'Version 0.103; contour study'}.items():
  f['name'].names=[n for n in f['name'].names if n.nameID!=ident];f['name'].setName(value,ident,3,1,0x409)
 target=OUT/source.name;f.save(target);shutil.copyfile(ROOT/f'Proof{kind}-OFL.txt',OUT/f'Proof{kind}-OFL.txt')
 manifest.append({'font':target.name,'base_version':'0.102','base_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changes':changes,'composite_descendants':propagated,'advance_deltas':deltas})
(OUT/'changes.json').write_text(json.dumps(manifest,indent=2));print('Built contour pass 0.103')
