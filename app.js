(() => {
  const validPages = new Set(['home','projects','research','engineering','about','cv']);
  const pages = [...document.querySelectorAll('[data-page]')];
  const links = [...document.querySelectorAll('[data-nav]')];
  const menu = document.getElementById('main-nav');
  const menuBtn = document.getElementById('menu-toggle');
  const notesBtn = document.getElementById('notes-toggle');

  const renderPage = () => {
    const requested = location.hash.replace(/^#/, '');
    if (requested === 'main-content') return;
    const name = validPages.has(requested) ? requested : 'home';
    pages.forEach(page => page.hidden = page.dataset.page !== name);
    links.forEach(link => {
      const active = link.dataset.nav === name;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    menu.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.innerHTML = 'Menu <span aria-hidden="true">☰</span>';
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.title = `${name === 'home' ? 'Home' : name[0].toUpperCase() + name.slice(1)} — Kelvin Schouten · Wireframes`;
  };
  window.addEventListener('hashchange', renderPage);
  renderPage();

  menuBtn.addEventListener('click', () => {
    const active = menu.classList.toggle('is-open');
    menuBtn.setAttribute('aria-expanded', String(active));
    menuBtn.innerHTML = active ? 'Close <span aria-hidden="true">×</span>' : 'Menu <span aria-hidden="true">☰</span>';
  });
  document.addEventListener('keydown', ev => { if(ev.key === 'Escape') { menu.classList.remove('is-open'); menuBtn.setAttribute('aria-expanded','false'); }});

  notesBtn.addEventListener('click', () => {
    const hidden = document.body.classList.toggle('hide-notes');
    notesBtn.setAttribute('aria-pressed', String(!hidden));
    notesBtn.innerHTML = `${hidden ? 'Show' : 'Hide'} layout notes <span>↗</span>`;
  });
})();
