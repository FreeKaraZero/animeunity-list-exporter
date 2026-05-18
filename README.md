# AnimeUnity List Exporter 🚀

[🇮🇹 Leggi in Italiano](#-italiano) | [🇬🇧 Read in English](#-english)

---

## 🇮🇹 Italiano

Uno script Python per estrarre la propria lista anime direttamente dal codice HTML del profilo di **AnimeUnity** e convertirla in un file XML "corazzato", pronto al 100% per essere importato su **MyAnimeList** o **AniList**.

### 🛑 Perché usare questo script e non l'export nativo?
Se hai provato a usare la funzione di esportazione XML integrata sul sito, avrai notato che il file generato è decisamente problematico. 
Questo script risolve i seguenti bug critici dell'export nativo:
- **Titoli troncati:** Il sito taglia i nomi lunghi con i puntini di sospensione (`...`). Se hai due stagioni con un nome molto lungo (es. *Attack on Titan Specials*), il database nativo le fonde insieme e cancella letteralmente degli anime dalla tua lista.
- **Stati sballati:** Il sistema nativo sposta spesso anime che avevi in "Plan to Watch" o "Dropped" direttamente nei "Watching", rovinando le tue statistiche complessive.

### ✨ Funzionalità
- Parsing preciso usando `BeautifulSoup` sull'HTML reale del tuo profilo.
- Matching intelligente con l'API GraphQL di AniList per recuperare i `MAL_ID` ufficiali.
- Gestione automatica dei Rate Limit (lo script si mette in pausa se il server si arrabbia, evitando crash).
- Generazione di un file `orphans.json` separato per gli anime che richiedono un'aggiunta manuale a causa di titoli troppo localizzati o non trovati.

### 🛠️ Installazione
Assicurati di avere Python 3 installato sul tuo sistema. Clona il repository e installa le dipendenze:
```bash
git clone https://github.com/FreeKaraZero/animeunity-list-exporter.git
cd animeunity-list-exporter
pip install -r requirements.txt
