# Analisi di Impatto: Migrazione da GUI Desktop Python a GUI Web

## Descrizione Documento

Questo documento fornisce un’analisi di impatto completa per sostituire l’attuale GUI desktop Python (basata su Tkinter/ttkbootstrap) con un’interfaccia web moderna per il MARK Analysis Tool.

**Stato Attuale**: GUI desktop (`gui_analysis.py`) basata su Tkinter e ttkbootstrap  
**Stato Proposto**: GUI web con tecnologie leggere e adatte a sviluppo rapido  
**Complessità della Migrazione**: Media  
**Sforzo Stimato**: 2–4 settimane per un’implementazione completa

---

## 1. Analisi dell’Architettura della GUI Attuale

### 1.1 Implementazione Esistente

**Percorso**: `MARK-Tool/MARK-Tool/Categorizer/src/GUI/`

**File**:
- `gui_analysis.py` (298 righe) – Applicazione GUI principale
- `style_gui.py` (11 righe) – Configurazione dello stile

**Stack Tecnologico**:
- **Tkinter**: Libreria standard di Python per GUI
- **ttkbootstrap**: Tema moderno per widget ttk
- **Threading**: Uso di `subprocess` per task in background

### 1.2 Funzionalità Attuali della GUI

#### Tab Input:
1. **Selezione cartella Input**: Sfoglia e seleziona la cartella che contiene i repository
2. **Selezione cartella Output**: Sfoglia e seleziona la cartella dei risultati
3. **Upload CSV GitHub Repo**: CSV opzionale con elenco repository
4. **Pulsante Avvia Analisi**: Avvia il workflow di analisi

#### Tab Output:
1. **Doppio Treeview**: Vista separata dei risultati Consumatori e Produttori
2. **Elenco file CSV**: Popolato automaticamente dai risultati dell’analisi
3. **Effetti Hover**: Evidenziazione interattiva delle righe
4. **Doppio click per aprire**: Apre i CSV in nuove tab
5. **Gestione tab dinamiche**: Crea tab per la visualizzazione dei CSV
6. **Visualizzatore CSV**: Tabella con scrolling, stile foglio elettronico

#### Integrazione del Workflow:
1. Valida i percorsi e il formato CSV
2. Opzionalmente avvia il clonatore repository `cloner.py`
3. Esegue `exec_analysis.py` via subprocess
4. Mostra i risultati in tab organizzate
5. Aggiorna automaticamente l’explorer dell’output a fine analisi

### 1.3 Punti di Forza della GUI Attuale
- Autonoma, non richiede server
- Accesso diretto al file system
- Integrazione con OS (finestre di dialogo)
- Deploy semplice (solo Python)
- Funziona offline

### 1.4 Limiti della GUI Attuale
- Dipendenze di piattaforma (setup corretto Python/Tkinter)
- Stilizzazione limitata
- Non responsive e look & feel poco moderno
- Non accessibile da remoto
- Stato UI difficile da versionare
- Limitata all’ambiente desktop
- Nessun feedback di progresso in tempo reale (blocco durante l’analisi)

---

## 2. Architettura Web Proposta

### 2.1 Stack Tecnologico Scelto

#### Opzione A: Flask + HTML/CSS/JS Vanilla
- **Backend**: Flask 
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Stile**: Bootstrap 5
- **Upload File**: Gestito da Flask
 

## 3. Analisi di Impatto Dettagliata

### 3.1 File da Modificare

#### DA ELIMINARE/DEPRECARE (2 file):
```
MARK-Tool/MARK-Tool/Categorizer/src/GUI/gui_analysis.py
MARK-Tool/MARK-Tool/Categorizer/src/GUI/style_gui.py
```

#### NUOVI FILE (GUI Web):
```
    MARK-Tool/MARK-Tool/web_gui/
    ├── app.py                          # Entry point Flask
    ├── config.py                       # Configurazione
    ├── routes/
    │   ├── __init__.py
    │   ├── analysis_routes.py          # Endpoint di esecuzione analisi
    │   ├── file_routes.py              # Endpoint upload/download file
    │   └── results_routes.py           # Endpoint visualizzazione risultati
    ├── services/
    │   ├── __init__.py
    │   ├── analysis_service.py         # Ponte verso exec_analysis.py
    │   └── file_service.py             # Operazioni su file
    ├── static/
    │   ├── css/
    │   │   └── styles.css              # Stili custom
    │   ├── js/
    │   │   ├── main.js                 # Logica frontend
    │   │   ├── file-upload.js          # Upload file
    │   │   └── results-viewer.js       # Visualizzazione risultati
    │   └── uploads/                    # Cartella upload temporanei
    ├── templates/
    │   ├── base.html                   # Template base
    │   ├── index.html                  # Pagina analisi
    │   ├── results.html                # Panoramica risultati
    │   ├── csv-viewer.html             # Viewer CSV
    │   └── components/
    │       ├── navbar.html
    │       └── file-browser.html
    └── requirements.txt                # Dipendenze web
```

#### FILE DA MODIFICARE:
```
MARK-Tool/MARK-Tool/Categorizer/src/exec_analysis.py
    - Aggiungere modalità API per invocazioni programmatiche

MARK-Tool/MARK-Tool/cloner/cloner.py
   - Rendere thread-safe per ambiente web

MARK-Tool/MARK-Tool/README.md
   - Aggiornare istruzioni di installazione
   - Aggiornare esempi d’uso
```

### 3.2 Modifiche Backend Necessarie

#### 3.2.1 Modifiche a exec_analysis.py

Design attuale:
- Parsing argomenti da CLI
- Accesso diretto al file system
- Esecuzione sincrona

Modifiche richieste:
```python
class ExecAnalyzer:
    def __init__(self, input_path=None, output_path=None):
        # ... codice esistente ...
    
    def run(self):
        # Codice di analisi esistente...
    
    # NUOVO: metodo per API web
    def run_async(self):
        """Esegue l’analisi in un thread in background"""
        import threading
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        return thread
```

Impatto: BASSO – modifiche additive, retrocompatibili

#### 3.2.2 Gestione Upload File

Attuale: usa `filedialog` di Tkinter  
Nuovo: upload via web

```python
# Nuovo service: web_gui/services/file_service.py
class FileService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
    
    def handle_csv_upload(self, file):
        """Gestione upload CSV GitHub"""
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath
    
    def validate_input_folder(self, folder_path):
        """Valida la cartella input selezionata/uploadata"""
        # Logica di validazione
        pass
```

Impatto: MEDIO – nuovo componente, richiede test

### 3.3 Modifiche Frontend Necessarie

#### 3.3.1 Form Input (sostituisce Tab Input)

Struttura HTML:
```html
<form id="analysisForm" method="POST" enctype="multipart/form-data">
    <!-- Cartella Input -->
    <div class="form-group">
        <label>Percorso cartella Input</label>
        <input type="text" name="input_path" required>
        <small>Percorso contenente i repository</small>
    </div>
    
    <!-- Cartella Output -->
    <div class="form-group">
        <label>Percorso cartella Output</label>
        <input type="text" name="output_path" required>
    </div>
    
    <!-- Upload CSV GitHub -->
    <div class="form-group">
        <label>CSV Repositories GitHub (opzionale)</label>
        <input type="file" name="github_csv" accept=".csv">
    </div>
    
    <!-- Submit -->
    <button type="submit" class="btn btn-primary">Avvia Analisi</button>
</form>
```

Logica JavaScript:
```javascript
// Gestione upload e avvio
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/analysis/start', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
    } catch (error) {
        showError(error.message);
    }
});
```

Impatto: MEDIO – conversione lineare

 

#### 3.3.3 Viewer dei Risultati (sostituisce Tab Output)

Funzionalità da replicare:
1. Elenco CSV per Consumers e Producers
2. Visualizzazione CSV in tabella
3. Viste scrollabili
4. Visualizzazione multipla

Approccio di implementazione:
```javascript
// Pagina risultati
async function loadResultsList() {
    const response = await fetch('/api/results/list');
    const data = await response.json();
    
    renderFileList('consumers', data.consumers);
    renderFileList('producers', data.producers);
}

async function viewCSV(filePath) {
    const response = await fetch(`/api/results/view?file=${filePath}`);
    const data = await response.json();
    
    renderCSVTable(data.headers, data.rows);
}
```

Impatto: MEDIO – sostituzione delle funzionalità core

### 3.4 Dipendenze principali

Dipendenze minime suggerite: Flask (backend), Bootstrap/JS (frontend). La selezione e la versione delle librerie verranno confermate in fase di implementazione.

---

## 4. Matrice di Parità delle Funzionalità

| Funzionalità | Attuale (Tkinter) | Web | Note |
|--------------|--------------------|-----|------|
| Selezione cartella input | ✅ Dialog nativo | ✅ Input testo + validazione | Il file browser richiede accesso lato server |
| Selezione cartella output | ✅ Dialog nativo | ✅ Input testo + validazione | Come sopra |
| Upload CSV | ✅ Dialog file | ✅ Drag & drop | UX migliorata |
| Avvio analisi | ✅ Click bottone | ✅ Invio AJAX | Non bloccante sul web |
| Visualizza risultati | ✅ Treeview | ✅ Lista/Card | Capacità equivalente |
| Viewer CSV | ✅ Tab | ✅ Pagina/Modal | Pattern UX diverso |
| Multi tab CSV | ✅ Widget tab | ✅ Tab JS | Realizzabile |
| Effetti hover | ✅ Eventi custom | ✅ CSS :hover | Più semplice sul web |
| Accesso offline | ✅ Sì | ⚠️Sì, ma richiede server locale | Più complesso ma meno dipendente dal sistema |
| Mobile | ❌ No | ✅ Responsive | Nuova capacità |

Parità complessiva: parità 100% raggiungibile + miglioramenti significativi

---

## 5. Valutazione dei Rischi

### 5.1 Rischi Tecnici

| Rischio | Gravità | Mitigazione |
|---------|---------|-------------|
| Limitazioni accesso file system | MEDIO | Operazioni lato server; documentare requisiti dei percorsi |
| Gestione processi long-running | MEDIO | Esecuzione in background opzionale |
| Accesso concorrente | BASSO | Lock su file se necessario |
| Gestione sessione | BASSO | Sessioni Flask per dati utente |
| Sicurezza (upload file) | ALTA | Validazione stretta, sandboxing, sanitizzazione percorsi |
| Compatibilità browser | BASSO | HTML5/CSS3 standard; test sui principali browser |
| Visualizzazione CSV grandi | MEDIO | Paginazione o virtual scrolling |
| Gestione stato | BASSO | Sessioni lato server o DB per stato job |

### 5.2 Rischi Non Tecnici

| Rischio | Gravità | Mitigazione |
|---------|---------|-------------|
| Resistenza degli utenti | BASSO | Guida di migrazione chiara; flusso familiare |
| Formazione necessaria | BASSO | UI web generalmente più intuitiva |
| Perdita capacità offline | MEDIO | Documentare setup localhost per uso offline |

---

## 6. Breaking Changes & Compatibilità

### 6.1 Breaking Changes

1. **Metodo di esecuzione**: 
   - VECCHIO: `python GUI/gui_analysis.py`
   - NUOVO: `python web_gui/app.py` (o `flask run`)

2. **Selezione cartelle**:
   - VECCHIO: dialog nativo del sistema
   - NUOVO: inserimento manuale percorso (input testo)
   - Workaround: widget file browser (es. directory picker JS)

3. **Uso offline**:
   - VECCHIO: app desktop completamente offline
   - NUOVO: richiede server web locale (ancora offline su localhost)

### 6.2 Retrocompatibilità

Compatibile:
- `exec_analysis.py` – utilizzabile da CLI
- Logica di analisi (producer/consumer)
- Dizionari librerie
- Formato output (CSV)

Non compatibile:
- Import diretti della classe `IGESAnalysisTool`
- Codice specifico Tkinter

---

## 7. Strategia di Migrazione

### 7.1 Approccio a Fasi (raccomandato)

#### Fase 1: Backend API (Settimana 1)
1. Creare struttura applicazione Flask
2. Implementare endpoint esecuzione analisi
3. Creare servizio upload file
4. Scrivere unit test

Deliverable: API funzionanti, testabili con Postman/curl

#### Fase 2: Frontend (Settimana 2)
1. Creare template HTML (base, index, results)
2. Implementare form input con validazione
3. Aggiungere barra di progresso e stato
4. Costruire pagina elenco risultati
5. Creare componente viewer CSV
6. Applicare stile (Bootstrap/Tailwind)

Deliverable: UI web funzionante

#### Fase 3: Integrazione & Test (Settimana 3)
1. Test end-to-end
2. Gestione errori e edge case
3. Performance con dataset grandi
4. Sicurezza (upload, path traversal)
5. Cross–browser
6. Responsive mobile

Deliverable: applicazione pronta alla produzione

#### Fase 4: Documentazione (Settimana 4)
1. Aggiornare README con istruzioni web

Deliverable: documentazione completa

## 8. Strategia di Testing

### 8.1 Unit Test

Nuovi test richiesti:
```python
# tests/web_gui/test_analysis_service.py
def test_analysis_service_start()
def test_analysis_service_cancellation()

# tests/web_gui/test_file_service.py
def test_csv_upload_valid()
def test_csv_upload_invalid()
def test_path_validation()

# tests/web_gui/test_routes.py
def test_analysis_start_endpoint()
def test_results_list_endpoint()
def test_csv_viewer_endpoint()
```

Test modificati:
```python
# tests/test_exec_analysis.py
def test_exec_analyzer_cli()            # ESISTENTE
```

### 8.2 Test di Integrazione

```python
# tests/integration/test_web_flow.py
def test_full_analysis_workflow()
def test_file_upload_and_analysis()
def test_results_retrieval()
## (test concorrenza fuori scope)
```

### 8.3 Checklist di Test Manuale

- [ ] Upload di un CSV valido
- [ ] Upload di un CSV non valido (gestione errori)
- [ ] Invio analisi con percorsi validi
- [ ] Invio analisi con percorsi non validi (gestione errori)
 
- [ ] Visualizzazione risultati Consumers
- [ ] Visualizzazione risultati Producers
- [ ] Apertura file CSV nel viewer
- [ ] Apertura multipla di CSV
- [ ] Test su browser diversi (Chrome, Firefox, Safari, Edge)
- [ ] Test con dataset grandi (performance)

---

## 9. Aggiornamenti di Documentazione Necessari

### 9.1 File da Aggiornare

1. **README.md**
   - Sezione installazione (dipendenze web)
   - Sezione usage (nuovi comandi)
   - Screenshot UI web

2. **Nuova Documentazione**
    - `web_gui/README.md` – Guida specifica alla GUI web
   - `API.md` – Documentazione endpoint API (se esposti)

### 9.2 Esempi README (prima/dopo)

PRIMA:
```bash
# Avvio GUI
python MARK-Tool/Categorizer/src/GUI/gui_analysis.py

# Avvio da CLI
python MARK-Tool/Categorizer/src/exec_analysis.py --input_path ./repos --output_path ./results
```

DOPO:
```bash
# Avvio da CLI (invariato)
python MARK-Tool/Categorizer/src/exec_analysis.py --input_path ./repos --output_path ./results
```

---

## 10. Requisiti di Risorse

### 10.1 Risorse Umane

| Ruolo | Sforzo | Attività |
|-------|--------|----------|
| **Backend Developer** | 1–2 settimane | App Flask, endpoint API, service layer |
| **Frontend Developer** | 1–2 settimane | HTML/CSS/JS, componenti, integrazione |
| **QA/Tester** | 3–5 giorni | Pianificazione test, esecuzione, bug report |
| **Technical Writer** | 2–3 giorni | Aggiornamento documentazione |

Sforzo totale: 2–4 settimane circa

### 10.2 Requisiti Tecnici

- Python 3.8+
- Browser moderno


## 11. Analisi Costi-Benefici

### 11.1 Costi

| Voce | Sforzo/Costo |
|------|--------------|
| Sviluppo | 2–4 settimane |
| Testing | 3–5 giorni |
| Documentazione | 2–3 giorni |
| **Totale Sviluppo** | **~3–5 settimane** |

### 11.2 Benefici

Benefici immediati:
- UI moderna e responsive
- Migliore gestione errori e feedback
- Possibile capacità multi–utente
- Possibile accesso remoto
- Possibile supporto mobile
- Stilizzazione più semplice
- Più facile versionare (template vs codice Tkinter)

Benefici a lungo termine:
- Onboarding più semplice (UI web familiare)
- Indipendenza dalla piattaforma (niente problemi Tkinter)
- Opzioni di deploy in cloud
- API riutilizzabile per integrazioni
- Migliori capacità di testing
- Scalabilità (cache, database, ecc.)

ROI: ALTO – costo una tantum per grandi miglioramenti UX

---

## 12. Piano di Implementazione

### 12.1 MVP – Settimana 1

Obiettivo: UI web di base funzionante con le feature core

Funzionalità:
1. Form input (percorsi + CSV opzionale)
2. Pulsante avvio analisi
3. Elenco risultati (Consumers/Producers)
4. Viewer CSV semplice

Stack: Flask + Bootstrap 5 + JS vanilla

### 12.2 Versione Avanzata – Settimane 2–3

Feature aggiuntive:
1. Upload drag & drop
2. Multi tab CSV
3. Download risultati
4. Notifiche error

### 12.3 Pronta per Produzione – Settimana 4

Migliorie:
1. Documentazione completa
2. Guida utente con screenshot

## 13. Criteri di Successo

La migrazione è da considerarsi riuscita quando:

- [ ] Tutte le funzionalità della GUI attuale sono replicate
- [ ] L’interfaccia web è accessibile da browser moderni
- [ ] L’esecuzione dell’analisi è identica al sistema attuale 
- [ ] La documentazione è aggiornata

## Informazioni Documento

**Versione**: 1.0  
**Data**: 2025-10-13  
**Autore**: Turco Luigi