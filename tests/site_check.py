#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import re

root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js=(root/'app.js').read_text(encoding='utf-8')
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.pages=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='article' and 'data-page' in a:self.pages.append(a['data-page'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
p=Page();p.feed(html)
assert len(p.ids)==len(set(p.ids)), 'Duplicate IDs'
assert len(p.pages)==6 and set(p.pages)=={'home','projects','research','engineering','about','cv'}
for link in p.links:
    if link.startswith('#'): assert link[1:] in p.ids, f'Broken anchor: {link}'
    elif not link.startswith(('https://','http://','mailto:')):
        assert (root/link.split('#')[0].split('?')[0]).is_file(), f'Missing file: {link}'
for expected in ('Paul Zegeling','Monte Carlo','fractional order differential systems','schoutenkelvin@gmail.com'):
    assert expected in html, f'Missing verified content: {expected}'
assert not re.search(r'98%|95%|WIREFRAME / CONCEPT|lorem ipsum',html,re.I)
assert 'prefers-reduced-motion' in css
assert 'aria-current' in js and 'aria-expanded' in js
print('PASS: sections, IDs, internal links, assets, evidence and navigation markers')
print('NOTE: Browser responsiveness, external HTTP links and CV privacy require manual checks.')
