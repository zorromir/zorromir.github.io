/* Kelvin Schouten portfolio — editable settings */
const GITHUB_USERNAME = "zorromir";
const MAX_REPOSITORIES = 3;

const root = document.documentElement;
const themeToggle = document.querySelector('#theme-toggle');
const menuToggle = document.querySelector('#menu-toggle');
const nav = document.querySelector('#primary-nav');
const repoGrid = document.querySelector('#repo-grid');

function setTheme(theme) {
  const value = theme === 'dark' ? 'dark' : 'light';
  root.setAttribute('data-theme', value);
  themeToggle.setAttribute('aria-label', `Switch to ${value === 'dark' ? 'light' : 'dark'} theme`);
  try { localStorage.setItem('kelvin-theme', value); } catch (_) { /* Private mode */ }
}

try { setTheme(localStorage.getItem('kelvin-theme') || 'light'); }
catch (_) { setTheme('light'); }
themeToggle.addEventListener('click', () => setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));

function closeMenu() {
  nav.classList.remove('is-open');
  menuToggle.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation menu');
}
menuToggle.addEventListener('click', () => {
  const opening = !nav.classList.contains('is-open');
  nav.classList.toggle('is-open', opening);
  menuToggle.classList.toggle('is-open', opening);
  menuToggle.setAttribute('aria-expanded', String(opening));
  menuToggle.setAttribute('aria-label', opening ? 'Close navigation menu' : 'Open navigation menu');
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });

const yearNode = document.querySelector('#current-year');
if (yearNode) yearNode.textContent = String(new Date().getFullYear());

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function makeRepoCard(repo) {
  const card = el('a', 'repo-card');
  card.href = repo.html_url;
  card.target = '_blank';
  card.rel = 'noopener noreferrer';

  const top = el('div', 'repo-top');
  const icon = el('span', 'repo-icon', '⌁');
  icon.setAttribute('aria-hidden', 'true');
  const mark = el('span', 'repo-arrow', '↗');
  mark.setAttribute('aria-hidden', 'true');
  top.append(icon, mark);

  const name = el('h3', '', repo.name.replace(/[-_]/g, ' '));
  const description = el('p', '', repo.description || 'Public GitHub repository');
  const foot = el('div', 'repo-foot');
  const language = el('span', '', repo.language || 'Repository');
  const date = repo.pushed_at ? new Date(repo.pushed_at).toLocaleDateString('en-GB', { year: 'numeric', month: 'short' }) : '';
  const updated = el('span', '', date ? `Updated ${date}` : 'View on GitHub');
  foot.append(language, updated);
  card.append(top, name, description, foot);
  return card;
}

async function loadPublicRepos() {
  const api = `https://api.github.com/users/${encodeURIComponent(GITHUB_USERNAME)}/repos?sort=updated&per_page=100&type=public`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 6500);
  try {
    const response = await fetch(api, { headers: { 'Accept': 'application/vnd.github+json' }, signal: controller.signal });
    if (!response.ok) throw new Error(`GitHub returned ${response.status}`);
    const result = await response.json();
    if (!Array.isArray(result)) throw new Error('Invalid response');
    // We prefer nonempty, nonfork repositories. Empty public repositories are still accessible via the profile.
    const repositories = result.filter(repo => !repo.fork && !repo.private && repo.size > 0)
      .sort((a, b) => Date.parse(b.pushed_at || b.updated_at) - Date.parse(a.pushed_at || a.updated_at))
      .slice(0, MAX_REPOSITORIES);
    repoGrid.replaceChildren();
    if (repositories.length === 0) {
      repoGrid.append(emptyRepoCard('Public projects will appear here as they are published. In the meantime, visit my GitHub profile.'));
      return;
    }
    repositories.forEach(repo => repoGrid.append(makeRepoCard(repo)));
  } catch (_) {
    // Offline, blocked API, or GitHub rate limit — the profile link remains usable.
    repoGrid.replaceChildren(emptyRepoCard('Live repository listings are temporarily unavailable. Visit my public GitHub profile to explore my code.'));
  } finally {
    clearTimeout(timeout);
  }
}
function emptyRepoCard(message) {
  const box = el('div', 'repo-empty');
  const icon = el('span', 'repo-empty-icon', '⌁');
  icon.setAttribute('aria-hidden', 'true');
  box.append(icon, el('p', '', message));
  const link = el('a', '', 'Open GitHub profile ↗');
  link.href = `https://github.com/${encodeURIComponent(GITHUB_USERNAME)}`;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  box.append(link);
  return box;
}
if (repoGrid) loadPublicRepos();
