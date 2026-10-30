from pathlib import Path
import urllib.request,urllib.parse,re,concurrent.futures
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
p=Path(__file__).parent
jobs=[(family,italic,w)for family in ['Inter','STIX Two Text']for italic in [False,True]for w in [400,500,600,700]]
def get(job):
 family,italic,w=job;stem=family.replace(' ','')+('-Italic'if italic else '-Roman')+'-'+str(w);dest=p/(stem+'.ttf')
 if not dest.exists():
  url='https://fonts.googleapis.com/css2?family='+urllib.parse.quote(family)+':ital,wght@'+str(int(italic))+','+str(w)
  css=urllib.request.urlopen(url).read().decode();url=re.search(r'url\((.*?)\)',css).group(1);urllib.request.urlretrieve(url,dest)
 f=TTFont(dest)
 if 'fvar' in f:
  f=instantiateVariableFont(f,{a.axisTag:w if a.axisTag=='wght' else a.defaultValue for a in f['fvar'].axes},inplace=False);f.save(dest)
 return stem,len(f.getGlyphOrder()),f['name'].getDebugName(5),f['head'].unitsPerEm,f['post'].italicAngle
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
 for r in pool.map(get,jobs):print(r,flush=True)
