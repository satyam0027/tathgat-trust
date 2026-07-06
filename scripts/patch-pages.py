import json
import re
from pathlib import Path

ROOT = Path(r"D:\TathaGat Trustee Wesite")
manifest = json.loads((ROOT / "assets/images/gallery-manifest.json").read_text(encoding="utf-8"))
items_html = (ROOT / "scripts/gallery-items.html").read_text(encoding="utf-8")

# Patch gallery.html
gallery = ROOT / "gallery.html"
text = gallery.read_text(encoding="utf-8")
text = re.sub(
    r"  <meta name=\"description\" content=\"[^\"]+\">",
    '  <meta name="description" content="Photo gallery of Tathagat Trust programs — award ceremonies, Vanvasi Medha Samman, Banaras Public School events, and community education across India.">',
    text,
)
text = re.sub(
    r"  <meta property=\"og:image\" content=\"[^\"]+\">",
    '  <meta property="og:image" content="assets/images/gallery/tathagat-trust-vanvasi-medha-samman-group-photo.jpg">',
    text,
)
text = re.sub(
    r"        <!-- TODO: Replace placeholder images with actual brochure photos -->\n        <div class=\"gallery-grid--masonry reveal\">.*?</div>",
    f"        <div class=\"gallery-grid--masonry reveal\">\n{items_html}\n        </div>",
    text,
    flags=re.DOTALL,
)
gallery.write_text(text, encoding="utf-8")
print("Updated gallery.html")


def preview_item(m, prefix="assets/images"):
    return f'''          <div class="gallery-item gallery-item--photo">
            <picture>
              <source srcset="{prefix}/{m['webp']}" type="image/webp">
              <img src="{prefix}/{m['jpg']}" alt="{m['alt']}" width="{m['width']}" height="{m['height']}" loading="lazy" decoding="async">
            </picture>
          </div>'''

# Index preview: 8 diverse picks
preview_indices = [0, 15, 18, 22, 30, 33, 16, 47]
index_items = "\n".join(preview_item(manifest[i]) for i in preview_indices)
index = ROOT / "index.html"
itext = index.read_text(encoding="utf-8")
itext = re.sub(
    r"        <!-- TODO: Replace placeholder images with actual brochure photos -->\n        <div class=\"gallery-grid reveal\">.*?</div>",
    f"        <div class=\"gallery-grid reveal\">\n{index_items}\n        </div>",
    itext,
    flags=re.DOTALL,
)
index.write_text(itext, encoding="utf-8")
print("Updated index.html preview")

# About page: 12 picks
about_indices = [0, 3, 15, 16, 18, 22, 30, 31, 33, 34, 37, 47]
about_items = "\n".join(preview_item(manifest[i]) for i in about_indices)
about = ROOT / "about.html"
atext = about.read_text(encoding="utf-8")
atext = re.sub(
    r"        <!-- TODO: Replace with actual brochure collage photos -->\n        <div class=\"gallery-grid reveal\">.*?</div>",
    f"        <div class=\"gallery-grid reveal\">\n{about_items}\n        </div>",
    atext,
    flags=re.DOTALL,
)
about.write_text(atext, encoding="utf-8")
print("Updated about.html gallery")

# Banaras BPS page gallery + building photos
bps_indices = [30, 31, 33, 37, 39, 44, 50 - 1]  # building, assembly, awards, campus
bps_items = []
for i in [30, 33, 37, 39, 44, 49]:
    m = manifest[i]
    bps_items.append(f'''          <div class="gallery-item gallery-item--photo">
            <picture>
              <source srcset="../assets/images/{m['webp']}" type="image/webp">
              <img src="../assets/images/{m['jpg']}" alt="{m['alt']}" width="{m['width']}" height="{m['height']}" loading="lazy" decoding="async">
            </picture>
          </div>''')
bps_grid = "\n".join(bps_items)

bps = ROOT / "work-areas/banaras-bps.html"
btext = bps.read_text(encoding="utf-8")
# Replace building placeholders
btext = btext.replace(
    '''        <!-- TODO: Replace with actual school building photos from brochure -->
        <div class="two-col" style="margin-top: 2rem;">
          <div class="reveal">
            <img src="../assets/images/bps-building-1.jpg" alt="Banaras Public School building exterior, Varanasi district" loading="lazy" style="border-radius: 8px; box-shadow: var(--shadow-md);">
          </div>
          <div class="reveal reveal-delay-1">
            <img src="../assets/images/bps-building-2.jpg" alt="Banaras Public School campus view" loading="lazy" style="border-radius: 8px; box-shadow: var(--shadow-md);">
          </div>
        </div>''',
    f'''        <div class="two-col mt-lg">
          <figure class="regional-map reveal">
            <picture>
              <source srcset="../assets/images/{manifest[30]['webp']}" type="image/webp">
              <img src="../assets/images/{manifest[30]['jpg']}" alt="{manifest[30]['alt']}" width="{manifest[30]['width']}" height="{manifest[30]['height']}" loading="lazy" decoding="async">
            </picture>
            <figcaption>Banaras Public School campus building, Varanasi</figcaption>
          </figure>
          <figure class="regional-map reveal reveal-delay-1">
            <picture>
              <source srcset="../assets/images/{manifest[49]['webp']}" type="image/webp">
              <img src="../assets/images/{manifest[49]['jpg']}" alt="{manifest[49]['alt']}" width="{manifest[49]['width']}" height="{manifest[49]['height']}" loading="lazy" decoding="async">
            </picture>
            <figcaption>Banaras Public School campus exterior view</figcaption>
          </figure>
        </div>''',
)
btext = re.sub(
    r"        <div class=\"gallery-grid reveal\">.*?</div>",
    f"        <div class=\"gallery-grid reveal\">\n{bps_grid}\n          <div class=\"gallery-item gallery-item--map\"><img src=\"../assets/images/tathagat-trust-banaras-varanasi-bps-map.jpg\" alt=\"Map of Banaras Varanasi district — Banaras Public School operational area\" loading=\"lazy\" width=\"1024\" height=\"682\"></div>\n        </div>",
    btext,
    flags=re.DOTALL,
)
bps.write_text(btext, encoding="utf-8")
print("Updated banaras-bps.html")

print("Done.")
