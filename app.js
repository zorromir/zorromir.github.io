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
    // Old technical-section bookmarks now point to the concise industrial summary.
    const projectAnchors = {
      'empirical-heading': 'empirical-heading',
      'panel-simulation-heading': 'panel-simulation-heading',
      'yield-curve-heading': 'yield-curve-heading',
      'industrial-project-title': 'industrial-project-title',
      'industrial-detail': 'industrial-project-title',
      'industrial-model-stages': 'industrial-project-title',
      'industrial-numerical-figures': 'industrial-project-title'
    };
    const detailTarget = Object.prototype.hasOwnProperty.call(projectAnchors, hash)
      ? document.getElementById(projectAnchors[hash]) : null;
    const researchTarget = hash === 'research-thesis-title' ? document.getElementById('research-thesis-title') : null;
    const name = researchTarget ? 'research' : (detailTarget ? 'projects' : (hash === 'main-content' ? currentPage : (hash === 'cv' ? 'about' : (validPages.has(hash) ? hash : 'home'))));
    const changed = name !== currentPage;
    currentPage = name;
    document.body.classList.toggle('is-projects-page', name === 'projects');

    pages.forEach(page => { page.hidden = page.dataset.page !== name; });
    links.forEach(link => {
      const active = link.dataset.nav === name;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });

    closeMenu();
    if (detailTarget || researchTarget) {
      const heading = detailTarget || researchTarget;
      const destination = heading.closest('.project-paper-entry, .academic-research-thesis') || heading;
      requestAnimationFrame(() => {
        requestAnimationFrame(() => destination.scrollIntoView({ block: 'start', behavior: 'instant' }));
      });
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

})();
