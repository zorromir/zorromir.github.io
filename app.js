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

  // Research-library data is maintained in data/reading-list.json; this code only renders it.
  const library = document.querySelector('[data-paper-carousel]');
  if (library) {
    const track = library.querySelector('[data-paper-track]');
    const counter = library.querySelector('[data-paper-count]');
    const prev = library.querySelector('[data-paper-prev]');
    const next = library.querySelector('[data-paper-next]');
    const filters = document.querySelector('[data-paper-filters]');
    const dotsHost = library.querySelector('[data-paper-dots]');
    const collectionNote = document.querySelector('[data-paper-collection-note]');
    let current = 0;
    let filtered = [];
    let activeFilter = 'all';
    let touchStart = null;

    function node(tag, className, value) {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (value !== undefined) el.textContent = String(value);
      return el;
    }

    function safeUrl(value, internal = false) {
      if (typeof value !== 'string') return null;
      if (internal && /^#[a-z0-9-]+$/i.test(value)) return value;
      try {
        const parsed = new URL(value);
        return parsed.protocol === 'https:' ? parsed.href : null;
      } catch (_) { return null; }
    }

    function link(text, href, className) {
      const a = node('a', className, text);
      const safe = safeUrl(href, true);
      if (!safe) return null;
      a.href = safe;
      if (!safe.startsWith('#')) {
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
      }
      return a;
    }

    function coverFor(paper, index) {
      const cover = node('div', 'paper-cover');
      const accent = /^#[0-9a-fA-F]{6}$/.test(paper.cover_accent || '') ? paper.cover_accent : '#24766e';
      cover.style.setProperty('--paper-accent', accent);
      cover.setAttribute('aria-label', 'Custom typographic cover for ' + paper.title);

      const top = node('div', 'paper-cover-top');
      top.append(node('span', '', 'RESEARCH / ' + paper.year), node('span', '', String(index + 1).padStart(2, '0')));

      const inside = node('div', 'paper-cover-inner');
      inside.append(node('span', 'paper-cover-code', paper.short_label));
      const lines = node('div', 'paper-cover-lines');
      for (let i = 0; i < 3; i++) lines.append(document.createElement('i'));
      inside.append(lines, node('span', 'paper-cover-topic', paper.topic.toUpperCase()));

      const bottom = node('div', 'paper-cover-bottom');
      bottom.append(node('span', '', paper.journal), node('span', '', 'SELECTED PAPER'));
      cover.append(top, inside, bottom);
      return cover;
    }

    function detail(label, value) {
      const wrapper = node('div', 'reading-detail');
      wrapper.append(node('span', 'meta', label), node('p', '', value));
      return wrapper;
    }

    function makeSlide(paper, index, projectMap) {
      const slide = node('article', 'reading-slide');
      slide.setAttribute('role', 'group');
      slide.setAttribute('aria-roledescription', 'slide');
      slide.setAttribute('aria-label', (index + 1) + ': ' + paper.title);

      const copy = node('div', 'reading-paper-copy');
      copy.append(
        node('span', 'meta', paper.topic.toUpperCase() + ' · ' + paper.year),
        node('h3', '', paper.title),
        node('p', 'reading-byline', paper.authors + ' · ' + paper.journal),
        detail('THE CORE IDEA', paper.idea),
        detail('WHY IT MATTERS FOR MY ECONOMETRICS', paper.relevance)
      );

      const related = node('div', 'reading-related');
      const projects = paper.project_ids.map(id => projectMap.get(id)).filter(Boolean);
      if (projects.length) {
        related.append(node('span', 'meta', 'CONNECTED PROJECTS'));
        const linksBox = node('div', 'reading-related-links');
        projects.forEach(project => {
          const a = link(project.name + ' ↗', project.url, 'reading-project-link');
          if (a) linksBox.append(a);
        });
        related.append(linksBox);
      }
      copy.append(related);

      const statusNames = {'to-read':'To read',reading:'Reading',read:'Read'};
      if (statusNames[paper.reading_status]) {
        copy.append(node('p', 'reading-status', 'Reading status: ' + statusNames[paper.reading_status]));
      }
      const paperLink = link('Open publication ↗', paper.url, 'text-link reading-paper-link');
      if (paperLink) copy.append(paperLink);
      slide.append(coverFor(paper, index), copy);
      return slide;
    }

    function showPaper(index) {
      if (!filtered.length) return;
      current = (index + filtered.length) % filtered.length;
      track.style.transform = 'translateX(-' + (100 * current) + '%)';
      [...track.children].forEach((slide, i) => {
        const selected = i === current;
        slide.setAttribute('aria-hidden', String(!selected));
        slide.inert = !selected;
      });
      [...dotsHost.children].forEach((dot, i) => {
        dot.classList.toggle('is-active', i === current);
        dot.setAttribute('aria-pressed', String(i === current));
      });
      counter.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(filtered.length).padStart(2, '0');
    }

    function renderCollection(data, category) {
      activeFilter = category;
      current = 0;
      filtered = data.papers.filter(paper => category === 'all' || paper.category_ids.includes(category));
      const projectMap = new Map(data.projects.map(project => [project.id, project]));
      track.style.transform = 'translateX(0)';
      track.replaceChildren(...filtered.map((paper, i) => makeSlide(paper, i, projectMap)));
      dotsHost.replaceChildren(...filtered.map((paper, i) => {
        const dot = node('button', 'reading-dot');
        dot.type = 'button';
        dot.setAttribute('aria-label', 'Show paper ' + (i + 1) + ': ' + paper.title);
        dot.setAttribute('aria-pressed', String(i === 0));
        dot.addEventListener('click', () => showPaper(i));
        return dot;
      }));
      [...filters.children].forEach(button => {
        const active = button.dataset.filter === category;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      const disabled = filtered.length < 2;
      prev.disabled = next.disabled = disabled;
      dotsHost.hidden = disabled;
      if (filtered.length) showPaper(0);
      else {
        track.append(node('p', 'reading-loading', 'No papers in this category yet.'));
        counter.textContent = '00 / 00';
      }
    }

    function validData(data) {
      if (!data || !Array.isArray(data.papers) || !Array.isArray(data.projects) || !Array.isArray(data.categories)) return false;
      const ids = new Set();
      const categories = new Set(data.categories.map(item => item.id));
      const projects = new Set(data.projects.map(item => item.id));
      return data.papers.every(p => {
        if (!p || typeof p.id !== 'string' || ids.has(p.id)) return false;
        ids.add(p.id);
        return ['title','authors','topic','journal','idea','relevance','short_label'].every(field => typeof p[field] === 'string' && p[field].trim().length > 0)
          && Number.isInteger(p.year) && !!safeUrl(p.url)
          && Array.isArray(p.category_ids) && p.category_ids.length > 0 && p.category_ids.every(id => categories.has(id))
          && Array.isArray(p.project_ids) && p.project_ids.every(id => projects.has(id))
          && [null,'to-read','reading','read'].includes(p.reading_status);
      });
    }

    fetch('data/reading-list.json')
      .then(response => {
        if (!response.ok) throw new Error('Reading list unavailable');
        return response.json();
      })
      .then(data => {
        if (!validData(data)) throw new Error('Reading-list data needs correction');
        const presentCategories = data.categories.filter(category => category.id === 'all' || data.papers.some(paper => paper.category_ids.includes(category.id)));
        filters.replaceChildren(...presentCategories.map(category => {
          const count = category.id === 'all' ? data.papers.length : data.papers.filter(paper => paper.category_ids.includes(category.id)).length;
          const button = node('button', 'reading-filter', category.label + ' · ' + count);
          button.type = 'button';
          button.dataset.filter = category.id;
          button.setAttribute('aria-pressed', 'false');
          button.addEventListener('click', () => renderCollection(data, category.id));
          return button;
        }));
        collectionNote.textContent = data.collection_note || 'Project-specific reading notes.';
        renderCollection(data, 'all');
      })
      .catch(() => {
        filters.replaceChildren();
        track.style.transform = 'none';
        track.replaceChildren(node('p', 'reading-loading', 'The paper library could not load. You can still open the source bibliography below.'));
        counter.textContent = '— / —';
        prev.disabled = next.disabled = true;
        dotsHost.replaceChildren();
        collectionNote.textContent = 'Paper cards are temporarily unavailable.';
      });

    prev.addEventListener('click', () => showPaper(current - 1));
    next.addEventListener('click', () => showPaper(current + 1));
    library.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        showPaper(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    library.addEventListener('touchstart', event => {
      if (event.touches.length === 1) touchStart = event.touches[0].clientX;
    }, { passive: true });
    library.addEventListener('touchend', event => {
      if (touchStart === null || !event.changedTouches.length) return;
      const dx = event.changedTouches[0].clientX - touchStart;
      touchStart = null;
      if (Math.abs(dx) > 55) showPaper(current + (dx < 0 ? 1 : -1));
    }, { passive: true });
  }

})();