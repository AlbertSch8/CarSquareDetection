import os
import shutil
from pathlib import Path

from ultralytics import YOLO
from tqdm import tqdm

# -----------------------------
# MODEL
# -----------------------------

MODEL_PATH = "yolov8s.pt"
model = YOLO(MODEL_PATH)

CAR_CLASS_ID = 2
CONF_THRESHOLD = 0.4

# -----------------------------
# INPUT
# -----------------------------

INPUT_FOLDERS = {
    "skoda": "obrazky_skoda",
    "audi": "obrazky_audi",
    "volkswagen": "obrazky_volkswagen"
}

CLASS_MAP = {
    "skoda": 0,
    "audi": 1,
    "volkswagen": 2
}

# -----------------------------
# OUTPUT
# -----------------------------

OUTPUT_DIR = Path("anotace_aut")

IMAGES_DIR = OUTPUT_DIR / "images"
LABELS_DIR = OUTPUT_DIR / "labels"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LABELS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# SPOČÍTAT CELKOVÝ POČET OBRÁZKŮ
# -----------------------------

all_images = []

for brand, folder in INPUT_FOLDERS.items():
    for img_name in os.listdir(folder):
        if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            all_images.append((brand, folder, img_name))

# -----------------------------
# PROGRESS BAR
# -----------------------------

for brand, folder, img_name in tqdm(all_images, desc="Anotuji obrázky"):

    class_id = CLASS_MAP[brand]

    img_path = os.path.join(folder, img_name)

    results = model(img_path)

    label_lines = []

    for r in results:

        if r.boxes is None:
            continue

        for box in r.boxes:

            detected_class = int(box.cls.item())
            conf = float(box.conf.item())

            # pouze auta
            if detected_class != CAR_CLASS_ID or conf < CONF_THRESHOLD:
                continue

            x, y, w, h = box.xywhn[0].tolist()

            label_lines.append(f"{class_id} {x} {y} {w} {h}")

    if not label_lines:
        continue

    # copy image
    shutil.copy(img_path, IMAGES_DIR / img_name)

    # save label
    label_path = LABELS_DIR / (Path(img_name).stem + ".txt")

    with open(label_path, "w") as f:
        f.write("\n".join(label_lines))

print("Hotovo ✔ Dataset je ve složce:", OUTPUT_DIR)