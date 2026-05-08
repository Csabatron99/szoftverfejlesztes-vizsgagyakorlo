# Szoftverfejlesztés Vizsgagyakorló

Interaktív vizsgafelkészítő alkalmazás szoftverfejlesztés témakörökből. Python + CustomTkinter alapú asztali GUI app, sötét módban.

## Tartalom

360 kérdés, 18 kategóriában, minden kategóriában 20 kérdés:

| Kategória | Témakör |
|---|---|
| Design patterns | GoF tervezési minták |
| Haladó Java | Lambda, stream, Optional, funkcionális interfészek |
| Java alapok | Nyelvi alapok, típusok, OOP |
| Java annotációk | Beépített és egyéni annotációk |
| Java SE/JDK újdonságok | Records, sealed classes, pattern matching, text blocks |
| Javadoc | Dokumentációs kommentek, tagek |
| JUnit és kódlefedettség | JUnit 5, tesztírás, lefedettség |
| Kódolvasás | Kód értelmezési feladatok |
| Maven és build rendszerek | Maven, pom.xml, életciklus |
| OOP tervezési alapelvek | DRY, KISS, YAGNI, SoC, csatoltság, Demeter-törvény |
| SOLID / OOP alapelvek | SRP, OCP, LSP, ISP, DIP |
| Sebezhetőségek | OWASP Top 10, biztonsági alapfogalmak |
| Szoftverfejlesztési alapfogalmak | SDLC, módszertanok, alapfogalmak |
| TDD | Test-Driven Development elvek és gyakorlat |
| Tesztelés | Teszttípusok, stratégiák |
| Tiszta kód | Clean Code elvek, refaktorálás |
| UML | Osztály-, szekvencia- és egyéb diagramok |
| Verziózás | Git alapok, branching, workflow-k |

**Kérdéstípusok:** egyválasztós, többválasztós, igaz/hamis, kódolvasás

**Kvíz módok:** kategória szerinti, véletlenszerű vegyes, nehézség szerinti

## Előfeltételek

- Python 3.11 vagy újabb
- pip

## Telepítés és futtatás

### Windows

```powershell
git clone https://github.com/Csabatron99/szoftverfejlesztes-vizsgagyakorlo.git
cd szoftverfejlesztes-vizsgagyakorlo/exam_trainer

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

### macOS / Linux

```bash
git clone https://github.com/Csabatron99/szoftverfejlesztes-vizsgagyakorlo.git
cd szoftverfejlesztes-vizsgagyakorlo/exam_trainer

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 main.py
```

> **Linux megjegyzés:** A CustomTkinter `tkinter`-t igényel. Ha hiányzik, telepítsd:
> - Ubuntu/Debian: `sudo apt install python3-tk`
> - Fedora: `sudo dnf install python3-tkinter`
> - Arch: `sudo pacman -S tk`

## Standalone .exe build (csak Windows)

A build PyInstallert használ és egyetlen `.exe` fájlt készít.

```powershell
# A venv aktiválása szükséges (pip install -r requirements.txt már lefutott)
.\build.ps1
```

Az elkészült fájl helye: `dist\SzoftverfejlesztesVizsgagyakarlo.exe`

Az `.exe` mellé kerül a `stats.json` (statisztikák) az első futtatáskor.

## Projektstruktúra

```
exam_trainer/
├── main.py                          # Belépési pont
├── app.py                           # Főablak, képernyőváltás
├── config.py                        # Beállítások, konstansok
├── models.py                        # Adatmodellek (Question, QuizResult)
├── question_manager.py              # Kérdések betöltése, szűrése
├── stats_manager.py                 # Statisztikák mentése/betöltése
├── requirements.txt                 # Python függőségek
├── build.ps1                        # Windows .exe build szkript
├── SzoftverfejlesztesVizsgagyakarlo.spec  # PyInstaller spec
├── data/
│   ├── questions.json               # Kérdésbank (360 kérdés)
│   └── stats.json                   # Felhasználói statisztikák (gitignore-olt)
└── ui/
    ├── home_screen.py               # Főképernyő
    ├── category_screen.py           # Kategóriaválasztó
    ├── quiz_screen.py               # Kvíz játékképernyő
    ├── result_screen.py             # Eredmények
    └── code_widget.py               # Kódmegjelenítő widget
```

## Függőségek

| Csomag | Verzió | Leírás |
|---|---|---|
| customtkinter | ≥ 5.2.2 | Modern dark-mode GUI keretrendszer |
| pyinstaller | ≥ 6.0.0 | Standalone .exe build (opcionális) |
