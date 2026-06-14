# АварКомиссар — статическая версия (для GitHub Pages)

Это «замороженная» статическая копия Django-сайта komissar125.ru.
Все страницы отрендерены с реальными данными из базы (настройки, услуги, FAQ),
ссылки и пути к стилям/скриптам сделаны **относительными** — сайт работает на
GitHub Pages по любому адресу (и на `username.github.io/repo/`, и на своём домене).

Папка для публикации — **`dist/`**. Заливать на GitHub нужно **содержимое `dist/`**
(а не саму папку `dist`).

```
dist/
├── index.html                     # главная
├── uslugi/                        # 4 страницы услуг
├── kontakty/  o-kompanii/         # контакты, о компании
├── politika-.../  soglasie-.../   # 4 юридические страницы (152-ФЗ)
├── static/css|js|img/             # стили, скрипт, логотип
├── robots.txt  sitemap.xml        # SEO
├── 404.html                       # страница ошибки
└── .nojekyll                      # отключает обработку Jekyll
```

---

## Деплой на GitHub Pages

### Вариант A — через сайт GitHub (без командной строки)

1. Создай новый репозиторий на github.com (например, `autocomissar`).
2. На странице репозитория → **Add file → Upload files**.
3. Перетащи **всё содержимое папки `dist/`** (открой `dist`, выдели все файлы и папки внутри). Файл `.nojekyll` тоже нужен — если его не видно, включи показ скрытых файлов.
4. **Commit changes**.
5. **Settings → Pages** → Source: `Deploy from a branch` → Branch: `main`, папка `/ (root)` → **Save**.
6. Через 1–2 минуты сайт будет доступен по адресу `https://ТВОЙ_ЛОГИН.github.io/autocomissar/`.

### Вариант B — через git (по одной команде)

```bash
cd dist
```
```bash
git init -b main
```
```bash
git add -A
```
```bash
git commit -m "Static site"
```
```bash
git remote add origin https://github.com/ТВОЙ_ЛОГИН/autocomissar.git
```
```bash
git push -u origin main
```
Затем включи Pages: **Settings → Pages → Branch: main → /(root) → Save**.

---

## Форма заявки

Без сервера БД для приёма заявок нет, поэтому форма настроена на **WhatsApp**:
клиент заполняет поля → жмёт «Отправить» → открывается WhatsApp с уже готовым
текстом заявки → он отправляет, и заявка приходит тебе.

**Сменить номер получателя:** `static/js/main.js`, строка
```js
var WHATSAPP_NUMBER = '79673888889';
```

**Хочешь заявки на e-mail вместо WhatsApp** — подключи бесплатный Formspree:
1. Зарегистрируйся на formspree.io, создай форму, получи ID вида `xxxxbbbb`.
2. В `static/js/main.js` замени тело функции `submitRequest` на:
```js
function submitRequest(data, onSuccess) {
  fetch('https://formspree.io/f/ТВОЙ_ID', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(data)
  }).then(function(r){ if (r.ok) onSuccess(); })
    .catch(function(){ alert('Ошибка отправки. Позвоните нам.'); });
}
```

---

## Свой домен (komissar125.ru) — опционально

Если будешь привязывать домен к GitHub Pages:
1. Создай файл `CNAME` (без расширения) в корне опубликованных файлов с одной строкой:
   ```
   komissar125.ru
   ```
2. В DNS домена добавь записи на GitHub Pages (4 A-записи на 185.199.108–111.153
   и CNAME `www` → `ТВОЙ_ЛОГИН.github.io`).
3. **Settings → Pages → Custom domain** → `komissar125.ru` → Save → включи Enforce HTTPS.

`sitemap.xml`, `robots.txt` и canonical-ссылки уже указывают на `https://komissar125.ru`.
Если домен другой — поменяй их.

---

## Что НЕ переехало (и почему)

GitHub Pages отдаёт только статику, без Python. Поэтому **не работают** серверные части:
- админ-панель Django (`/admin/`) и CMS (`/panel/`);
- сохранение заявок в базу (заменено на WhatsApp/Formspree).

Контент (услуги, FAQ, тексты, контакты) уже «вшит» в HTML на момент сборки.
Чтобы изменить тексты — правь готовые `*.html`, либо отредактируй данные в исходном
Django-проекте и пересобери статику скриптом `build_static.py`.
