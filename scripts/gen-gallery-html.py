import json
from pathlib import Path

manifest = json.loads(Path(r"D:\TathaGat Trustee Wesite\assets\images\gallery-manifest.json").read_text(encoding="utf-8"))
zoom = '<span class="gallery-item__zoom" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></span>'

items = []
for m in manifest:
    items.append(f'''          <div class="gallery-item gallery-item--photo" data-lightbox>
            <picture>
              <source srcset="assets/images/{m['webp']}" type="image/webp">
              <img src="assets/images/{m['jpg']}" alt="{m['alt']}" width="{m['width']}" height="{m['height']}" loading="lazy" decoding="async">
            </picture>
            {zoom}
          </div>''')

Path(r"D:\TathaGat Trustee Wesite\scripts\gallery-items.html").write_text("\n".join(items), encoding="utf-8")
print(f"Generated {len(items)} items")
