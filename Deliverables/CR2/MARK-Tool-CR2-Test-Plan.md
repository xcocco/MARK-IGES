# CR2 - Test Plan  

## Informazione Documento  
  
Versione: 1.1  
Data: 2025-12-02  
Autore: Turco Luigi

---  

## 1 Introduzione  
### 1.1 Scopo  
Questo documento definisce il Test Plan per la Change Request 2 (CR2) del progetto MARK-Tool.   
L'obiettivo è descrivere l'approccio, i requisiti di test, i casi di test principali e i criteri di accettazione per validare le funzionalità frontend/backend introdotte nella CR2 per l'estensione della GUI web con dashboard di analytics.

### 1.2 Struttura del documento  
Il documento è diviso in test plan per lato backend (analytics API) e test plan per il lato frontend (dashboard UI).  

---  

## 2 Test Plan Backend  

**In Scope:**  
- Analytics API endpoints (6 nuovi endpoints)  
- Analytics Service unit testing  
- Integration testing con risultati CSV esistenti  
- Dashboard frontend UI e interazioni grafici  
- Regression: core MARK-Tool (pre-CR1) invariato  
- Regression: funzionalità CR1 web GUI invariate  

### 2.1 Strategia di testing  
#### 2.1.1 Livelli  

| Livello | Strumenti | Focus |  
|---------|-----------|-------|  
| Unit Testing | pytest | AnalyticsService (9 metodi) |  
| API Testing | pytest + Flask client | 6 analytics endpoints |  
| Integration | pytest | E2E analytics workflows |  
| Regression Core | pytest + exec_analysis.py | Pipeline analisi core MARK-Tool invariata |  
| Regression CR1 | pytest | 33 test CR1 web GUI invariati |  

#### 2.1.2 Approccio  
- **Unit Testing** per AnalyticsService con CSV mock  
- **Category Partition** per ridurre test cases API  
- **Equivalence Partitioning** e **Boundary Value Analysis** per parametri  
- **Integration Testing** per workflow analytics completo  

#### 2.1.3 Criteri Accettazione  
- 100% copertura metodi AnalyticsService  
- 100% copertura analytics endpoints  
- Esecuzione completa e analisi di tutti i test CR1 per verificare assenza regressioni  
- Gestione errori HTTP corretta (400, 404, 500)  
- Performance accettabili su dataset realistici  

---  

### 2.2 Category Partition Analytics API  

#### 2.2.1 GET /api/analytics/summary  

**Categories:**  
- output_path: [valid, invalid, missing, not_directory]  
- CSV files: [both_present, only_consumer, only_producer, missing]  

**Constraints:**  
- If output_path missing → 400  
- If output_path invalid → 400  
- If CSV files missing → 400  

**Test Cases:** 6  

---  

#### 2.2.2 GET /api/analytics/consumer-producer-distribution  

**Categories:**  
- output_path: [valid, missing]  
- Data: [normal, empty, only_consumers, only_producers]  

**Test Cases:** 5  

---  

#### 2.2.3 GET /api/analytics/keywords  

**Categories:**  
- output_path: [valid, missing]  
- limit: [default(10), custom(5), boundary(1), boundary(100), invalid(0), invalid(101)]  
- Keywords: [normal, empty, single]  

**Test Cases:** 8  

---  

#### 2.2.4 GET /api/analytics/libraries  

**Categories:**  
- output_path: [valid, missing]  
- limit: [default(10), custom(5), boundary(1), boundary(100), invalid(0), invalid(101)]  
- Libraries: [normal, empty, single]  

**Test Cases:** 8  

---  

#### 2.2.5 GET /api/analytics/filter  

**Categories:**  
- output_path: [valid, missing]  
- type: [null, consumer, producer, invalid]  
- keyword: [null, valid, not_found]  
- library: [null, valid, not_found]  
- project: [null, valid, not_found]  
- limit: [default(100), custom(50), boundary(1), boundary(1000), invalid(0), invalid(1001)]  

**Constraints:**  
- If type invalid → 400  
- Multiple filters → AND logic  

**Test Cases:** 15  

---  

### 2.3 Casi di Test Analytics Service (20 totali)  

#### 2.3.1 Unit Test AnalyticsService  

* **TC-AS-01**: validate_output_path - Path Valido  
  * Input: Directory esistente con CSV  
  * Expected: (True, "Output path is valid")  

* **TC-AS-02**: validate_output_path - Path Non Esistente  
  * Input: "/nonexistent/path"  
  * Expected: (False, "Output path does not exist")  

* **TC-AS-03**: validate_output_path - Non Directory  
  * Input: Path a file regolare  
  * Expected: (False, "Output path is not a directory")  

* **TC-AS-04**: validate_output_path - CSV Mancanti  
  * Input: Directory senza consumer.csv né producer.csv  
  * Expected: (False, "No consumer.csv or producer.csv found")  

* **TC-AS-05**: get_summary - Conteggi Corretti  
  * Input: CSV con 3 consumers, 2 producers  
  * Expected: total_models=5, consumer_count=3, producer_count=2  

* **TC-AS-06**: get_summary - Progetti Unici  
  * Input: CSV con progetti ripetuti  
  * Expected: total_projects conta progetti distinti  

* **TC-AS-07**: get_summary - Librerie Uniche  
  * Input: CSV con librerie ripetute  
  * Expected: total_libraries conta librerie distinte  

* **TC-AS-08**: get_consumer_producer_distribution - Percentuali  
  * Input: 60 consumers, 40 producers  
  * Expected: percentages=[60.0, 40.0]  

* **TC-AS-09**: get_consumer_producer_distribution - Dataset Vuoto  
  * Input: CSV vuoti  
  * Expected: counts=[0, 0], percentages=[0.0, 0.0]  

* **TC-AS-10**: get_top_keywords - Ordinamento  
  * Input: Keywords con frequenze diverse  
  * Expected: Lista ordinata per frequenza decrescente  

* **TC-AS-11**: get_top_keywords - Limite Rispettato  
  * Input: 20 keywords, limit=10  
  * Expected: Ritorna esattamente 10 keywords  

* **TC-AS-12**: get_top_keywords - Dataset Vuoto  
  * Input: CSV senza keywords  
  * Expected: labels=[], counts=[], total_unique_keywords=0  

* **TC-AS-13**: get_library_distribution - Ordinamento  
  * Input: Librerie con frequenze diverse  
  * Expected: Lista ordinata per frequenza decrescente  

* **TC-AS-14**: get_library_distribution - Limite Rispettato  
  * Input: 15 librerie, limit=10  
  * Expected: Ritorna esattamente 10 librerie  

* **TC-AS-15**: get_filtered_results - Filtro Type Consumer  
  * Input: type='consumer'  
  * Expected: Solo consumer results, tutti con type='consumer'  

* **TC-AS-16**: get_filtered_results - Filtro Type Producer  
  * Input: type='producer'  
  * Expected: Solo producer results, tutti con type='producer'  

* **TC-AS-17**: get_filtered_results - Filtro Keyword  
  * Input: keyword='.predict('  
  * Expected: Solo results contenenti '.predict(' in keywords  

* **TC-AS-18**: get_filtered_results - Filtro Library  
  * Input: library='tensorflow'  
  * Expected: Solo results con library='tensorflow'  

* **TC-AS-19**: get_filtered_results - Filtri Multipli (AND)  
  * Input: type='consumer', library='tensorflow'  
  * Expected: Solo consumer con tensorflow  

* **TC-AS-20**: get_filtered_results - Limite Rispettato  
  * Input: Dataset con 200 elementi, limit=50  
  * Expected: Ritorna esattamente 50 elementi  

---  

### 2.4 Casi di Test Analytics API (30 totali)  

#### 2.4.1 GET /api/analytics/summary (5)  

* **TC-ANA-01**: Summary - Output Path Valido  
  * GET /api/analytics/summary?output_path=/valid/path  
  * Expected: 200, JSON con total_models, consumer_count, producer_count  

* **TC-ANA-02**: Summary - Output Path Mancante  
  * GET /api/analytics/summary  
  * Expected: 400, "output_path parameter is required"  

* **TC-ANA-03**: Summary - Output Path Non Esistente  
  * GET /api/analytics/summary?output_path=/nonexistent  
  * Expected: 400, "Output path does not exist"  

* **TC-ANA-04**: Summary - CSV Mancanti  
  * GET /api/analytics/summary?output_path=/empty/dir  
  * Expected: 400, "No consumer.csv or producer.csv found"  

* **TC-ANA-05**: Summary - Valori Corretti  
  * Input: CSV con dati noti  
  * Expected: Valori numerici corretti, last_analysis_id presente  

---  

#### 2.4.2 GET /api/analytics/consumer-producer-distribution (5)  

* **TC-ANA-06**: Distribution - Output Path Valido  
  * GET /api/analytics/consumer-producer-distribution?output_path=/valid  
  * Expected: 200, labels=['Consumer','Producer'], counts, percentages  

* **TC-ANA-07**: Distribution - Output Path Mancante  
  * Expected: 400, "output_path parameter is required"  

* **TC-ANA-08**: Distribution - Percentuali Corrette  
  * Input: 70 consumers, 30 producers  
  * Expected: percentages=[70.0, 30.0]  

* **TC-ANA-09**: Distribution - Dataset Vuoto  
  * Input: CSV vuoti  
  * Expected: 200, counts=[0,0], percentages=[0.0,0.0]  

* **TC-ANA-10**: Distribution - Solo Consumers  
  * Input: Solo consumer.csv popolato  
  * Expected: counts=[N, 0], percentages=[100.0, 0.0]  

---  

#### 2.4.3 GET /api/analytics/keywords (6)  

* **TC-ANA-11**: Keywords - Default Limit  
  * GET /api/analytics/keywords?output_path=/valid  
  * Expected: 200, massimo 10 keywords  

* **TC-ANA-12**: Keywords - Custom Limit  
  * GET /api/analytics/keywords?output_path=/valid&limit=5  
  * Expected: 200, massimo 5 keywords  

* **TC-ANA-13**: Keywords - Boundary Limit=1  
  * GET /api/analytics/keywords?output_path=/valid&limit=1  
  * Expected: 200, esattamente 1 keyword  

* **TC-ANA-14**: Keywords - Boundary Limit=100  
  * GET /api/analytics/keywords?output_path=/valid&limit=100  
  * Expected: 200, massimo 100 keywords  

* **TC-ANA-15**: Keywords - Limit Invalido (<1)  
  * GET /api/analytics/keywords?output_path=/valid&limit=0  
  * Expected: 400, "limit must be between 1 and 100"  

* **TC-ANA-16**: Keywords - Limit Invalido (>100)  
  * GET /api/analytics/keywords?output_path=/valid&limit=101  
  * Expected: 400, "limit must be between 1 and 100"  

---  

#### 2.4.4 GET /api/analytics/libraries (6)  

* **TC-ANA-17**: Libraries - Default Limit  
  * GET /api/analytics/libraries?output_path=/valid  
  * Expected: 200, massimo 10 libraries  

* **TC-ANA-18**: Libraries - Custom Limit  
  * GET /api/analytics/libraries?output_path=/valid&limit=5  
  * Expected: 200, massimo 5 libraries  

* **TC-ANA-19**: Libraries - Boundary Limit=1  
  * GET /api/analytics/libraries?output_path=/valid&limit=1  
  * Expected: 200, esattamente 1 library  

* **TC-ANA-20**: Libraries - Boundary Limit=100  
  * GET /api/analytics/libraries?output_path=/valid&limit=100  
  * Expected: 200, massimo 100 libraries  

* **TC-ANA-21**: Libraries - Limit Invalido (<1)  
  * GET /api/analytics/libraries?output_path=/valid&limit=0  
  * Expected: 400, "limit must be between 1 and 100"  

* **TC-ANA-22**: Libraries - Limit Invalido (>100)  
  * GET /api/analytics/libraries?output_path=/valid&limit=101  
  * Expected: 400, "limit must be between 1 and 100"  

---  

#### 2.4.5 GET /api/analytics/filter (7)  

* **TC-ANA-23**: Filter - Type Consumer  
  * GET /api/analytics/filter?output_path=/valid&type=consumer  
  * Expected: 200, tutti results con type='consumer'  

* **TC-ANA-24**: Filter - Type Producer  
  * GET /api/analytics/filter?output_path=/valid&type=producer  
  * Expected: 200, tutti results con type='producer'  

* **TC-ANA-25**: Filter - Type Invalido  
  * GET /api/analytics/filter?output_path=/valid&type=invalid  
  * Expected: 400, "type must be either 'consumer' or 'producer'"  

* **TC-ANA-26**: Filter - Keyword  
  * GET /api/analytics/filter?output_path=/valid&keyword=.predict(  
  * Expected: 200, results contenenti keyword  

* **TC-ANA-27**: Filter - Library  
  * GET /api/analytics/filter?output_path=/valid&library=tensorflow  
  * Expected: 200, results con library specificata  

* **TC-ANA-28**: Filter - Filtri Multipli  
  * GET /api/analytics/filter?output_path=/valid&type=consumer&library=torch  
  * Expected: 200, solo consumer con torch  

* **TC-ANA-29**: Filter - Limit Boundary  
  * GET /api/analytics/filter?output_path=/valid&limit=1000  
  * Expected: 200, massimo 1000 results  

---  

#### 2.4.6 GET /api/analytics/health (1)  

* **TC-ANA-30**: Health Check  
  * GET /api/analytics/health  
  * Expected: 200, {"status": "healthy", "service": "Analytics API"}  

---  

### 2.5 Test di Integrazione (4)  

* **TC-INT-ANA-01**: Workflow Analytics Completo  
  1. Eseguire analisi via /api/analysis/start  
  1. Attendere completamento  
  1. Chiamare /api/analytics/summary  
  1. Verificare dati coerenti con CSV prodotti  
  1. Chiamare /api/analytics/consumer-producer-distribution  
  1. Verificare percentuali somma a 100  

* **TC-INT-ANA-02**: Filtro e Visualizzazione  
  1. Ottenere top keywords via /api/analytics/keywords  
  1. Usare prima keyword per filtrare via /api/analytics/filter  
  1. Verificare che tutti i risultati contengano la keyword  
  1. Verificare count coerente  

* **TC-INT-ANA-03**: Dataset Vuoto  
  1. Creare analisi con input vuoto  
  1. Chiamare tutti gli analytics endpoints  
  1. Verificare gestione corretta (0 counts, liste vuote)  
  1. Nessun errore 500  

* **TC-INT-ANA-04**: Dataset Grande (Performance)  
  1. Caricare CSV con >1000 entries  
  1. Chiamare analytics endpoints  
  1. Verificare risposta <2 secondi  
  1. Verificare memoria stabile  

---  

### 2.6 Regression Testing  

**Obiettivo**: Eseguire tutti i test funzionali del sistema MARK-Tool (core + CR1) per verificare che l'aggiunta degli analytics endpoints non abbia introdotto regressioni o rotture nelle funzionalità esistenti. Analizzare i risultati confrontandoli con i risultati baseline.  

#### 2.6.1 Test Core MARK-Tool (Pre-CR1)  

Prima di testare le funzionalità web GUI aggiunte in CR1, è necessario verificare che il motore di analisi core del MARK-Tool funzioni correttamente:  

* **Categorizer Core Functions**:  
  - MLConsumerAnalyzer: Analisi consumer methods  
  - MLProducerAnalyzer: Analisi producer methods  
  - NotebookConverter: Conversione .ipynb → .py  
  - Library Dictionary Loading: Caricamento CSV dictionaries  

* **Analysis Pipeline**:  
  - Input validation (cartella repos esistente)  
  - Producer analysis workflow completo  
  - Consumer analysis workflow completo  
  - Output CSV generation (producer.csv, consumer.csv)  
  - Gestione progetti multipli  

* **Test da Eseguire**:  
  - Eseguire analisi su repository test di riferimento  
  - Verificare CSV output prodotti correttamente  
  - Verificare conteggi consumer/producer coerenti  
  - Confrontare risultati con baseline pre-CR1  

#### 2.6.2 Endpoints CR1 da Re-testare  

* **Analysis Routes** (5 endpoints):  
  - POST /api/analysis/start  
  - GET /api/analysis/status/<job_id>  
  - GET /api/analysis/jobs  
  - POST /api/analysis/cancel/<job_id>  
  - GET /api/analysis/logs/<job_id>  

* **File Routes** (6 endpoints):  
  - POST /api/file/upload  
  - POST /api/file/validate/input  
  - POST /api/file/validate/output  
  - POST /api/file/validate/csv  
  - GET /api/file/download  
  - GET /api/file/list  

* **Results Routes** (4 endpoints):  
  - GET /api/results/list  
  - GET /api/results/view  
  - GET /api/results/stats  
  - POST /api/results/search  

#### 2.6.3 Test Suite CR1 Web GUI  

Eseguire l'intera test suite CR1 documentata in `Deliverables/CR1/MARK-Tool-CR1-Test-Plan.md`:  

* **Test Funzionali CR1** (33 test cases):  
  - TC-A-01 a TC-A-12: Analysis service tests  
  - TC-F-01 a TC-F-12: File management tests  
  - TC-R-01 a TC-R-09: Results display tests  

* **Test Manuali CR1**:  
  - Workflow analisi completo  
  - Upload file e validazione  
  - Visualizzazione risultati  
  - Download CSV prodotti  

#### 2.6.4 Analisi Risultati Regression  

**Procedura**:  
1. **Baseline Core MARK-Tool**: Eseguire analisi core su repository test, salvare risultati CSV  
2. **Baseline CR1**: Eseguire test suite CR1 completa (33 test cases)  
3. **Post-CR2 Core**: Ri-eseguire analisi core, confrontare CSV con baseline  
4. **Post-CR2 CR1**: Ri-eseguire test suite CR1 completa  
5. **Confrontare risultati**:  
   - Core: CSV identici? Conteggi consumer/producer invariati?  
   - CR1: Test passati baseline vs post-CR2  
   - Tempi di risposta: confronto performance core + web GUI  
   - Log errori: identificazione nuovi issues  

**Criteri Accettazione Regression**:  
- **Core MARK-Tool**: CSV output identici a baseline, stessi conteggi, nessun errore analysis pipeline  
- **CR1 Web GUI**: Tutti i test CR1 che passavano in baseline devono continuare a passare  
- Nessun nuovo errore 500 introdotto  
- Performance core CR1 endpoints non degradata (tolleranza ±10%)  
- Funzionalità core MARK-Tool e CR1 invariate  

**Execution**: Eseguire test core + test suite CR1, documentare e analizzare eventuali differenze rispetto ai baseline.  

---  

### 2.7 Test Execution  

#### 2.7.1 Struttura Test Files  

```
MARK-Tool/MARK-Tool/
└── Functional_Test/
    ├── original_tests/
    │   ├── exec_analysis_test/
    │   │   └── exec_analysis_test.py        # Core MARK-Tool tests
    │   └── run_original_tests.py            # Runner test originali
    ├── cr1/
    │   ├── backend/
    │   │   ├── web_backend_tests/
    │   │   │   ├── test_analysis_routes.py  # CR1 analysis endpoints
    │   │   │   ├── test_file_routes.py      # CR1 file endpoints
    │   │   │   ├── test_results_routes.py   # CR1 results endpoints
    │   │   │   └── test_integration.py      # CR1 integration tests
    │   │   └── run_tests.py                 # Runner test CR1
    │   └── frontend/                        # Test frontend CR1
    └── cr2/
        ├── backend/
        │   ├── test_analytics_service.py    # 20 unit tests CR2
        │   ├── test_analytics_routes.py     # 30 API tests CR2 (da creare)
        │   ├── test_integration_analytics.py # 4 integration tests CR2
        │   └── run_tests_cr2.py             # Runner test CR2
        ├── frontend/                        # Test frontend CR2 dashboard
        └── test_analytics_api.py            # Script E2E manuale CR2
```

#### 2.7.2 Comandi Execution  

**Regression Core MARK-Tool (Original Tests):**  
```bash
cd MARK-Tool/MARK-Tool/Functional_Test/original_tests
python run_original_tests.py
# Oppure con pytest:
pytest exec_analysis_test/exec_analysis_test.py -v
```

**Regression CR1 Web GUI (Backend Tests):**  
```bash
cd MARK-Tool/MARK-Tool/Functional_Test/cr1/backend
python run_tests.py
# Oppure con pytest singoli moduli:
pytest web_backend_tests/test_analysis_routes.py -v
pytest web_backend_tests/test_file_routes.py -v
pytest web_backend_tests/test_results_routes.py -v
pytest web_backend_tests/test_integration.py -v
# O tutti insieme:
pytest web_backend_tests/ -v
```

**Unit Tests AnalyticsService CR2:**  
```bash
cd MARK-Tool/MARK-Tool/Functional_Test/cr2/backend
pytest test_analytics_service.py -v
```

**API Tests Analytics CR2:**  
```bash
pytest test_analytics_routes.py -v
```

**Integration Tests Analytics CR2:**  
```bash
pytest test_integration_analytics.py -v
```

**Tutti i Test CR2 Backend:**  
```bash
python run_tests_cr2.py
# Oppure con pytest:
pytest -v
```


---  

### 2.8 Criteri di Successo Backend  

- [ ] 20 unit tests AnalyticsService passati  
- [ ] 30 API tests analytics endpoints passati  
- [ ] 4 integration tests passati  
- [ ] Test core MARK-Tool (pre-CR1) eseguiti e analizzati: CSV output identici a baseline  
- [ ] Tutti i 33 test CR1 web GUI eseguiti e analizzati per verificare assenza regressioni  
- [ ] Confronto risultati test core + CR1 baseline vs post-CR2 documentato  
- [ ] 0 bug critici  
- [ ] Performance <2s su dataset normali (analytics API)  
- [ ] Performance core analysis pipeline invariata (±10%)  
- [ ] Copertura codice >90% per analytics module

---  

## 3 Test Plan Frontend  

**In Scope:**  
- Dashboard layout e componenti UI  
- Grafici Chart.js (pie chart, bar chart, keywords chart)  
- Interazioni dashboard (click grafici → filtri)  
- Integrazione con analytics API  
- UX/UI modernizzazione  

### 3.1 Strategia di testing  

**Obiettivi di test**:  
- Verificare rendering corretto della dashboard con grafici  
- Verificare chiamate AJAX agli analytics endpoints  
- Verificare interazioni click su grafici  
- Verificare responsive design  
- Verificare cross-browser compatibility  

**Strategia e approccio**:  
- Unit test JS per dashboard.js con mock API  
- Test manuali interfaccia grafica  
- Testing cross-browser (Chrome, Firefox, Edge)  
- Testing responsive (desktop, tablet)  

**Criteri di accettazione**:  
- Grafici renderizzati correttamente  
- Dati numerici coerenti con API responses  
- Interazioni grafici funzionanti  
- Nessun errore JavaScript in console  
- Performance caricamento dashboard <1s  

---  

### 3.2 Test Cases Dashboard UI (20 totali)  

#### 3.2.1 Rendering Dashboard (5)  

* **TC-UI-D01**: Caricamento Dashboard  
  - **Descrizione**: Verificare che la dashboard carichi senza errori  
  - **Precondizioni**: Analisi completata, risultati disponibili  
  - **Passi**:  
    1. Navigare alla pagina risultati  
    2. Verificare sezione dashboard visibile  
    3. Verificare nessun errore in console  
  - **Expected**: Dashboard visibile, sezione analytics caricata  

* **TC-UI-D02**: Cards Statistiche  
  - **Descrizione**: Verificare visualizzazione cards con statistiche  
  - **Passi**:  
    1. Osservare cards nella dashboard  
    2. Verificare presenza: Total Models, Consumers, Producers  
    3. Verificare numeri corretti da API summary  
  - **Expected**: 3+ cards con valori numerici corretti  

* **TC-UI-D03**: Pie Chart Consumer/Producer  
  - **Descrizione**: Verificare rendering pie chart  
  - **Passi**:  
    1. Localizzare canvas pie chart  
    2. Verificare grafico renderizzato  
    3. Verificare 2 slice (Consumer, Producer)  
    4. Verificare colori distinti  
    5. Verificare tooltip con percentuali  
  - **Expected**: Pie chart visibile con 2 slice colorate  

* **TC-UI-D04**: Bar Chart Consumer/Producer  
  - **Descrizione**: Verificare rendering bar chart  
  - **Passi**:  
    1. Localizzare canvas bar chart  
    2. Verificare grafico renderizzato  
    3. Verificare 2 barre (Consumer, Producer)  
    4. Verificare labels asse X  
    5. Verificare valori asse Y  
  - **Expected**: Bar chart con 2 barre, assi etichettati  

* **TC-UI-D05**: Keywords Chart  
  - **Descrizione**: Verificare rendering grafico keywords  
  - **Passi**:  
    1. Localizzare canvas keywords chart  
    2. Verificare grafico renderizzato (bar orizzontale)  
    3. Verificare top-N keywords visualizzate  
    4. Verificare ordinamento per frequenza  
  - **Expected**: Bar chart orizzontale con top keywords  

---  

#### 3.2.2 Integrazione API (5)  

* **TC-UI-D06**: Chiamata API Summary  
  - **Descrizione**: Verificare che dashboard chiami /api/analytics/summary  
  - **Passi**:  
    1. Aprire DevTools Network  
    2. Caricare dashboard  
    3. Verificare richiesta GET a /api/analytics/summary  
    4. Verificare response 200  
  - **Expected**: API chiamata correttamente, response parsato  

* **TC-UI-D07**: Chiamata API Distribution  
  - **Descrizione**: Verificare chiamata /api/analytics/consumer-producer-distribution  
  - **Passi**:  
    1. Network tab aperto  
    2. Caricare dashboard  
    3. Verificare richiesta API distribution  
    4. Verificare dati usati per pie/bar chart  
  - **Expected**: API chiamata, dati popolano grafici  

* **TC-UI-D08**: Chiamata API Keywords  
  - **Descrizione**: Verificare chiamata /api/analytics/keywords  
  - **Passi**:  
    1. Network tab aperto  
    2. Caricare dashboard  
    3. Verificare richiesta con limit=10 (default)  
    4. Verificare dati usati per keywords chart  
  - **Expected**: API chiamata con parametri corretti  

* **TC-UI-D09**: Gestione Errore API  
  - **Descrizione**: Verificare gestione errore se API fallisce  
  - **Precondizioni**: Simulare errore 500 da API  
  - **Passi**:  
    1. Caricare dashboard con API offline  
    2. Verificare messaggio errore visualizzato  
    3. Verificare grafici non rotti (graceful degradation)  
  - **Expected**: Messaggio errore user-friendly, no crash JS  

* **TC-UI-D10**: Loading State  
  - **Descrizione**: Verificare indicatore caricamento durante API calls  
  - **Passi**:  
    1. Caricare dashboard  
    2. Osservare durante caricamento API  
    3. Verificare spinner/skeleton screen  
  - **Expected**: Loading indicator visibile durante fetch  

---  

#### 3.2.3 Interazioni Dashboard (5)  

* **TC-UI-D11**: Click Pie Chart Slice Consumer  
  - **Descrizione**: Click su slice Consumer filtra risultati  
  - **Passi**:  
    1. Cliccare slice "Consumer" del pie chart  
    2. Verificare chiamata /api/analytics/filter?type=consumer  
    3. Verificare tabella risultati aggiornata  
    4. Verificare solo consumer visualizzati  
  - **Expected**: Tabella filtrata, solo consumer  

* **TC-UI-D12**: Click Pie Chart Slice Producer  
  - **Descrizione**: Click su slice Producer filtra risultati  
  - **Passi**:  
    1. Cliccare slice "Producer"  
    2. Verificare filtro type=producer  
    3. Verificare tabella mostra solo producer  
  - **Expected**: Tabella filtrata, solo producer  

* **TC-UI-D13**: Click Bar Keyword  
  - **Descrizione**: Click su barra keyword filtra per quella keyword  
  - **Passi**:  
    1. Cliccare barra keyword (es. ".predict(")  
    2. Verificare chiamata filter?keyword=.predict(  
    3. Verificare tabella mostra solo quella keyword  
  - **Expected**: Tabella filtrata per keyword specifica  

* **TC-UI-D14**: Reset Filtri  
  - **Descrizione**: Pulsante reset riporta vista completa  
  - **Passi**:  
    1. Applicare filtro (es. type=consumer)  
    2. Cliccare pulsante "Reset" o "Show All"  
    3. Verificare tabella mostra tutti i risultati  
  - **Expected**: Filtri rimossi, vista completa ripristinata  

* **TC-UI-D15**: Hover Tooltip Grafici  
  - **Descrizione**: Hover su grafico mostra tooltip con dettagli  
  - **Passi**:  
    1. Hover su slice pie chart  
    2. Verificare tooltip con label e valore  
    3. Hover su barra bar chart  
    4. Verificare tooltip  
  - **Expected**: Tooltips informativi visualizzati  

---  

#### 3.2.4 Styling e Responsiveness (3)  

* **TC-UI-D16**: Layout Responsive Desktop  
  - **Descrizione**: Dashboard layout corretto su desktop  
  - **Passi**:  
    1. Visualizzare su risoluzione 1920x1080  
    2. Verificare layout griglia corretto  
    3. Verificare grafici proporzionati  
  - **Expected**: Layout ben strutturato, grafici leggibili  

* **TC-UI-D17**: Layout Responsive Tablet  
  - **Descrizione**: Dashboard adattata per tablet  
  - **Passi**:  
    1. Visualizzare su risoluzione 768x1024  
    2. Verificare grafici stack verticalmente  
    3. Verificare cards responsive  
  - **Expected**: Layout adattato, contenuto accessibile  

* **TC-UI-D18**: Stili Moderni Applicati  
  - **Descrizione**: Verificare applicazione stili CSS moderni  
  - **Passi**:  
    1. Ispezionare elementi dashboard  
    2. Verificare uso Bootstrap classes  
    3. Verificare palette colori coerente  
    4. Verificare tipografia moderna  
  - **Expected**: UI moderna e coerente con design system  

---  

#### 3.2.5 Cross-Browser Testing (2)  

* **TC-UI-D19**: Dashboard su Chrome  
  - **Descrizione**: Funzionamento su Google Chrome  
  - **Passi**:  
    1. Aprire dashboard su Chrome (latest)  
    2. Verificare rendering grafici  
    3. Verificare interazioni  
    4. Verificare console pulita (no errori)  
  - **Expected**: Funzionamento completo, no errori  

* **TC-UI-D20**: Dashboard su Firefox/Edge  
  - **Descrizione**: Funzionamento su altri browser  
  - **Passi**:  
    1. Testare su Firefox (latest)  
    2. Testare su Edge (latest)  
    3. Verificare compatibilità Chart.js  
    4. Verificare interazioni funzionanti  
  - **Expected**: Comportamento identico a Chrome  

---  

### 3.3 Criteri di Successo Frontend  

- [ ] 20 UI test cases passati  
- [ ] Dashboard renderizzata correttamente  
- [ ] Tutti i grafici funzionanti (pie, bar, keywords)  
- [ ] Interazioni click implementate e funzionanti  
- [ ] 0 errori JavaScript in console  
- [ ] Stili moderni applicati correttamente  

---  

## 4 Appendix: Category Partition Tables  

### Analytics Summary  

| TC | output_path | CSV files | Status | Response |  
|----|-------------|-----------|--------|----------|  
| ANA-01 | valid | both | 200 | Full summary |  
| ANA-02 | missing | - | 400 | Error message |  
| ANA-03 | invalid | - | 400 | Path error |  
| ANA-04 | valid | missing | 400 | No CSV error |  
| ANA-05 | valid | both | 200 | Correct values |  

### Analytics Keywords  

| TC | output_path | limit | Status | Response |  
|----|-------------|-------|--------|----------|  
| ANA-11 | valid | 10 (default) | 200 | Max 10 keywords |  
| ANA-12 | valid | 5 | 200 | Max 5 keywords |  
| ANA-13 | valid | 1 | 200 | 1 keyword |  
| ANA-14 | valid | 100 | 200 | Max 100 keywords |  
| ANA-15 | valid | 0 | 400 | Validation error |  
| ANA-16 | valid | 101 | 400 | Validation error |  

### Analytics Filter  

| TC | type | keyword | library | Status | Response |  
|----|------|---------|---------|--------|----------|  
| ANA-17 | consumer | null | null | 200 | Consumers only |  
| ANA-18 | producer | null | null | 200 | Producers only |  
| ANA-19 | invalid | null | null | 400 | Type error |  
| ANA-20 | null | .predict() | null | 200 | Filtered by keyword |  
| ANA-21 | null | null | tensorflow | 200 | Filtered by library |  
| ANA-22 | consumer | null | torch | 200 | AND filters |  

---  

## 6 Test Deliverables  

- [ ] Test execution report CR2 analytics (Excel/CSV con results)  
- [ ] Test execution report core MARK-Tool regression (CSV comparison)  
- [ ] Test execution report CR1 web GUI regression (Excel/CSV con results)  
- [ ] Analisi comparativa baseline (core + CR1) vs post-CR2 (Markdown report)  
- [ ] Bug report (Markdown o issue tracker)  
- [ ] Test coverage report (pytest --cov)  
- [ ] Performance benchmark results (core analysis + CR1 + CR2)  
- [ ] Screenshots dashboard funzionante  
- [ ] Cross-browser compatibility matrix  
