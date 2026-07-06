"""Process WhatsApp gallery images: optimize, SEO rename, generate manifest."""
import json
import re
from pathlib import Path
from PIL import Image

SRC_DIR = Path(r"C:\Users\Admin\.cursor\projects\d-TathaGat-Trustee-Wesite\assets")
OUT_DIR = Path(r"D:\TathaGat Trustee Wesite\assets\images\gallery")
MANIFEST_PATH = Path(r"D:\TathaGat Trustee Wesite\assets\images\gallery-manifest.json")

# SEO slugs + alt text (chronological program themes)
GALLERY_META = [
    ("tathagat-trust-banaras-public-school-program-event-01", "Tathagat Trust community program event at Banaras Public School, Varanasi"),
    ("tathagat-trust-banaras-public-school-program-event-02", "Education and community outreach program organized by Tathagat Trust"),
    ("tathagat-trust-student-award-ceremony-varanasi-01", "Students receiving recognition at Tathagat Trust award ceremony in Varanasi"),
    ("tathagat-trust-community-education-program-01", "Tathagat Trust education initiative for underprivileged youth"),
    ("tathagat-trust-banaras-public-school-ceremony-01", "Formal ceremony at Banaras Public School supported by Tathagat Trust"),
    ("tathagat-trust-youth-empowerment-event-01", "Youth empowerment and skill development event by Tathagat Trust"),
    ("tathagat-trust-school-function-varanasi-01", "School function celebrating student achievement at Banaras Public School"),
    ("tathagat-trust-certificate-distribution-ceremony-01", "Certificate distribution ceremony for meritorious students, Tathagat Trust"),
    ("tathagat-trust-community-outreach-varanasi-01", "Community outreach program by Tathagat Trust in Varanasi district"),
    ("tathagat-trust-education-program-students-01", "Students participating in Tathagat Trust education program"),
    ("tathagat-trust-award-presentation-ceremony-01", "Award presentation ceremony honoring student excellence"),
    ("tathagat-trust-school-event-banaras-01", "School event at Banaras Public School, Tathagat Trust initiative"),
    ("tathagat-trust-student-recognition-program-01", "Student recognition program for tribal and underprivileged communities"),
    ("tathagat-trust-community-ceremony-varanasi-01", "Community ceremony supporting education and social inclusion"),
    ("tathagat-trust-education-ceremony-01", "Education ceremony promoting inclusive learning, Tathagat Trust"),
    ("tathagat-trust-vanvasi-medha-samman-group-photo", "Students holding certificates at Vanvasi Medha Samman Samaroh organized by Tathagat Trust, August 2025"),
    ("tathagat-trust-vanvasi-medha-samman-certificate", "Certificate presentation at Vanvasi Medha Samman Samaroh, Banaras Public School Varanasi"),
    ("tathagat-trust-vanvasi-medha-samman-samaroh-stage", "Vanvasi Medha Samman Samaroh stage ceremony organized by Tathagat Trust"),
    ("tathagat-trust-student-trophy-award-ceremony", "Student receiving trophy and certificate at Tathagat Trust award function"),
    ("tathagat-trust-award-ceremony-officials-stage", "School officials presenting awards to students on stage"),
    ("tathagat-trust-certificate-ceremony-female-student", "Female student receiving certificate at Tathagat Trust formal ceremony"),
    ("tathagat-trust-banaras-public-school-award-trophy", "Banaras Public School award ceremony with trophy presentation to student"),
    ("tathagat-trust-student-certificate-presentation-01", "Student certificate presentation during Tathagat Trust ceremony"),
    ("tathagat-trust-female-student-award-banaras-school", "Female student in uniform receiving award at Banaras Public School ceremony"),
    ("tathagat-trust-vanvasi-medha-samman-varanasi-2025", "Vanvasi Medha Samman Samaroh at Banaras Public School, Varanasi — Tathagat Trust"),
    ("tathagat-trust-sapling-presentation-ceremony-01", "Sapling presentation ceremony at Tathagat Trust community event"),
    ("tathagat-trust-tree-plantation-ceremony-01", "Tree plantation and sapling gifting ceremony, Tathagat Trust"),
    ("tathagat-trust-environmental-sapling-ceremony", "Environmental awareness sapling presentation at Tathagat Trust event"),
    ("tathagat-trust-scholarship-presentation-banaras-school", "Scholarship presentation ceremony at Banaras Public School"),
    ("tathagat-trust-student-certificate-award-varanasi", "Student receiving certificate from officials at Varanasi ceremony"),
    ("tathagat-trust-banaras-public-school-building-exterior", "Banaras Public School three-story campus building exterior, Varanasi"),
    ("tathagat-trust-baba-ramdev-yoga-camp-award-ceremony", "Baba Ramdev presenting certificate at one-day yoga camp, Patanjali Yogpeeth Haridwar"),
    ("tathagat-trust-baba-ramdev-banaras-public-school-event", "Baba Ramdev at Banaras Public School event, Barji Nayepur Varanasi"),
    ("tathagat-trust-banaras-public-school-assembly-ceremony", "School assembly at Banaras Public School with students in uniform"),
    ("tathagat-trust-sapling-gift-ceremony-community", "Community sapling gift ceremony at Tathagat Trust indoor event"),
    ("tathagat-trust-plant-presentation-ceremony-02", "Dignitaries presenting potted sapling at Tathagat Trust ceremony"),
    ("tathagat-trust-banaras-public-school-award-certificate", "Banaras Public School award ceremony — certificate and trophy to student"),
    ("tathagat-trust-female-student-certificate-ceremony", "Female student in school uniform receiving certificate at award ceremony"),
    ("tathagat-trust-banaras-public-school-prize-distribution", "Prize distribution ceremony at Banaras Public School, Tathagat Trust"),
    ("tathagat-trust-student-award-banaras-public-school-02", "Student award ceremony on stage at Banaras Public School"),
    ("tathagat-trust-award-function-students-certificates", "Award function with students displaying certificates, Tathagat Trust"),
    ("tathagat-trust-vanvasi-medha-samman-students-group", "Group of students with certificates at Vanvasi Medha Samman Samaroh"),
    ("tathagat-trust-certificate-ceremony-stage-varanasi", "Certificate ceremony on stage at Tathagat Trust Varanasi program"),
    ("tathagat-trust-school-campus-building-bicycles", "Banaras Public School campus building with bicycle parking area"),
    ("tathagat-trust-community-program-indoor-ceremony", "Indoor community program ceremony organized by Tathagat Trust"),
    ("tathagat-trust-education-event-dignitaries-students", "Dignitaries and students at Tathagat Trust education event"),
    ("tathagat-trust-award-ceremony-banaras-school-03", "Award ceremony at Banaras Public School with school banner"),
    ("tathagat-trust-student-achievement-recognition-01", "Student achievement recognition at Tathagat Trust program"),
    ("tathagat-trust-youth-education-ceremony-varanasi", "Youth education ceremony supporting underprivileged communities, Varanasi"),
    ("tathagat-trust-banaras-public-school-campus-view", "Banaras Public School institutional building campus view, Varanasi"),
]


def sort_key(path: Path) -> tuple:
    name = path.name
    m = re.search(r"2\.35\.(\d+)_PM", name)
    minute = int(m.group(1)) if m else 99
    sub = 0
    m2 = re.search(r"PM__(\d+)_", name)
    if m2:
        sub = int(m2.group(1))
    elif "PM-" in name and "PM__" not in name:
        sub = -1
    return (minute, sub, name)


def optimize_image(src: Path, slug: str) -> dict:
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    max_w = 1200
    if w > max_w:
        nh = int(h * max_w / w)
        img = img.resize((max_w, nh), Image.Resampling.LANCZOS)
        w, h = img.size

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jpg_path = OUT_DIR / f"{slug}.jpg"
    webp_path = OUT_DIR / f"{slug}.webp"
    img.save(jpg_path, "JPEG", quality=85, optimize=True, progressive=True)
    img.save(webp_path, "WEBP", quality=82, method=6)

    return {
        "slug": slug,
        "width": w,
        "height": h,
        "jpg": f"gallery/{slug}.jpg",
        "webp": f"gallery/{slug}.webp",
        "jpgSize": jpg_path.stat().st_size,
        "webpSize": webp_path.stat().st_size,
    }


def main():
    files = sorted(SRC_DIR.glob("*WhatsApp*"), key=sort_key)
    if len(files) != 50:
        print(f"Warning: expected 50 files, found {len(files)}")

    manifest = []
    for i, src in enumerate(files):
        slug, alt = GALLERY_META[i] if i < len(GALLERY_META) else (
            f"tathagat-trust-program-gallery-{i+1:02d}",
            f"Tathagat Trust education and community program photo {i+1}",
        )
        info = optimize_image(src, slug)
        info["alt"] = alt
        manifest.append(info)
        print(f"[{i+1:02d}] {slug} ({info['jpgSize']//1024}KB jpg / {info['webpSize']//1024}KB webp)")

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nManifest: {MANIFEST_PATH}")
    print(f"Total images: {len(manifest)}")


if __name__ == "__main__":
    main()
