import os
import shutil
from pathlib import Path
import urllib.request

from ultralytics import YOLO
import cv2

# -----------------------------
# MODEL
# -----------------------------

MODEL_PATH = "yolov8s.pt"


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
# LOAD MODEL
# -----------------------------

model = YOLO(MODEL_PATH)

# -----------------------------
# ANOTACE
# -----------------------------

for brand, folder in INPUT_FOLDERS.items():

    class_id = CLASS_MAP[brand]

    for img_name in os.listdir(folder):

        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(folder, img_name)

        results = model(img_path)

        label_lines = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes.xywhn.cpu().numpy():
                x, y, w, h = box
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