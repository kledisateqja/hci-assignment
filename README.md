# Evoluzione degli Anime nel tempo
## Assignment HCI per l’anno accademico 2025–2026

### Giulia Zenoni, Kledisa Teqja

## Introduzione
L’obiettivo di questo progetto è la realizzazione di un sistema in grado di supportare **analisi e visualizzazioni** dedicate al mondo degli anime nel corso degli anni, rivolto sia agli **appassionati** sia ai **giornalisti**.

Per il progetto viene fornito un insieme di dati, organizzato in file **CSV**, che descrive diversi aspetti degli anime nel tempo.


---

## Dataset
Il dataset da analizzare è composto dai seguenti file:

- **characters.csv**: 209.963 dettagli sui personaggi  
- **character_anime_works.csv**: 236.816 associazioni tra personaggi e opere anime  
- **character_nicknames.csv**: 37.080 soprannomi dei personaggi  
- **details.csv**: 28.955 dettagli sugli anime  
- **favs.csv**: 4.178.747 preferenze (like) degli utenti  
- **person_alternate_names.csv**: 20.465 nomi alternativi di persone (es. doppiatori, artisti)  
- **person_anime_works.csv**: 458.091 ruoli di persone nelle opere anime (es. sigle, staff)  
- **person_details.csv**: 76.699 dettagli sulle persone  
- **person_voice_works.csv**: 489.516 lavori di doppiaggio  
- **profiles.csv**: 337.155 dettagli dei profili utente  
- **ratings.csv**: 124.298.357 valutazioni assegnate dagli utenti  
- **recommendations.csv**: 105.249 raccomandazioni tra utenti  
- **stats.csv**: 28.955 statistiche utente (rating, numero di serie completate, ecc.)

---

## Gestione e pianificazione del lavoro
L’obiettivo è creare uno o più **Jupyter Notebook** che consentano a fan e giornalisti di esplorare i dati sugli anime attraverso processi di **pulizia, analisi e visualizzazione**.

Il progetto deve essere strutturato con un approccio **user-centric**, tenendo conto delle esigenze degli utenti finali.  
Alcuni esempi di analisi possibili includono:

- **Evoluzione storica della produzione**: quanti anime vengono prodotti e come si distribuiscono per genere nel tempo
- **Confronto tra produzione e grandimento**: i generi più prodotti sono anche quelli più apprezzati dai fan?
- **Popolarità vs qaulità percepita**: un anime molto seguito non è necessariamente quello con rating più altro
- **Comportamento degli utenti**: quali sono i titoli completati, abbandonati, pianificati
- **Community Globale**: dove si contrano geograficamente gli utenti e come cresce la community nel tempo
- **Industria e professioni**: chi lavora nell'industria anime, da quali apesi provengono

---
## Struttura del notebook
Il notebook **sotrytelling.ipynb** racconta l'ecosistema anime in 11 Capitoli:
1. **La crescita della produzione**
2. **Dalla produzione alla valutazione**
3. **Le origini narrative**
4. **Popolarità e impatto culturale**
5. **I personaggi**
6. **I doppiatori e le lingue**
7. **Community anime nel mondo**
8. **Persone e ruoli nell'industria**
9. **Come sono seguiti gli anime**
10. **Il pubblico target**
11. **Conclusione**

---

## Requisiti
Lo scopo del lavoro è offrire a fan e giornalisti la possibilità di **accedere, esplorare e comprendere i dati sugli anime**.  
È richiesto di progettare uno o più **Jupyter Notebook** che permettano di:

- pulire i dati (*data cleaning*)
- analizzarli
- visualizzarli in modo efficace.

---

## Struttura del progetto

```
hci-assignment/
│
├── dataset/                        # Cartella dati (da creare manualmente, non in git)
│   ├── raw/                        # File CSV originali da caricare qui
│   └── cleaned/                    # File CSV puliti, generati dai notebook di pulizia
│
├── solution/
│   ├── pulizia/                    # Notebook di data cleaning (uno per file CSV)
│   │   ├── characters.ipynb
│   │   ├── character_nicknames.ipynb
│   │   ├── clean_character_anime_works.ipynb
│   │   ├── clean_person_alternate_names.ipynb
│   │   ├── clean_person_anime_works.ipynb
│   │   ├── clean_person_details.ipynb
│   │   ├── clean_person_voice_works.ipynb
│   │   ├── clean_profiles.ipynb
│   │   ├── details.ipynb
│   │   ├── favs.ipynb
│   │   ├── ratings.ipynb
│   │   ├── recommendations.ipynb
│   │   └── stats.ipynb
│   │
│   ├── notebook/
│   │   └── storytelling.ipynb      # Notebook principale: analisi e visualizzazioni
│   │
│   └── utils/
│       ├── charts.py               # Funzioni di supporto per la creazione dei grafici
│       └── utils.py                # Funzioni di utilità condivise
│
├── README.md
└── .gitignore
```

---


## Build

## Setup e Virtual Environment
Questo progetto utilizza un **virtual environment Python** standard per mantenere isolate le dipendenze.

### 1. Creazione del virtual environment
Si consiglia di chiamare l’ambiente `.venv` (di solito nascosto dai file explorer e ignorato da Git, evitando così di inserirlo nel repository).

```bash
# Nella directory principale del progetto
python -m venv .venv 
```
## Attivazione dell'ambiente
Utilizzare il comando appropriato in base al sistema operativo:

```bash
# Linux / macOS / git bash / WSL
source .venv/bin/activate
```
```bash
# Windows / PowerShell / CMD
.venv\Scripts\activate.bat
```
## Disattivazione
Lo stesso comando vale per tutte le piattaforme:
```bash
deactivate
```

## (Alternativa) Configurare PyCharm per usare .venv
In alternativa ai passaggi precedenti, è possibile configurare PyCharm per utilizzare direttamente il virtual environment.
```
Percorso:
File → Settings → Interpreter → Add Interpreter → Add Local Interpreter
```
A questo punto è possibile:
 - creare un nuovo ambiente,
 - oppure selezionare un .venv già esistente.

Dopo aver riavviato l’IDE, l’ambiente sarà attivo e pronto all’uso.

## Run

Segui i passaggi in ordine per avviare correttamente il progetto.

### 1. Creare la struttura delle cartelle

Prima di tutto, crea la cartella `dataset` nella root del progetto con le due sottocartelle necessarie:

```bash
mkdir -p dataset/raw
mkdir -p dataset/cleaned
```

- `dataset/raw` -> conterrà i file CSV originali (dati grezzi)
- `dataset/cleaned` -> verrà popolata automaticamente dai notebook di pulizia

### 2. Caricare i dati grezzi

Copia i file `.csv` originali del dataset all'interno della cartella `dataset/raw`.  
Assicurati che tutti i file elencati nella sezione [Dataset](#dataset) siano presenti prima di procedere.

### 3. Eseguire i notebook di pulizia

Apri ed esegui **tutti i notebook** (`.ipynb`) presenti nella cartella `solution/pulizia/`.  
Questi notebook si occupano di pulire e normalizzare i dati, producendo i file `.csv` elaborati nella cartella `dataset/cleaned/`.

> Questo passaggio è obbligatorio: il notebook di analisi e storytelling dipende dai file puliti generati qui.

### 4. Aprire il notebook principale

Una volta completata la pulizia, apri ed esegui il notebook **`storytelling.ipynb`**.

