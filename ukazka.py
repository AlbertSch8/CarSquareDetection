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

CAR_CLASS_ID = 2   # COCO class for "car"
CONF_THRESHOLD = 0.4

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
# ANNOTATION FUNCTION
# -------------------------

def annotate_image(img_path, label):

    img = cv2.imread(img_path)

    results = model(img)

    for r in results:

        if r.boxes is None:
            continue

        for box in r.boxes:

            class_id = int(box.cls.item())
            conf = float(box.conf.item())

            # filtr pouze auta
            if class_id != CAR_CLASS_ID or conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

            text = f"{label} {conf:.2f}"

            cv2.putText(
                img,
                text,
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
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


print("Hotovo ✔ Ukázky jsou ve složce:", OUTPUT)