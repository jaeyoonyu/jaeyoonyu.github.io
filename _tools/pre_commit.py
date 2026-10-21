"""Pre-commit hook body: refresh ?v= stamps and stage the pages it touched.

Installed as .git/hooks/pre-commit by:  python _tools/install_hook.py
A page that already had unstaged edits is not staged behind the user's back:
the commit stops and says which page to look at.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True).stdout


dirty_before = set(git('diff', '--name-only').split())
out = subprocess.run([sys.executable, str(ROOT / '_tools' / 'version_assets.py')],
                     cwd=ROOT, capture_output=True, text=True).stdout
changed = [l.split('versioned links in ', 1)[1].replace('\\', '/') for l in out.splitlines()
           if l.startswith('versioned links in ')]
clash = [c for c in changed if c in dirty_before]
if clash:
    print('pre-commit: asset links were re-versioned in pages that also have unstaged edits:')
    for c in clash:
        print('   ', c)
    print('Review and stage them, then commit again.')
    sys.exit(1)
if changed:
    git('add', '--', *changed)
    print('pre-commit: refreshed ?v= links in', ', '.join(changed))
