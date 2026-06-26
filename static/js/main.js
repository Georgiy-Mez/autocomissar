// АварКомиссар Приморье — main.js

document.addEventListener('DOMContentLoaded', function () {

  // ---- ПРИНУДИТЕЛЬНОЕ ЗАКРЫТИЕ DROPDOWN ----
  document.querySelectorAll('.dropdown').forEach(function (el) {
    el.style.display = 'none';
  });
  document.querySelectorAll('.has-dropdown').forEach(function (el) {
    el.classList.remove('open');
  });

  // ---- BURGER MENU ----
  const burger = document.getElementById('burger');
  const nav = document.getElementById('main-nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  // ---- MODAL ----
  const overlay = document.getElementById('modal-overlay');
  const modalClose = document.getElementById('modal-close');

  function openModal() {
    if (overlay) { overlay.classList.add('active'); document.body.style.overflow = 'hidden'; }
  }
  function closeModal() {
    if (overlay) { overlay.classList.remove('active'); document.body.style.overflow = ''; }
  }

  document.querySelectorAll('.open-modal').forEach(function (btn) {
    btn.addEventListener('click', openModal);
  });
  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (overlay) overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  // ---- MAIN MODAL FORM ----
  var reqForm = document.getElementById('request-form');
  var formSuccess = document.getElementById('form-success');
  if (reqForm) {
    reqForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validateForm(reqForm)) return;
      var data = {
        name: reqForm.querySelector('[name=name]').value,
        phone: reqForm.querySelector('[name=phone]').value,
        service: reqForm.querySelector('[name=service]') ? reqForm.querySelector('[name=service]').value : '',
        city: reqForm.querySelector('[name=city]') ? reqForm.querySelector('[name=city]').value : '',
        message: reqForm.querySelector('[name=message]') ? reqForm.querySelector('[name=message]').value : '',
        consent: reqForm.querySelector('[name=consent]') ? reqForm.querySelector('[name=consent]').checked : false,
        marketing: reqForm.querySelector('[name=marketing]') ? reqForm.querySelector('[name=marketing]').checked : false
      };
      if (!data.consent) { alert('Необходимо согласие на обработку персональных данных.'); return; }
      submitRequest(data, function () {
        reqForm.style.display = 'none';
        if (formSuccess) { formSuccess.hidden = false; }
      });
    });
  }

  // ---- CONTACT PAGE FORM ----
  var cpForm = document.getElementById('contact-page-form');
  var cpSuccess = document.getElementById('cp-success');
  if (cpForm) {
    cpForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validateForm(cpForm)) return;
      var data = {
        name: cpForm.querySelector('[name=name]').value,
        phone: cpForm.querySelector('[name=phone]').value,
        service: cpForm.querySelector('[name=service]') ? cpForm.querySelector('[name=service]').value : '',
        city: cpForm.querySelector('[name=city]') ? cpForm.querySelector('[name=city]').value : '',
        message: cpForm.querySelector('[name=message]') ? cpForm.querySelector('[name=message]').value : '',
        consent: cpForm.querySelector('[name=consent]') ? cpForm.querySelector('[name=consent]').checked : true,
        marketing: cpForm.querySelector('[name=marketing]') ? cpForm.querySelector('[name=marketing]').checked : false
      };
      if (!data.consent) { alert('Необходимо согласие на обработку персональных данных.'); return; }
      submitRequest(data, function () {
        cpForm.style.display = 'none';
        if (cpSuccess) { cpSuccess.hidden = false; }
      });
    });
  }

  // Статическая версия сайта: заявка уходит менеджеру в WhatsApp
  // (на GitHub Pages нет бэкенда). Чтобы поменять номер — измените WA_NUMBER.
  var WA_NUMBER = '79673888889';
  function submitRequest(data, onSuccess) {
    var lines = ['Здравствуйте! Заявка с сайта komissar125.ru:'];
    if (data.name) lines.push('Имя: ' + data.name);
    if (data.phone) lines.push('Телефон: ' + data.phone);
    if (data.service) lines.push('Услуга: ' + data.service);
    if (data.city) lines.push('Город: ' + data.city);
    if (data.message) lines.push('Сообщение: ' + data.message);
    lines.push('Согласие на рекламную рассылку: ' + (data.marketing ? 'да' : 'нет'));
    var url = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
    if (window.ymGoal) { window.ymGoal('lead_form'); }
    window.open(url, '_blank');
    if (typeof onSuccess === 'function') onSuccess();
  }

  function validateForm(form) {
    var valid = true;
    form.querySelectorAll('[required]').forEach(function (field) {
      field.classList.remove('error');
      if (!field.value.trim()) { field.classList.add('error'); valid = false; }
    });
    var phoneField = form.querySelector('[name=phone]');
    if (phoneField && phoneField.value.trim()) {
      var digits = phoneField.value.replace(/\D/g, '');
      if (digits.length < 10) { phoneField.classList.add('error'); valid = false; }
    }
    return valid;
  }

  // ---- PHONE MASK ----
  document.querySelectorAll('input[type=tel]').forEach(function (input) {
    input.addEventListener('input', function () {
      var val = this.value.replace(/\D/g, '');
      if (val.startsWith('7') || val.startsWith('8')) val = val.slice(1);
      var result = '+7';
      if (val.length > 0) result += ' (' + val.slice(0, 3);
      if (val.length >= 3) result += ') ' + val.slice(3, 6);
      if (val.length >= 6) result += '-' + val.slice(6, 8);
      if (val.length >= 8) result += '-' + val.slice(8, 10);
      this.value = result;
    });
  });

  // ---- FAQ ----
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var answer = this.nextElementSibling;
      var expanded = this.getAttribute('aria-expanded') === 'true';
      // Close all others
      document.querySelectorAll('.faq-question').forEach(function (q) {
        q.setAttribute('aria-expanded', 'false');
        if (q.nextElementSibling) q.nextElementSibling.hidden = true;
      });
      if (!expanded) {
        this.setAttribute('aria-expanded', 'true');
        answer.hidden = false;
      }
    });
  });

  // ---- DROPDOWN по клику ----
  document.querySelectorAll('.has-dropdown').forEach(function (li) {
    var link = li.querySelector('a');
    var dropdown = li.querySelector('.dropdown');
    if (!link || !dropdown) return;
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = li.classList.contains('open');
      document.querySelectorAll('.has-dropdown.open').forEach(function (el) { el.classList.remove('open'); });
      if (!isOpen) li.classList.add('open');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-dropdown')) {
      document.querySelectorAll('.has-dropdown.open').forEach(function (el) { el.classList.remove('open'); });
    }
  });

  // ---- ЯНДЕКС.МЕТРИКА (грузится только после согласия на cookie) ----
  // ВАЖНО: впишите номер своего счётчика вместо 00000000
  var METRIKA_ID = 00000000;
  var metrikaLoaded = false;
  function loadMetrika() {
    if (metrikaLoaded || !METRIKA_ID || METRIKA_ID === 0) return;
    metrikaLoaded = true;
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < e.scripts.length; j++) { if (e.scripts[j].src === r) { return; } }
      k = e.createElement(t); a = e.getElementsByTagName(t)[0];
      k.async = 1; k.src = r; a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(METRIKA_ID, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
  }
  // цель: вызывается из submitRequest и обработчиков кликов
  window.ymGoal = function (name) {
    if (window.ym && METRIKA_ID && METRIKA_ID !== 0) { ym(METRIKA_ID, 'reachGoal', name); }
  };

  // ---- COOKIE BANNER (152-ФЗ) ----
  var cookieBanner = document.getElementById('cookie-banner');
  var cookieAccept = document.getElementById('cookie-accept');
  var cookieDecline = document.getElementById('cookie-decline');
  if (cookieBanner && cookieAccept) {
    var hasConsent = document.cookie.split('; ').some(function (c) { return c.indexOf('cookie_consent=1') === 0; });
    try {
      if (!document.cookie.split('; ').some(function (c) { return c.indexOf('cookie_consent=') === 0; })) {
        setTimeout(function () { cookieBanner.classList.add('show'); }, 700);
      } else if (hasConsent) {
        loadMetrika(); // согласие уже дано ранее — грузим Метрику
      }
    } catch (e) { cookieBanner.classList.add('show'); }
    function setConsent(val) {
      var d = new Date();
      d.setTime(d.getTime() + 365 * 24 * 60 * 60 * 1000);
      document.cookie = 'cookie_consent=' + val + '; expires=' + d.toUTCString() + '; path=/; SameSite=Lax';
      cookieBanner.classList.remove('show');
      if (val === '1') { loadMetrika(); }
    }
    cookieAccept.addEventListener('click', function () { setConsent('1'); });
    if (cookieDecline) cookieDecline.addEventListener('click', function () { setConsent('0'); });
  }

  // ---- ЦЕЛИ: клики по телефону и мессенджерам ----
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) { window.ymGoal('phone_click'); }
    else if (href.indexOf('wa.me') !== -1 || href.indexOf('api.whatsapp') !== -1) { window.ymGoal('whatsapp_click'); }
    else if (href.indexOf('t.me') !== -1) { window.ymGoal('telegram_click'); }
  });


  // ---- STICKY HEADER SHADOW ----
  var header = document.getElementById('site-header');
  if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ---- SCROLL ANIMATION ----
  var animateEls = document.querySelectorAll('.service-card, .why-item, .review-card, .city-card, .stat-card, .about-num, .value-item');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'fade-up 0.5s ease forwards';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    animateEls.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      io.observe(el);
    });
  }

});

// CSS keyframe via JS
var style = document.createElement('style');
style.textContent = '@keyframes fade-up { to { opacity: 1; transform: translateY(0); } }';
document.head.appendChild(style);
