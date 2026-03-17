import os
import random
from pathlib import Path
import cv2
import urllib.request

from ultralytics import YOLO

# -------------------------
# MODEL
# -------------------------

MODEL_PATH = "yolov8s.pt"

model = YOLO(MODEL_PATH)

# -------------------------
# INPUT
# -------------------------

FOLDERS = {
    "skoda": "obrazky_skoda",
    "audi": "obrazky_audi",
    "volkswagen": "obrazky_volkswagen"
}

# -------------------------
# OUTPUT
# -------------------------

OUTPUT = Path("ukazky_anotaci")
OUTPUT.mkdir(exist_ok=True)

# -------------------------
# FUNCTION
# -------------------------

def annotate_image(img_path, label):

    img = cv2.imread(img_path)

    results = model(img)

    for r in results:

        if r.boxes is None:
            continue

        for box in r.boxes:

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

            cv2.putText(
                img,
                label,
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

    return img


# -------------------------
# PROCESS
# -------------------------

for brand, folder in FOLDERS.items():

    images = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg",".jpeg",".png"))
    ]

    sample = random.sample(images, min(4, len(images)))

    for img_name in sample:

        path = os.path.join(folder, img_name)

        annotated = annotate_image(path, brand)

        out_name = f"{brand}_{img_name}"

        cv2.imwrite(str(OUTPUT / out_name), annotated)


print("Hotovo. Ukázky v:", OUTPUT)