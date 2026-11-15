(() => {
  'use strict';

  const validPages = new Set(['home', 'projects', 'research', 'engineering', 'about']);
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
    // Preserve bookmarked Projects anchors, including figures inside closed disclosures.
    const projectAnchors = ['empirical-heading', 'industrial-detail', 'industrial-model-stages', 'industrial-numerical-figures'];
    const detailTarget = projectAnchors.includes(hash) ? document.getElementById(hash) : null;
    const name = detailTarget ? 'projects' : (hash === 'main-content' ? currentPage : (hash === 'cv' ? 'about' : (validPages.has(hash) ? hash : 'home')));
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
    if (detailTarget) {
      // First reveal the routed page, then any closed ancestor disclosure,
      // so direct links to project figures remain useful after the redesign.
      const disclosure = detailTarget.closest('details');
      if (disclosure) disclosure.open = true;
      detailTarget.scrollIntoView({ block: 'start', behavior: 'instant' });
    } else if (changed && hash !== 'main-content') {
      window.scrollTo({ top: 0, behavior: 'instant' });
    }
    const label = {home:'Home',projects:'Projects',research:'Research',engineering:'Exploring & Reading',about:'Profile & CV'}[name];
    document.title = name === 'engineering'
      ? 'Exploring & Reading'
      : label === 'Home'
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

  // Independent project carousels: process stages and Python-generated figures.
  // Controls remain available when the surrounding technical disclosure is opened.
  document.querySelectorAll('[data-project-carousel]').forEach(carousel => {
    const track = carousel.querySelector('[data-project-track]');
    const slides = track ? [...track.querySelectorAll('.project-slide')] : [];
    const previous = carousel.querySelector('[data-project-prev]');
    const next = carousel.querySelector('[data-project-next]');
    const counter = carousel.querySelector('[data-project-count]');
    const tabs = [...carousel.querySelectorAll('[data-project-go]')];
    const dotsHost = carousel.querySelector('[data-project-dots]');
    if (!slides.length || !previous || !next || !counter) return;

    let current = 0;
    let touchStart = null;
    carousel.classList.add('is-enhanced');

    if (dotsHost) {
      slides.forEach((slide, index) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.setAttribute('aria-label', 'Show figure ' + (index + 1) + ': ' + slide.getAttribute('aria-label'));
        dot.setAttribute('aria-pressed', String(index === 0));
        dot.addEventListener('click', () => show(index));
        dotsHost.append(dot);
      });
    }

    function show(index) {
      current = (index + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (100 * current) + '%)';
      slides.forEach((slide, i) => {
        const active = i === current;
        slide.setAttribute('aria-hidden', String(!active));
        slide.inert = !active;
      });
      tabs.forEach((tab, i) => {
        const active = i === current;
        tab.classList.toggle('is-active', active);
        tab.setAttribute('aria-pressed', String(active));
      });
      if (dotsHost) {
        [...dotsHost.children].forEach((dot, i) => {
          dot.classList.toggle('is-active', i === current);
          dot.setAttribute('aria-pressed', String(i === current));
        });
      }
      counter.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    }

    const hasMultiple = slides.length > 1;
    previous.disabled = next.disabled = !hasMultiple;
    previous.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current + 1));
    tabs.forEach(tab => {
      const target = Number(tab.dataset.projectGo);
      if (Number.isInteger(target) && target >= 0 && target < slides.length) {
        tab.addEventListener('click', () => show(target));
      }
    });
    carousel.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (event.target.closest('a, button, input, select, textarea')) return;
      event.preventDefault();
      show(current + (event.key === 'ArrowRight' ? 1 : -1));
    });
    const viewport = carousel.querySelector('.project-viewport');
    if (viewport) {
      viewport.addEventListener('touchstart', event => {
        if (event.touches.length === 1) {
          touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
        }
      }, { passive: true });
      viewport.addEventListener('touchend', event => {
        if (!touchStart || !event.changedTouches.length) return;
        const dx = event.changedTouches[0].clientX - touchStart.x;
        const dy = event.changedTouches[0].clientY - touchStart.y;
        touchStart = null;
        if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.2) {
          show(current + (dx < 0 ? 1 : -1));
        }
      }, { passive: true });
      viewport.addEventListener('touchcancel', () => { touchStart = null; }, { passive: true });
    }
    show(0);
  });



})();