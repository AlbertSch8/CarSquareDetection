from pathlib import Path
from PIL import Image
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None  # vypnout limit pro velké obrázky

INPUT_DIR = Path("anotace_aut/images")
OUTPUT_DIR = Path("anotace_aut/images_resized")
TARGET_WIDTH = 1000

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

extensions = {".jpg", ".jpeg", ".png"}
already_done = {f.name for f in OUTPUT_DIR.iterdir() if f.suffix.lower() in extensions}
images = [f for f in INPUT_DIR.iterdir() if f.suffix.lower() in extensions and f.name not in already_done]

print(f"Celkem obrázků: {len(already_done) + len(images)}, už hotovo: {len(already_done)}, zbývá: {len(images)}")

for img_path in tqdm(images, desc="Zmenšování"):
    with Image.open(img_path) as img:
        w, h = img.size
        if w == 0:
            continue
        new_h = int(h * TARGET_WIDTH / w)
        resized = img.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
        out_path = OUTPUT_DIR / img_path.name
        resized.save(out_path, quality=95)

print(f"Hotovo! Zmenšené obrázky jsou v: {OUTPUT_DIR}")
