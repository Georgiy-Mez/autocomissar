#!/usr/bin/env python3
"""Заменяет ранее вставленный блок Яндекс.Метрики на актуальный код
из личного кабинета (счётчик 107049587) во всех статических HTML-страницах."""
import re
from pathlib import Path

COUNTER_ID = 107049587

NEW_SNIPPET = f'''  <!-- Yandex.Metrika counter -->
  <script type="text/javascript">
      (function(m,e,t,r,i,k,a){{
          m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
          m[i].l=1*new Date();
          for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
          k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
      }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id={COUNTER_ID}', 'ym');

      ym({COUNTER_ID}, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/{COUNTER_ID}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- /Yandex.Metrika counter -->'''

BLOCK_RE = re.compile(
    r'  <!-- Yandex\.Metrika counter -->.*?<!-- /Yandex\.Metrika counter -->',
    re.DOTALL
)

root = Path(__file__).resolve().parent
html_files = sorted(p for p in root.rglob('*.html') if 'dist' not in p.parts)

updated, not_found = [], []
for f in html_files:
    html = f.read_text(encoding='utf-8')
    html2, n = BLOCK_RE.subn(NEW_SNIPPET, html, count=1)
    if n == 1:
        f.write_text(html2, encoding='utf-8')
        updated.append(f)
    else:
        not_found.append(f)

print(f'Обновлено файлов: {len(updated)}')
for f in updated:
    print(f'   ~ {f.relative_to(root)}')
if not_found:
    print(f'Блок не найден (не тронуты): {len(not_found)}')
    for f in not_found:
        print(f'   ? {f.relative_to(root)}')
