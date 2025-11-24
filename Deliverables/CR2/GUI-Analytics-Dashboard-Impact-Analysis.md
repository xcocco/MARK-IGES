# Analisi di Impatto: Estensione GUI Web con Dashboard di Analytics

## Informazioni Documento

**Versione**: 1.0  
**Data**: 2025-11-24  
**Autore**: De Pasquale Luca, De Pasquale Marco, Turco Luigi

## Descrizione Documento

Questo documento fornisce un’analisi di impatto per l’evoluzione della nuova GUI web del MARK Analysis Tool con:
- miglioramento grafico e adozione di stili moderni;
- introduzione di una dashboard di analytics;
- esposizione di nuovi endpoint backend per fornire al frontend dati aggregati sull’output dell’analisi.

**Stato Attuale**: GUI web di base (CR1) con form di input e visualizzazione risultati principalmente tabellare.  
**Stato Proposto**: GUI web arricchita da una dashboard interattiva con grafici (pie chart, istogrammi, grafico keywords) e layout modernizzato, supportata da nuovi endpoint REST.

**Complessità della Change Request**: Medio–Alta  
**Sforzo Stimato**: 1–2 settimane (building sulla base dell’architettura web già introdotta in CR1)

---

## 1. Architettura Attuale della GUI Web (post-CR1)

### 1.1 Implementazione Esistente

**Percorso**: `MARK-Tool/MARK-Tool/web_gui/`

**File principali** (da CR1):
- `app.py` – Entry point Flask
- `config.py` – Configurazione
- `routes/analysis_routes.py` – Endpoint avvio analisi
- `routes/file_routes.py` – Endpoint upload/download file
- `routes/results_routes.py` – Endpoint visualizzazione risultati (lista CSV, viewer)
- `services/analysis_service.py` – Ponte verso `exec_analysis.py`
- `services/file_service.py` – Gestione upload/validazione
- `templates/` – `base.html`, `index.html`, `results.html`, `csv-viewer.html`  
- `static/` – CSS/JS e risorse statiche

### 1.2 Funzionalità Attuali Rilevanti

#### Input/Workflow
1. Form web per:
   - percorso cartella input,
   - percorso cartella output,
   - upload CSV GitHub (opzionale).
2. Endpoint backend per avvio analisi (sincrono o asincrono) via `analysis_service`.
3. Persistenza dei risultati in CSV come nella versione desktop.

#### Output
1. Elenco file risultati per Consumers e Producers (lista CSV).  
2. Viewer CSV web (tabella con scrolling) che replica la visualizzazione della GUI desktop.  
3. Nessuna dashboard grafica o aggregazione avanzata; le informazioni sono esposte principalmente in forma tabellare.

### 1.3 Punti di Forza
- Architettura già separata in routes/services/templates.  
- Riutilizzo della logica di analisi esistente (`exec_analysis.py`).  
- Struttura pronta per estensioni API.

### 1.4 Limiti Attuali
- Interfaccia grafica basica, con stile limitato e poca gerarchia visiva.  
- Manca una dashboard sintetica che presenti:
  - percentuali consumer vs producer;
  - conteggi assoluti;
  - distribuzione delle keywords usate per la verifica/classificazione.  
- I risultati sono poco “narrativi”: l’utente deve interpretare le tabelle manualmente.

---

## 2. Architettura Web Proposta (Estensione con Dashboard)

### 2.1 Obiettivi della Change Request

1. **Migliorare la UX/UI** dell’interfaccia con uno stile moderno e più intuitivo (layout a sezioni, cards, colori coerenti).  
2. **Introdurre una dashboard di analytics** che mostri:
   - un grafico a torta (% modelli consumer vs producer),
   - un istogramma con i numeri assoluti per consumer/producer (ed eventuale categoria "Altro"/non classificati),
   - un grafico per la prevalenza delle keywords utilizzate per la verifica/classificazione (top-N keywords).
3. **Esporre dati aggregati via nuovi endpoint backend** dedicati all’analytics, in grado di:
   - restituire aggregazioni globali dell’ultima analisi,
   - restituire, se necessario, dati filtrati (es. per tipo consumer/producer o per keyword).

### 2.2 Stack Tecnologico (frontend)

- **Framework CSS**: Bootstrap 5 (o equivalente già usato nella CR1) per:
  - layout responsive (grid, cards);
  - componenti UI (navbar, cards, alerts).
- **Libreria grafici**: Chart.js per:
  - pie chart, bar chart verticali/orizzontali;
  - tooltips e interazioni base (click, hover) per filtrare i risultati.  
- **JavaScript**: vanilla JS o modulo dedicato (es. `static/js/dashboard.js`) per:
  - chiamare gli endpoint analytics;
  - inizializzare e aggiornare i grafici;
  - collegare interazioni grafico ↔ tabella risultati.

### 2.3 Nuovi Endpoint API Proposti

All’interno di `MARK-Tool/MARK-Tool/web_gui/routes/results_routes.py` **o** in un nuovo modulo dedicato `analytics_routes.py`:

1. `GET /api/analytics/summary`
   - **Output** (JSON, esempio):
     ```json
     {
       "total_models": 120,
       "consumer_count": 70,
       "producer_count": 40,
       "other_count": 10,
       "last_analysis_id": "2025-11-24T10:32:01Z"
     }
     ```
   - Usato per popolare cards sintetiche e grafici consumer/producer.

2. `GET /api/analytics/consumer-producer-distribution`
   - Restituisce i dati per pie chart e bar chart:
     ```json
     {
       "labels": ["Consumer", "Producer", "Altro"],
       "counts": [70, 40, 10],
       "percentages": [58.3, 33.3, 8.4]
     }
     ```

3. `GET /api/analytics/keywords`
   - Restituisce la distribuzione delle keywords principali (top-N):
     ```json
     {
       "labels": ["train", "predict", "inference", "fit"],
       "counts": [30, 25, 18, 12]
     }
     ```
   - I dati provengono dall’analisi dei documenti già esistenti (stesso corpus usato per la classificazione producer/consumer).

4. (Opzionale) `GET /api/analytics/filter`
   - Parametri query: `type=consumer|producer`, `keyword=<kw>`.  
   - Restituisce una lista di elementi filtrati, da usare per aggiornare la tabella dei risultati quando l’utente clicca sui grafici.

---

## 3. Analisi di Impatto Dettagliata

### 3.1 File da Creare/Modificare

#### NUOVI FILE (Dashboard & Analytics)

```text
MARK-Tool/MARK-Tool/web_gui/
├── routes/
│   └── analytics_routes.py          # Endpoint analytics (summary, distribuzioni, keywords)
├── services/
│   └── analytics_service.py        # Logica di aggregazione dai CSV o da struttura dati
├── static/
│   ├── js/
│   │   └── dashboard.js            # Inizializzazione/aggiornamento grafici Chart.js
│   └── css/
│       └── dashboard.css           # Stili specifici per cards e dashboard
└── templates/
    └── dashboard.html              # Pagina (o sezione) principale analytics
```

> Nota: se la dashboard viene integrata direttamente in `results.html`, `dashboard.html` può essere sostituito da componenti inclusi (ad es. `templates/components/dashboard.html`).

#### FILE DA MODIFICARE

```text
MARK-Tool/MARK-Tool/web_gui/app.py
    - Registrare il nuovo blueprint `analytics_routes`

MARK-Tool/MARK-Tool/web_gui/routes/results_routes.py
    - (Opzionale) Aggiungere endpoint JSON già menzionati se non si vuole un file separato

MARK-Tool/MARK-Tool/web_gui/services/analysis_service.py
    - Esporre API/metodi per ottenere strutture dati in forma utilizzabile da `analytics_service`

MARK-Tool/MARK-Tool/web_gui/templates/base.html
    - Aggiungere link di navigazione alla dashboard (navbar)

MARK-Tool/MARK-Tool/web_gui/templates/results.html
    - Integrare la sezione dashboard oppure linkare a `dashboard.html`

MARK-Tool/MARK-Tool/web_gui/static/css/styles.css
    - Integrare/armonizzare gli stili moderni (cards, layout) con `dashboard.css`

MARK-Tool/MARK-Tool/web_gui/static/js/main.js
    - Inizializzare la dashboard o orchestrare il caricamento di `dashboard.js`

MARK-Tool/MARK-Tool/web_gui/requirements.txt
    - Verificare/aggiornare dipendenze (es. Chart.js referenziato via CDN nel template)

MARK-Tool/MARK-Tool/README.md
    - Aggiornare sezione GUI web con screenshot/descrizione dashboard analytics
```

### 3.2 Modifiche Backend Necessarie

#### 3.2.1 `analytics_service.py`

Responsabilità principali:
- Caricare/leggere i CSV risultati generati dall’analisi (consumers/producers).  
- Calcolare:
  - conteggi globali (consumer/producer/altro),
  - percentuali sulla base del totale,
  - mappa `keyword -> count` su tutti gli elementi analizzati.
- Esporre metodi invocati da `analytics_routes.py`, ad esempio:

```python
class AnalyticsService:
    def __init__(self, results_folder):
        self.results_folder = results_folder

    def get_consumer_producer_counts(self):
        """Restituisce conteggi e percentuali per consumer/producer/altro."""
        ...

    def get_top_keywords(self, limit=10):
        """Restituisce le top-N keywords con le rispettive frequenze."""
        ...
```

Impatto: MEDIO – nuovo componente di servizio, richiede accesso ai formati CSV già esistenti ma non modifica la logica dell’analisi.

#### 3.2.2 `analytics_routes.py`

- Registrato come Blueprint in `app.py`.  
- Definisce endpoint JSON descritti nella sezione 2.3.  
- Utilizza `AnalyticsService` per costruire le risposte.

Impatto: MEDIO – nuovo layer API, efficacemente indipendente dalle route esistenti.

#### 3.2.3 Adeguamenti a `analysis_service.py`

- Fornire un modo standard per individuare l’“ultima analisi” o l’analisi corrente (path cartella risultati, ID job, timestamp).  
- Esporre metadati utili a `AnalyticsService` (es. posizione dei CSV di output consolidati).

Impatto: BASSO – modifiche additive.

### 3.3 Modifiche Frontend Necessarie

#### 3.3.1 Layout e Stili Moderni

- Aggiornamento di `base.html`/`results.html` per:
  - introdurre una sezione “Dashboard” con layout a griglia (Bootstrap);  
  - usare cards per:
    - `Totale modelli`,
    - `# Consumer`, `# Producer`, `# Altro`,
    - eventuali indicatori aggiuntivi (es. n° librerie, n° progetti analizzati).
- Aggiornamento CSS (`styles.css` + `dashboard.css`) per:
  - palette coerente (colori distinti per consumer/producer);
  - tipografia migliorata;  
  - spaziatura e bordi per una UX più chiara.

Impatto: MEDIO – cambiamenti principalmente estetici, strutturali ma non funzionali lato backend.

#### 3.3.2 Integrazione Grafici (Chart.js)

- Aggiungere in `base.html` o nella pagina dashboard:
  - import di Chart.js (CDN consigliato).  
- In `dashboard.html` o `results.html`:
  - definire `<canvas>` per:
    - grafico a torta consumer/producer,
    - istogramma consumer/producer,
    - grafico (bar orizzontale) per keywords.
- In `dashboard.js`:
  - chiamare `/api/analytics/consumer-producer-distribution` e `/api/analytics/keywords`;
  - inizializzare i grafici con i dati ricevuti;
  - (opzionale) gestire eventi `onClick` sui grafici per filtrare la tabella risultati.

Impatto: MEDIO – richiede uno sforzo di integrazione JS, ma non altera la logica core.

#### 3.3.3 Collegamento Grafici ↔ Viewer Risultati (Opzionale)

- Aggiungere funzioni JS che, in risposta a:
  - click su slice “Consumer”/“Producer” del pie chart;
  - click su una barra keyword;
  chiamino un endpoint tipo `/api/analytics/filter` e aggiornino la tabella dei risultati (già gestita da `results-viewer.js` in CR1).

Impatto: MEDIO–ALTO – migliora molto la UX, ma aumenta la complessità JS.

---

## 4. Matrice di Parità e Miglioramenti Funzionali

| Funzionalità | Stato Attuale Web | Stato Proposto | Note |
|--------------|-------------------|----------------|------|
| Form input analisi | ✅ Sì | ✅ Invariato (restyling) | Nessun impatto logico |
| Lista risultati (CSV) | ✅ Sì | ✅ Invariato (più integrata con dashboard) | Mantiene parità funzionale |
| Viewer CSV | ✅ Sì | ✅ Invariato | Nessun cambiamento semantico |
| Dashboard consumer/producer | ❌ No | ✅ Sì | Nuova funzionalità |
| Grafico a torta % cons/prod | ❌ No | ✅ Sì | Nuova capacità di sintesi |
| Istogramma numeri cons/prod | ❌ No | ✅ Sì | Nuova capacità di lettura quantitativa |
| Grafico keywords | ❌ No | ✅ Sì | Nuova capacità di insight sulle logiche di classificazione |
| Endpoint analytics JSON | ❌ No | ✅ Sì | Nuovo layer API |
| Click grafici → filtri | ❌ No | ⚠️ Opzionale | Implementabile in fase avanzata |

---

## 5. Valutazione dei Rischi

### 5.1 Rischi Tecnici

| Rischio | Gravità | Mitigazione |
|---------|---------|-------------|
| Incoerenza dati analytics (conteggi errati) | MEDIO | Scrivere test automatici su `AnalyticsService` e confrontare con CSV di riferimento |
| Performance su dataset grandi (keywords) | MEDIO | Limitare analisi a top-N keywords; caching dei risultati |
| Aumento complessità JS (Chart.js + interazioni) | BASSO–MEDIO | Tenere `dashboard.js` modulare e separato da `main.js` |
| Versioning dei risultati/ultima analisi | BASSO | Definire chiaramente come identificare l’analisi corrente (timestamp/cartella) |
| Problemi di compatibilità grafici tra browser | BASSO | Chart.js è cross–browser; test principali (Chrome, Firefox, Edge) |

### 5.2 Rischi Non Tecnici

| Rischio | Gravità | Mitigazione |
|---------|---------|-------------|
| Sovraccarico informativo (troppi grafici) | BASSO | Limitare a 2–3 grafici ben spiegati; tooltips chiari |
| Necessità di aggiornare documentazione e screenshot | BASSO | Pianificare aggiornamento README e manuale utente |

---

## 6. Breaking Changes & Compatibilità

### 6.1 Breaking Changes

- **Nessuna breaking change lato API esistenti**: i nuovi endpoint sono aggiuntivi e non sostituiscono quelli creati in CR1.  
- Il layout grafico della pagina risultati può cambiare in modo significativo (nuova dashboard in alto, risultati in basso), ma la semantica dei dati resta invariata.

### 6.2 Retrocompatibilità

Compatibile:
- Flusso di analisi (avvio, esecuzione, salvataggio CSV).  
- Endpoint di base per caricamento input e visualizzazione risultati introdotti in CR1.  
- Formato CSV e logica di classificazione producer/consumer.

Non pienamente compatibile (solo a livello visivo/UX):
- Aspetto e posizionamento dei componenti UI nella pagina risultati rispetto alla versione web di base.

---

## 7. Strategia di Implementazione

### 7.1 Fase 1 – Backend Analytics (2–3 giorni)

1. Implementare `AnalyticsService` con:
   - lettura CSV risultati,
   - calcolo distribuzioni consumer/producer,
   - calcolo top-N keywords.
2. Implementare `analytics_routes.py` con endpoint JSON:
   - `/api/analytics/summary`,
   - `/api/analytics/consumer-producer-distribution`,
   - `/api/analytics/keywords`.
3. Integrare blueprint in `app.py`.
4. Scrivere test unitari minimi per `AnalyticsService` e per gli endpoint.

### 7.2 Fase 2 – Dashboard Frontend (2–4 giorni)

1. Progettare layout dashboard in `dashboard.html` o `results.html` (sezione dedicata).  
2. Integrare Bootstrap (se non già fatto) per cards e griglia.  
3. Aggiungere i canvas per i tre grafici.  
4. Implementare `dashboard.js` per:
   - chiamare gli endpoint analytics,
   - inizializzare i grafici Chart.js,
   - aggiornare i grafici al cambio dell’analisi corrente.

### 7.3 Fase 3 – Integrazione con Viewer Risultati (1–2 giorni, opzionale ma raccomandata)

1. Aggiungere interazioni click sui grafici per filtrare la tabella risultati.  
2. Aggiungere, se necessario, endpoint `/api/analytics/filter`.  
3. Aggiornare `results-viewer.js` (o equivalente) per:
   - ricaricare i dati filtrati in tabella.

### 7.4 Fase 4 – Test & Documentazione (1–2 giorni)

1. Testare:
   - correttezza numerica dei grafici rispetto ai CSV,
   - caricamento corretto della dashboard su diversi browser,
   - performance con dataset realistici.  
2. Aggiornare `web_gui/README.md` e `MARK-Tool/MARK-Tool/README.md` con:
   - screenshot della dashboard,
   - descrizione dei nuovi grafici e del loro significato,
   - elenco degli endpoint analytics.

---

## 8. Strategia di Testing

### 8.1 Unit Test

Nuovi test suggeriti:

```text
# tests/web_gui/test_analytics_service.py
- test_consumer_producer_counts_from_sample_csv()
- test_percentages_sum_to_100()
- test_top_keywords_limit()

# tests/web_gui/test_analytics_routes.py
- test_analytics_summary_endpoint()
- test_consumer_producer_distribution_endpoint()
- test_keywords_endpoint()
```

### 8.2 Test di Integrazione

```text
# tests/integration/test_web_analytics_flow.py
- test_full_analytics_workflow()        # analisi + chiamata endpoint + verifica grafici lato frontend (parziale)
```

### 8.3 Checklist di Test Manuale

- [ ] Eseguire un’analisi su un progetto di esempio.  
- [ ] Verificare caricamento dashboard senza errori JS.  
- [ ] Controllare che la somma `consumer + producer + altro` coincida col totale.  
- [ ] Verificare che le percentuali nel pie chart siano coerenti con i conteggi.  
- [ ] Verificare che le keywords mostrate siano effettivamente presenti nei risultati.  
- [ ] Testare la dashboard su almeno 2 browser.  
- [ ] (Se implementato) Verificare il funzionamento dei filtri tramite click sui grafici.

---

## 9. Requisiti di Risorse

### 9.1 Risorse Umane

| Ruolo | Sforzo | Attività |
|-------|--------|----------|
| **Backend Developer** | 2–3 giorni | `AnalyticsService`, `analytics_routes.py`, test |
| **Frontend Developer** | 3–5 giorni | Layout dashboard, integrazione Chart.js, interazioni |


Sforzo totale stimato: ~1–2 settimane (considerando che la base web esiste già).

### 9.2 Requisiti Tecnici

- Python 3.8+  
- Flask (già presente da CR1)  
- Browser moderno con supporto HTML5/JS  
- Accesso ai risultati CSV generati dall’analisi

---

## 10. Criteri di Successo

La change request è da considerarsi completata con successo quando:

- [ ] La GUI web mostra una dashboard di analytics con almeno:
  - un grafico a torta % consumer/producer,  
  - un istogramma con num. consumer/producer (ed eventuale altro),  
  - un grafico delle top-N keywords.
- [ ] I nuovi endpoint backend forniscono i dati necessari in formato JSON stabile.  
- [ ] I valori mostrati dai grafici sono coerenti con i CSV prodotti dal sistema.  
- [ ] Il layout complessivo è più moderno, leggibile e intuitivo rispetto alla versione web di base.  
- [ ] La documentazione (README e guida GUI web) è aggiornata con la descrizione della dashboard e dei nuovi endpoint.
