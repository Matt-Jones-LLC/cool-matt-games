/* Shared behaviour for every page: the light/dark switch. The saved choice is applied by a
   one-line script in each page's <head> so there is no flash; this file wires up the button. */
(function () {
  var root = document.documentElement;
  function current() {
    return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.theme');
    if (!btn) return;
    function label() { btn.setAttribute('aria-label', 'Switch to ' + (current() === 'dark' ? 'light' : 'dark') + ' colours'); }
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('mj-theme', next); } catch (e) {}
      label();
      document.dispatchEvent(new CustomEvent('mj-theme', { detail: next }));
    });
    label();
  });
})();
