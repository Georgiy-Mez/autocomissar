#!/usr/bin/env python3
"""Вставляет код счётчика Яндекс.Метрики (ID 107049587) перед </head>
во все статические HTML-страницы сайта (кроме dist/, она генерируется
build_static.py и не публикуется напрямую)."""
import re
from pathlib import Path

COUNTER_ID = 107049587

SNIPPET = f'''  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
     (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
     m[i].l=1*new Date();
     for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
     k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})
     (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

     ym({COUNTER_ID}, "init", {{
          clickmap:true,
          trackLinks:true,
          accurateTrackBounce:true,
          webvisor:true
     }});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/{COUNTER_ID}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->
'''

root = Path(__file__).resolve().parent
html_files = sorted(p for p in root.rglob('*.html') if 'dist' not in p.parts)

changed, skipped = [], []
for f in html_files:
    html = f.read_text(encoding='utf-8')
    if f'ym({COUNTER_ID}' in html:
        skipped.append(f)
        continue
    if '</head>' not in html:
        print(f'  ПРОПУЩЕН (нет </head>): {f}')
        continue
    html2 = html.replace('</head>', SNIPPET + '</head>', 1)
    f.write_text(html2, encoding='utf-8')
    changed.append(f)

print(f'Обновлено файлов: {len(changed)}')
for f in changed:
    print(f'   + {f.relative_to(root)}')
if skipped:
    print(f'Уже содержали счётчик (пропущены): {len(skipped)}')
    for f in skipped:
        print(f'   = {f.relative_to(root)}')
