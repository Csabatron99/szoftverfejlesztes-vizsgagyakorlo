# TestTodo.md – Vizsgagyakorló Alkalmazás Fejlesztési Napló

---

## ✅ Elkészült feladatok

### 1. lépés – Projektstruktúra és futtatható skeleton

- [x] `exam_trainer/` könyvtárstruktúra létrehozva
- [x] `config.py` – konstansok, színek, fontok, tesztmódok, fájlútvonalak
- [x] `models.py` – `Question` dataclass (`is_correct`, `is_partial` metódusok)
- [x] `question_manager.py` – `QuestionManager` skeleton (load, filter, random)
- [x] `stats_manager.py` – `StatsManager` skeleton (load/save JSON)
- [x] `app.py` – `ExamTrainerApp` főablak customtkinter-rel, képernyőváltás logika
- [x] `main.py` – belépési pont
- [x] `ui/__init__.py` – ui csomag
- [x] `ui/home_screen.py` – `HomeScreen` (módválasztó gombok, statisztika preview)
- [x] `ui/category_screen.py` – `CategoryScreen` skeleton
- [x] `ui/quiz_screen.py` – `QuizScreen` skeleton (placeholder)
- [x] `ui/result_screen.py` – `ResultScreen` skeleton (placeholder)
- [x] `data/questions.json` – üres lista placeholder
- [x] `data/stats.json` – alapértelmezett statisztika struktúra
- [x] `TestTodo.md` – létrehozva és naprakész

### 2. lépés – Question modell, QuestionManager, kérdésbank

- [x] `models.py` – `Question` dataclass véglegesítve és kompatibilis a JSON struktúrával
- [x] `question_manager.py` – `load_questions`, `get_categories`, `get_by_category`, `get_by_ids`, `get_random` teljesen implementálva
- [x] `data/questions.json` – **30 kérdés** feltöltve minden kategóriából:
  - Szoftverfejlesztési alapfogalmak (5 kérdés): Library/API/Framework/SDK/IDE, WORA, JDK eszközei
  - Sebezhetőségek (4 kérdés): zero-day, CVE formátum, CVSS Critical küszöb, NVD vs CVE
  - Verziózás (3 kérdés): SemVer MAJOR/MINOR/PATCH, breaking change utáni verzió, pre-release sorrendek
  - Java annotációk (4 kérdés): @Override, @Retention, @FunctionalInterface, @Repeatable
  - Tesztelés (4 kérdés): AAA minta, @BeforeAll, FIRST elvek, 100% lefedettség mítosz
  - UML (3 kérdés): láthatóság jelölések, kompozíció vs aggregáció, absztrakt jelölés
  - SOLID / OOP alapelvek (3 kérdés): SRP, OCP, Demeter törvénye
  - Design patterns (4 kérdés): Singleton, Observer kategória, Decorator, Builder kódolvasás

---

## 🔄 Folyamatban lévő feladatok

_(jelenleg nincs aktív fejlesztés)_

---

## 📋 Hátralévő modulok

- [x] **2. lépés** – `models.py` véglegesítés, `question_manager.py` implementálás, `data/questions.json` 30 kérdéssel
- [x] **3. lépés** – `CategoryScreen` teljes implementáció, `app.py` `"category_run"` mód kezelése
- [x] **4. lépés** – `QuizScreen`: kérdésmegjelenítés, válasz gombok, keverés, következő kérdés
- [x] **5. lépés** – Pontszámítás, `ResultScreen` helyes/hibás válaszok kijelzésével
- [x] **6. lépés** – Timer, pause funkció, keyboard shortcutok
- [ ] **8. lépés** – Kérdésbank bővítése 150+ kérdésre (minden kategóriából)
- [x] **9. lépés** – Refaktorálás, hibajavítás, UI finomítás, végső ellenőrzés
- [ ] **10. lépés** – Kérdésbank bővítése hiányzó témakörökkel (Batch 7–9)
  - [ ] **Batch 7** – Tiszta kód (15–20 kérdés): milyen a tiszta kód, értelmes nevek, függvények kívánatos jellemzői
  - [ ] **Batch 8** – Java SE/JDK új lehetőségei (15–20 kérdés): switch kifejezések, szövegblokkok, rekord osztályok, pattern matching instanceof, boilerplate
  - [ ] **Batch 9** – Kódolvasás (15–20 kérdés): Java kódrészletek értelmezése, `code_reading` típusú kérdések, string/tömb műveletek, JavaFX alapok

---

## 🐛 Hibák / Javítandó részek

- ~~`CategoryScreen` `start_quiz("category_run", ...)` hívás: az `app.py`-ban a `"category_run"` mód még nincs kezelve~~ **✅ megjavítva a 3. lépésben**
- ~~`QuizScreen` placeholder~~ **✅ teljesen implementálva a 4. lépésben**
- ~~`ResultScreen` egyelőre csak placeholder-t jelenít meg~~ **✅ teljesen implementálva az 5. lépésben**

---

### 3. lépés – CategoryScreen és app.py navigáció

- [x] `app.py` – `start_quiz("category_run", category=...)` ág hozzáadva: az összes kategóriabeli kérdés lekérése (`get_random(category=cat)`, shuffle)
- [x] `ui/category_screen.py` – teljesen újraírva:
  - Fejléc: cím + alcím + összes kérdés/kategória szám megjelenítése
  - Scrollozható lista: minden kategóriának saját sor (gomb + kérdésszám badge)
  - Vissza gomb a főmenübe
  - Üreslista eset kezelve

---

### 4. lépés – QuizScreen teljes implementáció

- [x] `ui/quiz_screen.py` – teljesen újraírva:
  - Felső sáv: mód neve + „Kérdés X / N" + progress bar
  - Kategória badge + nehézség badge + kérdéstípus felirat minden kérdésnél
  - Kérdésszöveg (code_reading kérdésnél Consolas font)
  - Típus-tudatos válaszgombok: single_choice/true_false/code_reading → rádió stílus, multiple_choice → jelölős stílus
  - „Ellenőrzés" gomb → zöld/piros/sötétzöld visszajelzés + magyarázat szöveg
  - „Következő →" / „Befejezés ✓" gomb az utolsó kérdésnél
  - Eredmény dict összeállítása: total, correct, wrong_ids, results lista
  - `app.show_results(results)` hívás az utolsó kérdés után

---

### 5. lépés – ResultScreen és StatsManager.record()

- [x] `stats_manager.py` – `record(results)` metódus implementálva:
  - `total_tests` növelése, `all_percents` lista bővítése
  - `avg_percent` gördülő átlag, `best_score` max frissítés
  - `wrong_question_ids` intelligens frissítése (újonnan hibás hozzáadva, újonnan helyes eltávolítva)
  - `last_test_date` mai dátum mentése, `save_stats()` hívás
- [x] `ui/result_screen.py` – teljesen újraírva:
  - Pontszámkártya: emoji + minősítés szöveg (Kiváló/Jó/Megfelelt/Nem felelt meg) + százalék progress bar
  - Akciógombok: Főmenü, Újra (ugyanaz a mód), Hibás kérdések (disabled ha nincs hibás)
  - Scrollozható kérdés-szintű összesítő: ✅/❌ ikon, kategória badge, nehézség, kérdés előnézet

---

### 6. lépés – Timer, Pause funkció, Keyboard shortcutok

- [x] `ui/quiz_screen.py` – Timer refaktorálva és bővítve:
  - `full` mód: 90 perces **visszaszámláló** (⏱ MM:SS), fehér → narancs (<5 perc) → piros (<1 perc)
  - `quick`/`normal` mód: **eltelt idő** megjelenítése (MM:SS, szürke felirat)
  - Ha a visszaszámláló lejár: `_finish_timed_out()` → meg nem válaszolt kérdések automatikusan hibásnak számítanak → `_finish()` hívás
- [x] **Pause gomb** a felső sávban (⏸ Szünet / ▶ Folytatás):
  - `_pause()`: timer leáll, kérdés eltakarva → sötét overlay panel „Szüneteltetve" szöveggel
  - `_resume()`: overlay eltűnik, kérdés visszajelenik, timer folytatódik
- [x] **Keyboard shortcutok** (betöltéskor kötve, kilépéskor/befejezéskor levetve):
  - `1–5`: válasz ki-/bejelölése (pause alatt, vagy már ellenőrzött kérdésnél: no-op)
  - `Enter`: ellenőrzés (ha van kijelölés) / következő kérdés (ha már ellenőrizve)
  - `P` / `p`: pause/resume
  - `Esc`: `_quit_quiz()` (timer leáll, billentyűk levéve, főmenüre navigál)

---

## ➡️ Következő lépés

**8. lépés:** Kérdésbank bővítése 150+ kérdésre kis batch-ekben (max 20 kérdés egyszerre), minden kategóriából egyenletesen.

---

_Utoljára frissítve: 6. lépés befejezése után_
