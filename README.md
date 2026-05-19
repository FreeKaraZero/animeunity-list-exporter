🇬🇧 [Read in English](#-english) | 🇮🇹 [Leggi in Italiano](#-italiano)

---

# 🇬🇧 English

# AnimeUnity List Exporter 🚀

A Python script (and standalone executable) born from a specific need: **AnimeUnity does not allow you to export your anime list in any way**. This tool bridges that gap by extracting data directly from your profile page's HTML code and converting it into a "bulletproof" XML file, 100% ready to be imported into **MyAnimeList** or **AniList**.

### ✨ New Features
- **Modern GUI & CLI:** Double-click to use the sleek graphical interface (powered by `customtkinter`), or run it via terminal for real-time hacker-style logs.
- **Smart Title Cleaner:** Automatically strips away Italian release tags (e.g., `[1080p]`, `(SUB ITA)`, `(DUB)`) to ensure maximum match rates with official databases.
- **Accurate Parsing:** Preserves your exact progress, scores, and watch statuses (Watching, Completed, Dropped, Plan to Watch).
- **Orphan Handling:** Generates an `orphans.json` file for any highly localized titles that couldn't be matched automatically.

---

### 📦 For Normal Users (No Python Required)
If you just want to export your list without dealing with code, terminals, or installations:
1. Go to the **[Releases](../../releases)** tab on the right side of this page.
2. Download the latest `.exe` for Windows (or the Linux binary).
3. Go to your AnimeUnity profile, open your Anime List.
4. Save the page as an HTML file (`Right Click -> Save As... -> Webpage, Complete` or `HTML Only`).
5. Run the downloaded exporter, select your HTML file, and let it do the magic!

---

### 🛠️ For Developers (Source Code Setup)
Make sure you have Python 3 installed. If you are on a modern Linux distribution (PEP 668), remember to use a virtual environment.

```bash
git clone https://github.com/FreeKaraZero/animeunity-list-exporter.git
cd animeunity-list-exporter

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 🚀 Usage (Terminal / CLI Mode)
To get the raw terminal output and real-time logs, pass the HTML file directly as an argument:
```bash
python animeunity_exporter.py "AnimeUnity.html" -o import_mal.xml
```

#### 🖥️ Usage (GUI Mode)
To launch the modern graphical interface directly from the source code, run it without arguments:
```bash
python animeunity_exporter.py
```

### 📥 Final Step
Grab the generated `import_mal.xml` and import it directly into [AniList](https://anilist.co/settings/import) or [MyAnimeList](https://myanimelist.net/import.php)!

<br><br>

---

# 🇮🇹 Italiano

# AnimeUnity List Exporter 🚀

Uno script in Python (ed eseguibile standalone) nato da una necessità ben precisa: **AnimeUnity non permette in alcun modo di esportare la propria lista anime**. Questo tool risolve il problema estraendo i dati direttamente dal codice HTML della pagina del tuo profilo e convertendoli in un file XML "blindato", pronto al 100% per essere importato su **MyAnimeList** o **AniList**.

### ✨ Nuove Feature
- **GUI Moderna & CLI:** Fai doppio click per usare l'elegante interfaccia grafica (basata su `customtkinter`), oppure lancialo da terminale per avere i log in tempo reale e capire esattamente cosa sta facendo il motore sotto il cofano.
- **Smart Title Cleaner:** Pialla via in automatico i tag di release italiani (es. `[1080p]`, `(SUB ITA)`, `(DUB)`) per massimizzare la probabilità di match con i database ufficiali.
- **Parsing Accurato:** Preserva alla perfezione il tuo progresso, i voti e lo stato (Watching, Completed, Dropped, Plan to Watch).
- **Gestione Orfani (Orphan Handling):** Genera un file `orphans.json` per quei titoli così pesantemente localizzati o tradotti in italiano da non poter essere abbinati in automatico dalle API.

---

### 📦 Per Utenti Normali (Non serve Python)
Se vuoi solo esportare la tua lista senza impazzire con codice, terminali o installazioni:
1. Vai nella scheda **[Releases](../../releases)** sulla destra di questa pagina.
2. Scarica l'ultimo `.exe` per Windows (o il binario per Linux).
3. Vai sul tuo profilo AnimeUnity, apri la tua Anime List.
4. Salva la pagina come file HTML (`Tasto Destro -> Salva con nome... -> Pagina Web, Completa` o `Solo HTML`).
5. Avvia l'eseguibile appena scaricato, seleziona il tuo file HTML e fagli fare la magia!

---

### 🛠️ Per Sviluppatori (Setup dal Codice Sorgente)
Assicurati di avere Python 3 installato. Se sei su una distribuzione Linux moderna (PEP 668), ricordati di usare un virtual environment per evitare che il gestore pacchetti ti urli contro.

```bash
git clone https://github.com/FreeKaraZero/animeunity-list-exporter.git
cd animeunity-list-exporter

# Crea e attiva il virtual environment
python -m venv .venv
source .venv/bin/activate  # Su Windows usa: .venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt
```

#### 🚀 Utilizzo (Modalità Terminale / CLI)
Per avere l'output crudo sul terminale e i log della comunicazione API in tempo reale, passa il file HTML direttamente come argomento:
```bash
python animeunity_exporter.py "AnimeUnity.html" -o import_mal.xml
```

#### 🖥️ Utilizzo (Modalità GUI)
Per lanciare l'interfaccia grafica moderna direttamente dal codice sorgente, eseguilo semplicemente senza parametri:
```bash
python animeunity_exporter.py
```

### 📥 Step Finale
Prendi il file `import_mal.xml` appena generato e importalo direttamente su [AniList](https://anilist.co/settings/import) o [MyAnimeList](https://myanimelist.net/import.php)!
