import os
import io
import base64
from pathlib import Path

from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)

MODEL_PATH = Path(__file__).parent / "best.pt"
model = YOLO(str(MODEL_PATH))

CLASS_NAMES = {
    0: "Škoda",
    1: "Audi",
    2: "Volkswagen",
}

BRAND_COLORS = {
    0: (0, 180, 0),      # Škoda – zelená
    1: (200, 0, 0),      # Audi – červená
    2: (0, 100, 220),    # Volkswagen – modrá
}

MAX_UPLOAD_MB = 10
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def run_inference(image_bytes: bytes):
    """Spustí model na obrázku a vrátí anotovaný obrázek + výsledky."""
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return None, []

    results = model(img, verbose=False)

    detections = []

    for r in results:
        if r.boxes is None:
            continue
        for box in r.boxes:
            class_id = int(box.cls.item())
            conf = float(box.conf.item())
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            brand = CLASS_NAMES.get(class_id, "neznámé")
            color = BRAND_COLORS.get(class_id, (255, 255, 255))

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            label = f"{brand}  {conf * 100:.0f} %"

            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(img, (x1, y1 - th - 12), (x1 + tw + 8, y1), color, -1)
            cv2.putText(img, label, (x1 + 4, y1 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            detections.append({"brand": brand, "confidence": round(conf * 100, 1)})

    _, buf = cv2.imencode(".jpg", img)
    img_b64 = base64.b64encode(buf).decode("utf-8")
    return img_b64, detections


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Nebyl nahrán žádný soubor."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nebyl vybrán žádný soubor."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Nepodporovaný formát. Nahraj JPG, PNG nebo WEBP."}), 400

    image_bytes = file.read()
    img_b64, detections = run_inference(image_bytes)

    if img_b64 is None:
        return jsonify({"error": "Nepodařilo se načíst obrázek."}), 400

    if not detections:
        return jsonify({
            "image": img_b64,
            "detections": [],
            "message": "Na obrázku nebylo rozpoznáno žádné auto ze skupiny Škoda / Audi / Volkswagen.",
        })

    return jsonify({
        "image": img_b64,
        "detections": detections,
        "message": None,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
