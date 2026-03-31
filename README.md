# CarSquareDetection

Webová aplikace pro detekci a klasifikaci značek automobilů (Škoda, Audi, Volkswagen) pomocí modelu Ultralytics YOLO. Nahraj fotku auta a aplikace ti řekne, o jakou značku se jedná.

## 🌐 Online verze

Aplikace běží na hostingu [Render](https://render.com) a je přístupná odkudkoliv bez nutnosti instalace:

**[https://carsquaredetection.onrender.com](https://carsquaredetection.onrender.com)**

> Poznámka: Render při nečinnosti uspí free instanci – první načtení může trvat ~30 sekund.

---

## 🚀 Spuštění na jiném PC (krok po kroku)

Před začátkem se ujisti, že máš nainstalované:

- **Python 3.10 nebo 3.11** – stáhnout na [python.org](https://www.python.org/downloads/)  
  *(při instalaci zaškrtni „Add Python to PATH")*
- **Git** – stáhnout na [git-scm.com](https://git-scm.com/)

Pak stačí 4 příkazy v terminálu:

```bash
git clone https://github.com/AlbertSch8/CarSquareDetection.git
cd CarSquareDetection
pip install -r requirements.txt
python app.py
```

Po spuštění otevři v prohlížeči adresu:

```
http://127.0.0.1:5000
```

Ukončení aplikace: `Ctrl + C`

---

## 🚗 Funkce projektu

- rozpoznávání značky auta ze fotky (Škoda / Audi / Volkswagen)
- webové rozhraní postavené na Flasku
- detekce pomocí vlastního YOLO modelu (`best.pt`)
- automatická anotace obrázků a generování YOLO datasetu
- podpora trénovací pipeline

---

## 📁 Struktura projektu

```
projekt/
│
├── app.py                  # Flask webová aplikace
├── annotator.py            # Skript pro automatickou anotaci
├── best.pt                 # Natrénovaný YOLO model
├── requirements.txt        # Seznam závislostí
├── templates/
│   └── index.html          # Šablona webového rozhraní
├── obrazky_skoda/          # Trénovací obrázky Škoda
├── obrazky_audi/           # Trénovací obrázky Audi
├── obrazky_volkswagen/     # Trénovací obrázky Volkswagen
└── anotace_aut/            # Vygenerovaný YOLO dataset
    ├── images/
    └── labels/
```

---

## ⚙️ Generování datasetu (volitelné)

Pokud chceš sám vygenerovat anotace z obrázků ve složkách `obrazky_*/`, spusť:

```bash
python annotator.py
```

Skript:
1. načte YOLO model
2. detekuje auta na obrázcích
3. přiřadí značku podle složky
4. vytvoří YOLO anotace do složky `anotace_aut/`

---

## 🏷 Mapování tříd

| ID | Značka     |
|----|------------|
| 0  | Škoda      |
| 1  | Audi       |
| 2  | Volkswagen |

---

## 🧾 Formát anotací (YOLO)

```
class x_center y_center width height
```

Příklad:
```
1 0.52 0.44 0.31 0.21
```

Souřadnice jsou normalizované v rozsahu 0–1.
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