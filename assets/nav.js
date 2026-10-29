/* Mobile nav toggle. Shared by every page, including index.html, which
   keeps its own inline script for the hero animations; the two do not
   touch the same state.

   The panel is the SAME .nav-links element the desktop nav uses. Below
   940px CSS repositions it as a dropdown instead of an inline row, so
   there is no duplicate mobile list to keep in step with the first one.

   Without JS the panel stays closed and the four links are unreachable on
   a phone, which is why the toggle button is the only thing added to the
   markup: no JS also means no button, so nothing renders that cannot work. */
(function () {
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  var panel = document.querySelector('.nav-links');
  if (!nav || !toggle || !panel) return;

  function setOpen(on) {
    nav.classList.toggle('menu-open', on);
    toggle.setAttribute('aria-expanded', on ? 'true' : 'false');
  }

  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  // A tapped link has to close the panel itself. The homepage links are
  // same-page anchors, which never reload, so the panel would otherwise
  // stay open covering the section the reader just jumped to.
  panel.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });

  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target)) setOpen(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });

  // Rotating to landscape past 940px with the panel open would strand
  // menu-open on a desktop nav, where the dropdown rules no longer apply
  // and the class would silently do nothing until the next tap.
  var wide = window.matchMedia('(min-width: 940px)');
  function sync() { if (wide.matches) setOpen(false); }
  if (wide.addEventListener) wide.addEventListener('change', sync);
  else wide.addListener(sync);
})();
