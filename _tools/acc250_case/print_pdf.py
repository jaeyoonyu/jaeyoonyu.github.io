#!/usr/bin/env python3
"""Print worksheet HTML pages to PDF with headless Chrome: <name>.pdf and <name>-Key.pdf (the #key view).

Usage: python _tools/acc250_case/print_pdf.py assets/ACC250/Ch9-PPE-Worksheet.html [...]
"""
import os, subprocess, sys
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for f in sys.argv[1:]:
    p = Path(f).resolve()
    for suffix, frag in (("", ""), ("-Key", "#key")):
        out = p.with_name(p.stem + suffix + ".pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=3000", f"--print-to-pdf={out}", p.as_uri() + frag],
                       check=True, capture_output=True)
        print("wrote", out.name)
