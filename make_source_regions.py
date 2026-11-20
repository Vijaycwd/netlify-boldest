import re
import shutil

FILE = "index.html"
PATH = "/index.html"
shutil.copy(FILE, "index.before-source.html")  # backup

src = open(FILE, encoding="utf-8").read()
parts = re.split(r'(<script.*?</script>)', src, flags=re.S)

pat = re.compile(r'<(h[1-6]|p|blockquote|summary)(\s[^>]*)?>([^<]+)</\1>')
n = 0

def fix(m):
    global n
    name, attrs, text = m.group(1), m.group(2) or "", m.group(3)
    if not text.strip() or "data-editable" in attrs:
        return m.group(0)
    
    attrs = re.sub(r'class="editable\s*"', '', attrs)
    attrs = attrs.replace('class="editable ', 'class="')
    attrs = re.sub(r'class=editable\b', '', attrs)
    n += 1
    attrs += f' data-editable="source" data-path="{PATH}" data-key="t{n}"'
    return f'<{name}{attrs}>{text}</{name}>'

out = [p if p.startswith("<script") else pat.sub(fix, p) for p in parts]
open(FILE, "w", encoding="utf-8").write("".join(out))
print(f"Done. {n} text regions added.")