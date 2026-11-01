(() => {
  'use strict';
  const validPages = new Set(['home', 'projects', 'research', 'engineering', 'about', 'cv']);
  const pages = [...document.querySelectorAll('[data-page]')];
  const links = [...document.querySelectorAll('[data-nav]')];
  const menu = document.getElementById('main-nav');
  const menuBtn = document.getElementById('menu-toggle');
  const main = document.getElementById('main-content');
  const skip = document.querySelector('.skip');
  let currentPage = 'home';

  // Page selection must run even when the URL is #main-content.
  // That fragment is reserved for the accessible skip link, not for a seventh page.
  function renderPage() {
    const hash = location.hash.slice(1);
    const name = hash === 'main-content' ? currentPage : (validPages.has(hash) ? hash : 'home');
    const changed = name !== currentPage;
    currentPage = name;

    pages.forEach(page => { page.hidden = page.dataset.page !== name; });
    links.forEach(link => {
      const active = link.dataset.nav === name;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });

    closeMenu();
    if (changed && hash !== 'main-content') window.scrollTo({ top: 0, behavior: 'instant' });
    const label = {home:'Home',projects:'Projects',research:'Research',engineering:'Now & Reading',about:'About',cv:'CV & Contact'}[name];
    document.title = label === 'Home'
      ? 'Kelvin Schouten | Quantitative Finance & Mathematical Modelling'
      : label + ' | Kelvin Schouten';
  }

  function closeMenu() {
    if (!menu || !menuBtn) return;
    menu.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.innerHTML = 'Menu <span aria-hidden="true">☰</span>';
  }

  window.addEventListener('hashchange', renderPage);
  renderPage();

  if (menu && menuBtn) {
    menuBtn.addEventListener('click', () => {
      const open = menu.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.innerHTML = open ? 'Close <span aria-hidden="true">×</span>' : 'Menu <span aria-hidden="true">☰</span>';
    });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', ev => {
      if (ev.key === 'Escape') closeMenu();
    });
  }

  // Preserve the selected page while allowing keyboard users to skip the header.
  if (skip && main) {
    main.setAttribute('tabindex', '-1');
    skip.addEventListener('click', ev => {
      ev.preventDefault();
      main.focus({ preventScroll: false });
    });
  }

  // Selected research shelf. All cards remain static HTML so paper links work without JavaScript.
  const carousel = document.querySelector('[data-paper-carousel]');
  if (carousel) {
    const track = carousel.querySelector('[data-paper-track]');
    const slides = [...carousel.querySelectorAll('.reading-slide')];
    const counter = carousel.querySelector('[data-paper-count]');
    const dots = [...carousel.querySelectorAll('[data-paper-dot]')];
    const prev = carousel.querySelector('[data-paper-prev]');
    const next = carousel.querySelector('[data-paper-next]');
    let current = 0;
    let touchStart = null;
    function showPaper(index) {
      if (!slides.length) return;
      current = (index + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + current * 100 + '%)';
      slides.forEach((slide, i) => {
        const selected = i === current;
        slide.setAttribute('aria-hidden', String(!selected));
        slide.querySelectorAll('a, button').forEach(el => { el.tabIndex = selected ? 0 : -1; });
      });
      dots.forEach((dot, i) => {
        dot.classList.toggle('is-active', i === current);
        dot.setAttribute('aria-pressed', String(i === current));
      });
      counter.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    }
    prev.addEventListener('click', () => showPaper(current - 1));
    next.addEventListener('click', () => showPaper(current + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => showPaper(i)));
    carousel.addEventListener('keydown', ev => {
      if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
        ev.preventDefault();
        showPaper(current + (ev.key === 'ArrowRight' ? 1 : -1));
      }
    });
    carousel.addEventListener('touchstart', ev => {
      if (ev.touches.length === 1) touchStart = ev.touches[0].clientX;
    }, { passive: true });
    carousel.addEventListener('touchend', ev => {
      if (touchStart === null || !ev.changedTouches.length) return;
      const delta = ev.changedTouches[0].clientX - touchStart;
      touchStart = null;
      if (Math.abs(delta) > 55) showPaper(current + (delta < 0 ? 1 : -1));
    }, { passive: true });
    showPaper(0);
  }

})();