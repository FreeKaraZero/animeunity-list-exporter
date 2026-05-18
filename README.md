# AnimeUnity List Exporter 🚀

A Python script born from a specific need: **AnimeUnity does not allow you to export your anime list in any way**. This tool bridges that gap by extracting data directly from your profile page's HTML code and converting it into a "bulletproof" XML file, 100% ready to be imported into **MyAnimeList** or **AniList**.

### 🛑 Why use this script?
Since there is no native export feature on the platform, this script is the only alternative to securely back up your list without having to manually re-enter dozens of titles. Furthermore, direct extraction avoids the typical issues found in generic automatic parsers:
- **No truncated titles:** It prevents long names from being cut off with ellipses, ensuring that different seasons are not overwritten or merged together in the database.
- **Accurate statuses and progress:** Perfectly preserves the separation between currently watching (Watching), completed (Completed), dropped (Dropped), or planning to watch (Plan to Watch), along with your scores and exact episode counts.

### ✨ Features
- Accurate parsing using `BeautifulSoup` on your profile's raw HTML structure.
- Smart matching with the AniList GraphQL API to fetch the official corresponding `MAL_ID`s.
- Automatic Rate Limit handling (the script automatically sleeps if the API throttles connections, avoiding crashes).
- Generates a separate `orphans.json` file for anime that require manual addition due to heavy localizations or missing matches.

### 🛠️ Installation
Make sure you have Python 3 installed on your system. Clone the repository and install the dependencies:

```bash
git clone [https://github.com/FreeKaraZero/animeunity-list-exporter.git](https://github.com/FreeKaraZero/animeunity-list-exporter.git)
cd animeunity-list-exporter
pip install -r requirements.txt
```

### 🚀 Usage
1. Open your browser and go to your AnimeUnity profile, specifically inside the **Anime List** section.
2. **Download the page as an HTML file:** Right-click on any empty space on the page, select `Save As...` (or `Save Page As...`), and make sure to save the file to your computer as **"Webpage, Complete"** or **"HTML Only"**.
3. Move the downloaded HTML file inside the project folder.
4. Run the script by passing the filename as an argument:

```bash
python animeunity2mal.py "AnimeUnity.html" -o my_export_list.xml
```
5. Grab the generated `my_export_list.xml` and import it directly into [AniList](https://anilist.co/settings/import) or MyAnimeList!
