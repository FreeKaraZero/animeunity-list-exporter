#!/usr/bin/env python3
"""
AnimeUnity to MyAnimeList/AniList Exporter
------------------------------------------
Autore: FreeKaraZero (Karabbina)

L'ho creato per una necessità puramente egoistica: mi rifiuto di aggiornare
a mano decine di anime solo perché AnimeUnity non ha un tasto "Esporta". 
Questo script raschia l'HTML salvato e mi genera un XML a prova di bomba per MAL.

Ho previsto due strade:
1. Doppio click (o senza argomenti): Apre la UI per chi non mastica i terminali.
2. Da terminale: Modalità hacker pura, con log in tempo reale.
"""

import sys
import argparse
import json
import re
import time
import threading
from typing import List, Dict, Optional, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Le mie dipendenze. Assicuratevi di aver fatto pip install
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- LE MIE CONFIGURAZIONI ---
ANILIST_API_URL = 'https://graphql.anilist.co'

# Ho compilato queste regex per piallare via la sporcizia che i siti italiani
# mettono nei titoli (tipo "[1080p]" o "(SUB ITA)"). Compilarle prima mi fa risparmiare cicli.
CLEANUP_PATTERNS = [
    re.compile(r'\[.*?\]'),  
    re.compile(r'\(\s*(ITA|SUB\s*ITA|DUB|SUB)\s*\)', re.IGNORECASE), 
    re.compile(r'\s+'), 
]

# Setto il tema della UI per adattarsi al sistema. Il Dark Mode è d'obbligo.
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 


# ==========================================
# 1. IL MOTORE (La logica cruda)
# ==========================================

def clean_title_for_api(title: str) -> str:
    """Faccio passare il titolo tra le mie regex per ripulirlo per bene."""
    c_title = title
    for pattern in CLEANUP_PATTERNS:
        c_title = pattern.sub(' ', c_title)
    return c_title.strip()

def get_title_variations(clean_title: str) -> List[str]:
    """
    Visto che spesso si inventano sottotitoli inesistenti, qui genero delle varianti.
    Se c'è un due punti o un trattino, spezzo la stringa e provo a cercare
    solo il franchise principale, sennò l'API di AniList mi rimbalza.
    """
    variations = [clean_title]
    
    if ':' in clean_title:
        variations.append(clean_title.split(':')[0].strip())
    if '-' in clean_title:
        variations.append(clean_title.split('-')[0].strip())
        
    no_parentheses = re.sub(r'\(.*?\)', '', clean_title).strip()
    if no_parentheses and no_parentheses not in variations:
        variations.append(no_parentheses)
        
    return variations

def parse_animeunity_html(html_file: str) -> List[Dict[str, Any]]:
    """Vado di BeautifulSoup per fare scraping offline del mio stesso file HTML."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except IOError:
        return []

    anime_list = []
    
    # Mi ciclo tutte le sezioni (Plan to watch, Completed...)
    for sec in soup.find_all('div', class_='list-section'):
        status_tag = sec.find('h3', class_='list-title')
        if not status_tag: 
            continue
            
        status = 'Plan to Watch' if status_tag.text.strip().lower() == 'plan to watch' else status_tag.text.strip()
            
        for entry in sec.find_all('div', class_='entry-card'):
            title_tag = entry.find('div', class_='title')
            progress_tag = entry.find('div', class_='progress')
            score_tag = entry.find('div', class_='score')
            
            # Qui gestisco gli episodi. Spesso è formattato come "12/24", a me serve solo il "12"
            p_text = progress_tag.text.strip() if progress_tag else "0"
            watched = p_text.split('/')[0] if '/' in p_text else p_text
            score = score_tag.find('div').text.strip() if (score_tag and score_tag.find('div')) else "0"
                    
            anime_list.append({
                'title': title_tag.text.strip() if title_tag else "Sconosciuto",
                'watched': watched,
                'score': score,
                'status': status
            })
            
    return anime_list

def query_anilist(search_term: str) -> Optional[int]:
    """Sparo una query GraphQL alle API di AniList."""
    query = '''query ($search: String) { Media (search: $search, type: ANIME) { idMal } }'''
    try:
        # Metto un timeout sennò se cade la rete mi rimane il thread appeso per sempre
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': {'search': search_term}}, timeout=10)
        
        if response.status_code == 200:
            media = response.json().get('data', {}).get('Media')
            return media.get('idMal') if media else None
            
        elif response.status_code == 429:
            # Mi hanno limitato. Leggo l'header, mi metto in pausa e poi ci riprovo.
            attesa = int(response.headers.get('Retry-After', 60))
            time.sleep(attesa)
            return query_anilist(search_term) 
            
    except RequestException:
        pass 
    return None

def get_mal_id_smart(title: str) -> Optional[int]:
    """La mia funzione furba: testo tutte le varianti finché non faccio match."""
    clean_title = clean_title_for_api(title)
    variations = get_title_variations(clean_title)
    
    for variant in variations:
        mal_id = query_anilist(variant)
        if mal_id: 
            return mal_id
        # Rispetto il rate limit tra un tentativo e l'altro per non farmi bannare l'IP
        time.sleep(0.4) 
        
    return None

def generate_robust_xml(anime_list: List[Dict[str, Any]], output_file: str) -> None:
    """Costruisco l'albero XML a mano con ElementTree. Zero bug con i caratteri speciali."""
    root = ET.Element("myanimelist")
    
    myinfo = ET.SubElement(root, "myinfo")
    ET.SubElement(myinfo, "user_id").text = "12345"
    ET.SubElement(myinfo, "user_name").text = "ImportUser"
    ET.SubElement(myinfo, "user_export_type").text = "1"
    ET.SubElement(myinfo, "user_total_anime").text = str(len(anime_list))

    for anime in anime_list:
        anime_node = ET.SubElement(root, "anime")
        ET.SubElement(anime_node, "series_animedb_id").text = str(anime.get("mal_id", 0))
        ET.SubElement(anime_node, "series_title").text = anime["title"]
        ET.SubElement(anime_node, "series_type").text = "TV"
        ET.SubElement(anime_node, "series_episodes").text = "0"
        ET.SubElement(anime_node, "my_id").text = "0"
        ET.SubElement(anime_node, "my_watched_episodes").text = str(anime["watched"])
        ET.SubElement(anime_node, "my_start_date").text = "0000-00-00"
        ET.SubElement(anime_node, "my_finish_date").text = "0000-00-00"
        ET.SubElement(anime_node, "my_rated").text = ""
        ET.SubElement(anime_node, "my_score").text = str(anime["score"])
        ET.SubElement(anime_node, "my_status").text = anime["status"]
        ET.SubElement(anime_node, "update_on_import").text = "1"

    # Genero l'XML indentato per renderlo umano
    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="    ")
    
    with open(output_file, "w", encoding="utf-8") as f:
        # Piallo via le righe vuote di troppo che genera minidom
        f.write('\n'.join([line for line in xml_str.split('\n') if line.strip()]))


# ==========================================
# 2. INTERFACCIA GRAFICA (Per l'utente medio)
# ==========================================

class AnimeUnityExporterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AnimeUnity List Exporter")
        self.geometry("500x350")
        self.resizable(False, False)

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="AnimeUnity Exporter 🚀", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        self.subtitle_label = ctk.CTkLabel(self.main_frame, text="Esporta la tua lista HTML in formato XML per MAL/AniList", font=ctk.CTkFont(size=12))
        self.subtitle_label.pack(pady=(0, 20))

        self.select_button = ctk.CTkButton(self.main_frame, text="Seleziona File HTML", command=self.avvia_esportazione, font=ctk.CTkFont(size=14, weight="bold"), height=45)
        self.select_button.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, mode="indeterminate")
        self.progress_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=12))

    def avvia_esportazione(self):
        file_path = filedialog.askopenfilename(
            title="Seleziona la tua lista AnimeUnity (File HTML)",
            filetypes=[("HTML Files", "*.html"), ("Tutti i file", "*.*")]
        )
        if not file_path:
            return

        self.select_button.configure(state="disabled")
        self.progress_label.configure(text="Estrazione dati e comunicazione con AniList...\nQuesto processo richiederà alcuni minuti.")
        self.progress_label.pack(pady=(15, 5))
        self.progress_bar.pack(pady=5, fill="x", padx=40)
        self.progress_bar.start()

        # Isolo il processo in un thread separato. Se non lo faccio, l'UI di Tkinter
        # mi blocca tutta la finestra finché non finisce di elaborare.
        threading.Thread(target=self.processa_file, args=(file_path,), daemon=True).start()

    def processa_file(self, file_path: str):
        """Il processo in background vero e proprio."""
        raw_anime_list = parse_animeunity_html(file_path)
        
        if not raw_anime_list:
            self.ripristina_ui()
            messagebox.showerror("Errore", "Nessun anime trovato.\nSicuro di aver preso l'HTML giusto?")
            return

        success_list = []
        orphans = []

        for anime in raw_anime_list:
            mal_id = get_mal_id_smart(anime['title'])
            if mal_id:
                anime['mal_id'] = mal_id
                success_list.append(anime)
            else:
                # Quelli che non matchano me li salvo a parte
                orphans.append({
                    "original_title": anime['title'], 
                    "status": anime['status'], 
                    "watched": anime['watched']
                })
            time.sleep(0.6)

        if success_list: 
            generate_robust_xml(success_list, "import_mal.xml")
        if orphans:
            with open("orphans.json", 'w', encoding='utf-8') as f:
                json.dump(orphans, f, indent=4, ensure_ascii=False)

        self.ripristina_ui()

        msg = f"Esportazione Completata!\n\n✔ Salvati {len(success_list)} anime in 'import_mal.xml'\n"
        if orphans: 
            msg += f"⚠ {len(orphans)} titoli non trovati (controlla 'orphans.json')."
        messagebox.showinfo("Finito!", msg)

    def ripristina_ui(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.select_button.configure(state="normal")


# ==========================================
# 3. INTERFACCIA A RIGA DI COMANDO (La mia preferita)
# ==========================================

def avvia_cli(file_path: str, output_file: str, json_file: str):
    """Modalità terminale cruda, così posso scrivermi i log in tempo reale."""
    print(f"\n🚀 [INIT] AnimeUnity Exporter CLI Mode")
    print(f"[*] Analisi del file: {file_path}")
    
    raw_anime_list = parse_animeunity_html(file_path)
    
    if not raw_anime_list:
        print("[!] ERRORE: Nessun anime trovato. HTML non valido.")
        sys.exit(1)
        
    print(f"[*] Trovati {len(raw_anime_list)} anime. Inizio match con AniList...\n")
    
    success_list = []
    orphans = []
    
    for anime in raw_anime_list:
        # Formatto l'output così è incolonnato decentemente sul terminale
        print(f" -> Cerco: {anime['title'][:40].ljust(45)} ... ", end="", flush=True)
        mal_id = get_mal_id_smart(anime['title'])
        
        if mal_id:
            print(f"[ TROVATO ] (ID: {mal_id})")
            anime['mal_id'] = mal_id
            success_list.append(anime)
        else:
            print(f"[ DISPERSO ]")
            orphans.append(anime)
            
        time.sleep(0.6)
        
    if success_list:
        generate_robust_xml(success_list, output_file)
        print(f"\n[+] SUCCESS: Generato XML per {len(success_list)} anime in '{output_file}'")
        
    if orphans:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(orphans, f, indent=4, ensure_ascii=False)
        print(f"[-] WARNING: {len(orphans)} anime non trovati. Dettagli in '{json_file}'")


# ==========================================
# 4. ENTRY POINT
# ==========================================

if __name__ == "__main__":
    # Il bivio: vedo come mi hanno lanciato lo script.
    if len(sys.argv) > 1:
        # Se c'è un file passato come argomento, vado di CLI
        parser = argparse.ArgumentParser(description="Esporta la lista AnimeUnity in XML per MyAnimeList/AniList.")
        parser.add_argument("input_html", help="Il file HTML scaricato dal profilo")
        parser.add_argument("-o", "--output", default="import_mal.xml", help="Nome del file XML in uscita")
        parser.add_argument("-j", "--json", default="orphans.json", help="Dove butto gli orfani")
        args = parser.parse_args()
        
        avvia_cli(args.input_html, args.output, args.json)
    else:
        # Nessun argomento (es. doppio click sull'exe), faccio partire la GUI
        app = AnimeUnityExporterApp()
        app.mainloop()
