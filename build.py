#!/usr/bin/env python3
"""Builds privacy.html, terms.html, delete-account.html and support.html
from src/*.md. No dependencies. Run after editing anything in src/:

    python3 build.py

Edit the two constants below once; every page picks them up."""
import html
import pathlib
import re

STUDIO = "The Trap & Run team"
SUPPORT_EMAIL = "nazishahsan40@gmail.com"

ROOT = pathlib.Path(__file__).parent
PAGES = {"privacy": "Privacy Policy", "terms": "Terms of Service",
         "delete-account": "Delete your account", "support": "Support"}


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def convert(md):
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    md = md.replace("[Your name or studio]", STUDIO)
    md = md.replace("[support email]", SUPPORT_EMAIL)
    out, para, items, rows = [], [], [], []

    def flush():
        nonlocal para, items, rows
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para = []
        if items:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(i) for i in items))
            items = []
        if rows:
            head, body = rows[0], rows[2:]
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (
                "".join("<th>%s</th>" % inline(c) for c in head),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in body)))
            rows = []

    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            flush()
        elif s.startswith("#"):
            flush()
            level = len(s) - len(s.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (level, inline(s[level:].strip()), level))
        elif s.startswith("|"):
            if para or items:
                flush()
            rows.append([c.strip() for c in s.strip("|").split("|")])
        elif re.match(r"^(\d+\.|-)\s", s):
            if para or rows:
                flush()
            items.append(re.sub(r"^(\d+\.|-)\s+", "", s))
        elif (items and s.startswith("  ")):
            items[-1] += " " + s.strip()
        else:
            if items or rows:
                flush()
            para.append(s.strip())
    flush()
    return "\n".join(out)


TEMPLATE = (ROOT / "src" / "page.html").read_text()
for name, title in PAGES.items():
    body = convert((ROOT / "src" / f"{name}.md").read_text())
    page = TEMPLATE.replace("{{title}}", html.escape(title)).replace("{{body}}", body)
    (ROOT / f"{name}.html").write_text(page)
    print("wrote", f"{name}.html")
