"""Apply the audited pair repairs to canonical accented equivalents too."""
from pathlib import Path
import json,unicodedata,hashlib
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildPairPosGlyphsSubtable,buildLookup,buildValue
p=Path(__file__).resolve().parent/'v0.200';records=json.loads((p/'spacing-validation.json').read_text())
for rec in records:
 if rec.get('accent_equivalents_expanded'):continue
 f=TTFont(p/rec['file']);cm=f.getBestCmap();mapping={}
 def fam(c):return {n for code,n in cm.items() if unicodedata.normalize('NFD',chr(code))[0]==c}
 existing={tuple(r['glyphs'])for r in rec['repairs']}
 for repair in rec['repairs']:
  a,b=repair['pair']
  for left in fam(a):
   for right in fam(b):
    if (left,right)not in existing:mapping[(left,right)]=(buildValue({'XAdvance':repair['units']}),None)
 if mapping:
  t=f['GPOS'].table;i=len(t.LookupList.Lookup);t.LookupList.Lookup.append(buildLookup([buildPairPosGlyphsSubtable(mapping,f.getReverseGlyphMap())],table='GPOS'));t.LookupList.LookupCount=len(t.LookupList.Lookup)
  for r in t.FeatureList.FeatureRecord:
   if r.FeatureTag=='kern':r.Feature.LookupListIndex.append(i);r.Feature.LookupCount=len(r.Feature.LookupListIndex)
  f.save(p/rec['file'])
 rec['accent_equivalents_expanded']=len(mapping)
(p/'spacing-validation.json').write_text(json.dumps(records,indent=2))
m=json.loads((p/'manifest.json').read_text())
for item in m:item['sha256']=hashlib.sha256((p/item['file']).read_bytes()).hexdigest()
(p/'manifest.json').write_text(json.dumps(m,indent=2))
print('Expanded corrections to accented equivalents.')
