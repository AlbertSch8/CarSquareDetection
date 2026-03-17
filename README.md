CarSquareDetection

Automatické vytváření datasetu pro detekci a klasifikaci značek automobilů (Škoda, Audi, Volkswagen) pomocí modelu Ultralytics YOLO.

Tento projekt slouží k automatické anotaci obrázků automobilů. Skript detekuje auta na obrázcích, přiřadí jim značku podle složky, ve které se obrázek nachází, a vytvoří dataset ve formátu YOLO, který lze použít pro trénování modelů počítačového vidění.

🚗 Funkce projektu

automatická detekce aut pomocí YOLO

generování YOLO datasetu

filtrace pouze objektů car

podpora značek Škoda / Audi / Volkswagen

progress bar při zpracování obrázků

kompatibilita s YOLO training pipeline

📁 Struktura projektu

Před spuštěním skriptu musí mít projekt tuto strukturu:

projekt/
│
├─ obrazky_skoda/
│   ├─ img1.jpg
│   ├─ img2.jpg
│
├─ obrazky_audi/
│   ├─ img1.jpg
│   ├─ img2.jpg
│
├─ obrazky_volkswagen/
│   ├─ img1.jpg
│   ├─ img2.jpg
│
├─ script.py
└─ README.md

Každá složka obsahuje obrázky jedné značky auta.

⚙️ Instalace

Nejprve nainstalujte potřebné knihovny:

pip install ultralytics
pip install opencv-python
pip install tqdm
▶️ Spuštění skriptu

Skript se spouští příkazem:

python script.py

Skript následně:

načte YOLO model

detekuje auta na obrázcích

přiřadí značku podle složky

vytvoří YOLO anotace

📦 Výstup datasetu

Po spuštění skriptu vznikne složka:

anotace_aut/
│
├─ images/
│   ├─ img1.jpg
│   ├─ img2.jpg
│
└─ labels/
    ├─ img1.txt
    ├─ img2.txt

Každý obrázek má odpovídající soubor s anotací.

🧾 Formát anotací

Dataset používá YOLO formát:

class x_center y_center width height

Příklad:

1 0.52 0.44 0.31 0.21

Souřadnice jsou normalizované v rozsahu 0–1.

🏷 Mapování tříd

Dataset používá následující třídy:

0 = skoda
1 = audi
2 = volkswagen

Třída se určuje podle složky, ze které obrázek pochází.

🔍 Filtrace detekcí

Model YOLO detekuje mnoho objektů, ale skript filtruje pouze:

car

V COCO datasetu má tato třída ID:

car = 2

Zároveň jsou odstraněny detekce s nízkou jistotou (confidence threshold).

📊 Progress bar

Při generování datasetu se zobrazuje průběh zpracování:

Anotuji obrázky: 63% |██████████████████▏| 1250/2000

Ukazuje:

procento dokončení

počet zpracovaných obrázků

rychlost zpracování

⚠ Omezení

model nemusí detekovat všechna auta

bounding boxy nemusí být vždy perfektní

obrázky bez detekovaného auta nejsou do datasetu přidány

🚀 Možná rozšíření projektu

Projekt lze dále rozšířit například o:

automatické oříznutí auta (crop)

rozdělení datasetu na train / validation

rychlejší zpracování pomocí batch inference

generování statistik datasetu

📄 Licence

MIT License

👨‍💻 Autor

Projekt CarSquareDetection byl vytvořen jako experimentální nástroj pro práci s datasetem automobilů a počítačovým viděním.