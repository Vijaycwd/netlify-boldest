import re

src = open("index.html", encoding="utf-8").read()
parts = re.split(r'(<script.*?</script>)', src, flags=re.S)
tag = re.compile(r'<(h[1-6]|p|blockquote|summary)(\s[^>]*)?>')

def fix(m):
    name, attrs = m.group(1), m.group(2) or ""
    if "editable" in attrs:
        return m.group(0)
    if 'class="' in attrs:
        attrs = attrs.replace('class="', 'class="editable ', 1)
    elif re.search(r'class=\w', attrs):          # class=lede (quotes இல்லாதது)
        attrs = re.sub(r'class=(\w+)', r'class="editable \1"', attrs, 1)
    else:
        attrs += ' class="editable"'
    return f'<{name}{attrs}>'

out = [p if p.startswith("<script") else tag.sub(fix, p) for p in parts]
open("index.editable.html", "w", encoding="utf-8").write("".join(out))
print("Done: index.editable.html")