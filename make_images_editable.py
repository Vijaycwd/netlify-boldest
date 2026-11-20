import re
import shutil

FILE = "index.html"
shutil.copy(FILE, "index.before-images.html")  # backup

src = open(FILE, encoding="utf-8").read()
parts = re.split(r'(<script.*?</script>)', src, flags=re.S)
img = re.compile(r'<img\b([^>]*?)(/?)>', re.S)

count = 0

def fix(m):
    global count
    attrs, slash = m.group(1), m.group(2)

    if "data-img=" not in attrs:
        return m.group(0)
    if "data-editable" in attrs:
        return m.group(0)

    
    if re.search(r'\bclass="', attrs):
        attrs = re.sub(r'class="', 'class="editable ', attrs, 1)
    else:
        attrs += ' class="editable"'

    attrs += ' data-editable="image" data-path="/assets/img"'
    count += 1
    return f'<img{attrs}{slash}>'

out = [p if p.startswith("<script") else img.sub(fix, p) for p in parts]
open(FILE, "w", encoding="utf-8").write("".join(out))
print(f"Done. {count} images updated.")