"""Stamp every link to a PDF or HTML file under /assets/ with ?v=<content hash>.

Phones open a PDF from the copy they downloaded earlier, so re-posting a file at
the same URL does not reach them. The hash changes only when the file's bytes
change, so a re-posted file gets a new URL and an unchanged one keeps its link.

Run from anywhere:  python _tools/version_assets.py
The pre-commit hook (_tools/install_hook.py) runs it before every commit.
Prints the pages it changed; exits 0 either way.
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {'_site', 'assets', '_includes', '_layouts', '_tools', '.git', 'node_modules'}
LINK = re.compile(r'(/assets/[^"\'()\s?#<>]+\.(?:pdf|html))(\?v=[0-9a-f]+)?')


def pages():
    for p in ROOT.rglob('*'):
        if p.suffix in ('.md', '.html') and p.is_file():
            rel = p.relative_to(ROOT)
            if not (set(rel.parts[:-1]) & SKIP):
                yield p


def stamp(path, cache={}):
    if path not in cache:
        f = ROOT / path.lstrip('/')
        cache[path] = hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.is_file() else None
    return cache[path]


def main():
    changed = []
    for p in pages():
        with open(p, encoding='utf-8', newline='') as fh:   # keep CRLF/LF as found
            text = fh.read()

        def sub(m):
            h = stamp(m.group(1))
            return m.group(0) if h is None else f'{m.group(1)}?v={h}'

        new = LINK.sub(sub, text)
        if new != text:
            p.write_text(new, encoding='utf-8', newline='')
            changed.append(str(p.relative_to(ROOT)))
    for c in changed:
        print('versioned links in', c)


if __name__ == '__main__':
    main()
