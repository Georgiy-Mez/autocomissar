#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавляет в ШАПКУ кнопку вызова с номером (видна на мобиле/планшете, по тапу
набор номера), как на dtp125. Правит main.css один раз, вставляет кнопку во все
страницы и поднимает версию стилей v4->v5. Идемпотентно. Запуск из корня репо."""
from pathlib import Path

root = Path(__file__).resolve().parent
html_files = [p for p in root.rglob("*.html") if "dist" not in p.parts]

BTN = '''<a href="tel:+79673888889" class="header-call" aria-label="Вызвать комиссара" title="Вызвать комиссара 24/7">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>
          <span class="hc-txt"><span class="hc-num">+7 (967) 388-88-89</span><span class="hc-sub">Вызов комиссара 24/7</span></span>
        </a>
        '''
ANCHOR = '<nav class="main-nav" id="main-nav"'

CSS = '''

/* === Кнопка вызова в шапке (мобильная), как на dtp125 === */
.header-call { display: none; }
@media (max-width: 768px) {
  .header-call { display: inline-flex; align-items: center; gap: 7px; margin-left: auto; padding: 7px 11px; background: var(--red); color: #fff; border-radius: 10px; text-decoration: none; line-height: 1.05; flex-shrink: 0; }
  .header-call svg { flex-shrink: 0; }
  .header-call .hc-txt { display: flex; flex-direction: column; }
  .header-call .hc-num { font-size: 13px; font-weight: 800; white-space: nowrap; }
  .header-call .hc-sub { font-size: 8.5px; opacity: .92; text-transform: uppercase; letter-spacing: .2px; white-space: nowrap; }
  .burger { margin-left: 10px; }
  .header-social { display: none !important; }
  .header-mobile-msgs { display: none !important; }
  .logo { min-width: 0; }
  .logo-name-mobile { font-size: 0.78rem !important; }
}
@media (max-width: 360px) {
  .header-call { padding: 6px 9px; }
  .header-call .hc-num { font-size: 12px; }
}
'''

# 1) CSS один раз
css_file = root / "static" / "css" / "main.css"
c = css_file.read_text(encoding="utf-8")
if "Кнопка вызова в шапке" not in c:
    css_file.write_text(c + CSS, encoding="utf-8")
    print("main.css: стили кнопки добавлены")
else:
    print("main.css: стили уже есть")

# 2) кнопка + бамп версии в каждой странице
for f in html_files:
    s = f.read_text(encoding="utf-8")
    ch = False
    if 'class="header-call"' not in s and ANCHOR in s:
        s = s.replace("        " + ANCHOR, BTN + ANCHOR, 1)
        ch = True
    if "main.css?v=4" in s:
        s = s.replace("main.css?v=4", "main.css?v=5")
        ch = True
    if ch:
        f.write_text(s, encoding="utf-8")
        print("  +", f.relative_to(root))

print("Готово.")
