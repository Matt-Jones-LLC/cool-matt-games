/* Shared behaviour for every page on matt-jones.org:
   theme toggle, mobile menu, current-page highlight, scroll progress, back-to-top. */
(function () {
  var root = document.documentElement;
  var KEY = 'mj-theme';
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  if (stored === 'light' || stored === 'dark') root.setAttribute('data-theme', stored);

  var ICON = {
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    up: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>'
  };

  function button(cls, label, icon) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'mj-tool ' + cls;
    b.setAttribute('aria-label', label); b.innerHTML = icon;
    return b;
  }
  function norm(p) { return p.replace(/index\.html$/, '').replace(/\/?$/, '/'); }

  function init() {
    var bar = document.querySelector('header.bar');
    var wrap = bar && bar.querySelector('.wrap, .bar-wrap');
    var nav = bar && bar.querySelector('nav.top');
    if (getComputedStyle(root).getPropertyValue('--stitch').trim()) root.classList.add('mj-ball');

    /* Skip link for keyboard users */
    var mainEl = document.querySelector('main');
    if (mainEl) {
      if (!mainEl.id) mainEl.id = 'main';
      mainEl.setAttribute('tabindex', '-1');
      var skip = document.createElement('a');
      skip.className = 'mj-skip'; skip.href = '#' + mainEl.id; skip.textContent = 'Skip to content';
      document.body.insertBefore(skip, document.body.firstChild);
    }

    /* Current page */
    var here = norm(location.pathname);
    function markCurrent(scope) {
      scope.querySelectorAll('a[href]').forEach(function (a) {
        var href = a.getAttribute('href');
        if (href.charAt(0) !== '/' || href.indexOf('#') !== -1) return;
        if (norm(href) === here) { a.classList.add('mj-current'); a.setAttribute('aria-current', 'page'); }
      });
    }
    if (nav) markCurrent(nav);

    /* Scroll progress, header shadow, back to top */
    var prog = document.createElement('div');
    prog.className = 'mj-progress'; prog.setAttribute('aria-hidden', 'true');
    document.body.appendChild(prog);
    var top = button('mj-top', 'Back to top', ICON.up);
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    document.body.appendChild(top);
    var ticking = false;
    function onScroll() {
      ticking = false;
      var max = root.scrollHeight - window.innerHeight;
      var y = window.scrollY || 0;
      prog.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
      if (bar) bar.classList.toggle('mj-scrolled', y > 8);
      top.classList.toggle('show', y > 700);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
    }, { passive: true });
    onScroll();

    if (!wrap) return;
    var tools = document.createElement('div');
    tools.className = 'mj-tools';
    wrap.appendChild(tools);

    /* Theme toggle — only where the page's own styles support data-theme */
    var supportsTheme = Array.prototype.some.call(document.querySelectorAll('style'), function (s) {
      return s.textContent.indexOf('data-theme="dark"') !== -1;
    });
    if (supportsTheme) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var isDark = function () {
        var t = root.getAttribute('data-theme');
        return t ? t === 'dark' : mq.matches;
      };
      var tbtn = button('mj-theme', '', '');
      var paint = function () {
        tbtn.innerHTML = isDark() ? ICON.sun : ICON.moon;
        tbtn.setAttribute('aria-label', isDark() ? 'Switch to light theme' : 'Switch to dark theme');
      };
      tbtn.addEventListener('click', function () {
        var next = isDark() ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem(KEY, next); } catch (e) {}
        paint();
        window.dispatchEvent(new Event('mj-themechange'));
      });
      if (mq.addEventListener) mq.addEventListener('change', paint);
      paint();
      tools.appendChild(tbtn);
    }

    /* Mobile menu: built from the page's own nav, shown when that nav is hidden */
    if (!nav) return;
    var drawer = document.createElement('nav');
    drawer.className = 'mj-drawer'; drawer.id = 'mj-drawer';
    drawer.setAttribute('aria-label', 'Menu');
    nav.querySelectorAll('a[href]').forEach(function (a) {
      var c = document.createElement('a');
      c.href = a.getAttribute('href');
      c.textContent = a.textContent.replace('▾', '').trim();
      if (a.closest('.menu-list')) c.className = 'mj-sub';
      drawer.appendChild(c);
    });
    markCurrent(drawer);
    document.body.appendChild(drawer);

    var burger = button('mj-burger', 'Open menu', ICON.menu);
    burger.setAttribute('aria-controls', 'mj-drawer');
    burger.setAttribute('aria-expanded', 'false');
    tools.appendChild(burger);
    function setOpen(open) {
      drawer.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      burger.innerHTML = open ? ICON.close : ICON.menu;
    }
    burger.addEventListener('click', function () { setOpen(!drawer.classList.contains('open')); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) { setOpen(false); burger.focus(); }
    });
    var probe = nav.querySelector('a:not(.pill)') || nav;
    function fit() {
      var hidden = getComputedStyle(nav).display === 'none' || getComputedStyle(probe).display === 'none';
      root.classList.toggle('mj-compact', hidden);
      if (!hidden) setOpen(false);
      drawer.style.top = bar.getBoundingClientRect().height + 'px';
    }
    window.addEventListener('resize', fit);
    fit();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
