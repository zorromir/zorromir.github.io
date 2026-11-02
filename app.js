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
    const name = hash === 'main-content' ? currentPage : (hash === 'cv' ? 'about' : (validPages.has(hash) ? hash : 'home'));
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
    const label = {home:'Home',projects:'Projects',research:'Research',engineering:'Exploring & Reading',about:'Profile & CV'}[name];
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

  // Independent project carousels: process stages and Python-generated figures.
  // Static HTML keeps the content accessible and available without external data.
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

  // Current readings appear beside their exploration topics; this searchable shelf holds the remaining references.
  // The HTML contains a usable bibliography if JavaScript or the JSON fetch fails.
  // data/reading-list.json remains the maintained source for enhanced entries.
  const library = document.querySelector('[data-paper-library]');
  if (library) {
    const list = library.querySelector('[data-paper-list]');
    const filters = library.querySelector('[data-paper-filters]');
    const fallback = library.querySelector('[data-paper-fallback]');
    const counter = library.querySelector('[data-paper-count]');
    const collectionNote = library.querySelector('[data-paper-collection-note]');

    function node(tag, className, text) {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text !== undefined) el.textContent = String(text);
      return el;
    }

    function safeUrl(value, allowHash = false) {
      if (typeof value !== 'string') return null;
      if (allowHash && /^#[a-z0-9-]+$/i.test(value)) return value;
      try {
        const url = new URL(value);
        return url.protocol === 'https:' ? url.href : null;
      } catch (_) { return null; }
    }

    function paperLink(text, url, className) {
      const href = safeUrl(url, true);
      if (!href) return null;
      const a = node('a', className, text);
      a.href = href;
      if (!href.startsWith('#')) {
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
      }
      return a;
    }

    function validData(data) {
      if (!data || !Array.isArray(data.papers) || !Array.isArray(data.categories) || !Array.isArray(data.projects)) return false;
      const ids = new Set();
      const categories = new Set(data.categories.map(c => c.id));
      const projects = new Set(data.projects.map(p => p.id));
      if (!categories.has('all')) return false;
      return data.papers.every(p => {
        if (!p || typeof p.id !== 'string' || ids.has(p.id)) return false;
        ids.add(p.id);
        return ['title','authors','topic','journal','idea','relevance'].every(k => typeof p[k] === 'string' && p[k].trim())
          && Number.isInteger(p.year) && !!safeUrl(p.url)
          && Array.isArray(p.category_ids) && p.category_ids.length > 0
          && p.category_ids.every(id => categories.has(id))
          && Array.isArray(p.project_ids) && p.project_ids.every(id => projects.has(id))
          && [null, 'to-read', 'reading', 'read'].includes(p.reading_status);
      });
    }

    function makeEntry(paper, projectMap) {
      const row = node('li', 'academic-paper-entry');
      const heading = node('h3', 'academic-paper-title');
      const title = paperLink(paper.title, paper.url, '');
      if (title) heading.append(title);
      row.append(heading);

      row.append(node('p', 'academic-paper-citation', paper.authors + ' (' + paper.year + ') · ' + paper.journal));
      row.append(node('p', 'academic-paper-relevance', paper.relevance));
      const more = node('details', 'academic-paper-detail');
      more.append(node('summary', '', 'Core idea'), node('p', '', paper.idea));
      row.append(more);

      const related = paper.project_ids.map(id => projectMap.get(id)).filter(Boolean);
      if (related.length) {
        const relationships = node('p', 'academic-paper-related');
        relationships.append(node('span', '', 'Related: '));
        related.forEach((project, i) => {
          if (i) relationships.append(document.createTextNode(' · '));
          const a = paperLink(project.name, project.url, '');
          if (a) relationships.append(a);
        });
        row.append(relationships);
      }

      const names = {'to-read':'To read', 'reading':'Reading', 'read':'Read'};
      if (names[paper.reading_status]) row.append(node('p', 'academic-paper-status', 'Reading status: ' + names[paper.reading_status]));
      return row;
    }

    function render(data, category) {
      const papers = data.papers.filter(p => p.reading_status !== 'reading' && (category === 'all' || p.category_ids.includes(category)));
      const projectMap = new Map(data.projects.map(p => [p.id, p]));
      list.replaceChildren(...papers.map(p => makeEntry(p, projectMap)));
      if (!papers.length) list.append(node('li', 'academic-paper-empty', 'No references in this category.'));
      counter.textContent = papers.length + (papers.length === 1 ? ' reference' : ' references');
      [...filters.children].forEach(button => {
        const active = button.dataset.filter === category;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });
    }

    fetch('data/reading-list.json')
      .then(response => {
        if (!response.ok) throw new Error('Reading list unavailable');
        return response.json();
      })
      .then(data => {
        if (!validData(data)) throw new Error('Invalid reading-list data');
        const usedCategories = data.categories.filter(c =>
          c.id === 'all' || data.papers.some(p => p.reading_status !== 'reading' && p.category_ids.includes(c.id))
        );
        filters.replaceChildren(...usedCategories.map(category => {
          const button = node('button', 'academic-paper-filter', category.id === 'all' ? 'All' : category.label);
          button.type = 'button';
          button.dataset.filter = category.id;
          button.setAttribute('aria-pressed', 'false');
          button.addEventListener('click', () => render(data, category.id));
          return button;
        }));
        if (typeof data.collection_note === 'string') collectionNote.textContent = data.collection_note;
        render(data, 'all');
        list.hidden = false;
        counter.hidden = false;
        fallback.hidden = true;
      })
      .catch(() => {
        // Preserve the static bibliography as a fallback, rather than showing an error-only panel.
        list.hidden = true;
        counter.hidden = true;
        fallback.hidden = false;
        filters.replaceChildren();
      });
  }

})();