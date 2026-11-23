import json
from pathlib import Path
r=Path(__file__).parent
data=json.loads((r/'data.json').read_text(encoding='utf-8'))
source=(r/'site.html').read_text(encoding='utf-8')
source=source.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
(r/'index.html').write_text(source,encoding='utf-8')
print(f"Generated index.html with {len(data['jobs'])} jobs, {len(data['companies'])} firms")
