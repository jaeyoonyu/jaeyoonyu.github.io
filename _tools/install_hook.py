"""Install the pre-commit hook that keeps /assets/ links versioned (run once per clone)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
hook = ROOT / '.git' / 'hooks' / 'pre-commit'
hook.write_text('#!/bin/sh\nexec python "$(git rev-parse --show-toplevel)/_tools/pre_commit.py"\n',
                encoding='utf-8', newline='\n')
hook.chmod(0o755)
print('installed', hook)
