
# CR1 - Test Plan  
  
## Informazione Documento  
  
Versione: 1.0  
Data: 2025-11-17  
Autore: De Pasquale Luca, De Pasquale Marco, Turco Luigi  
  
---  
  
## 1 Introduzione  
### 1.1 Scopo  
Questo documento definisce il Test Plan per la Change Request 1 (CR1) del progetto MARK-Tool.   
L'obiettivo è descrivere l'approccio, i requisiti di test,   
i casi di test principali e i criteri di   
accettazione per validare le funzionalità frontend/backend introdotte   
nella CR1 per l'implementazione della nuova GUI.  
  
### 1.2 Struttura del documento  
Il documento è diviso in test plan per lato backend e test plan per il lato frontend.  
  
---  
  
## 2 Test Plan Backend  
  
**In Scope:**  
- API endpoints Flask (15 endpoints totali)  
- Regression: exec_analysis_test, cloner_test  
- Integration testing E2E  
  
### 2.1 Strategia di testing  
#### 2.1.1 Livelli  
  
| Livello | Strumenti | Focus |  
|---------|-----------|-------|  
| API Testing | pytest + Flask client | 15 endpoints |  
| Integration | pytest | E2E workflows |  
| Regression | unittest | exec_analysis, cloner |  
  
#### 2.1.2 Approccio  
- **Category Partition** per ridurre test cases  
- **Equivalence Partitioning** - **Boundary Value Analysis**  
  
#### 2.1.3 Criteri Accettazione  
- 100% endpoint coverage  
- Regression tests pass  
- Gestione errori HTTP corretta  
  
---  
  
### 2.2 Category Partition  
  
#### 2.2.1 POST /api/analysis/start  
  
**Categories:**  
- input_path: [valid, invalid, missing]  
- output_path: [valid, invalid, missing]  
- github_csv: [valid, null]  
- run_cloner: [true, false]  
  
**Constraints:**  
- If input_path OR output_path missing  400  
  
**Test Cases:** 4  
  
---  
  
#### 2.2.2 POST /api/file/upload  
  
**Categories:**  
- file: [csv, non_csv, missing]  
  
**Test Cases:** 3  
  
---  
  
#### 2.2.3 GET /api/results/view  
  
**Categories:**  
- filepath: [valid, invalid, missing]  
- limit: [default, custom]  
  
**Test Cases:** 3  
  
---  
  
### 2.3 Casi di Test API (33 totali)  
  
#### 2.3.1 Routes di Analisi (9)  
* TC-A01: Avvio Analisi - Input Validi  
  * POST /api/analysis/start  
  * Body: {input_path, output_path}  
  * Expected: 200, job_id restituito  
  
* TC-A02: input_path Mancante  
  * Expected: 400, "input_path is required"  
  
* TC-A03: output_path Mancante  
  * Expected: 400, "output_path is required"  
  
* TC-A04: Con Cloner  
  * Body: {input_path, output_path, github_csv, run_cloner: true}  
  * Expected: 200  
  
* TC-A05: Stato Job - Esistente  
  * GET /api/analysis/status/<job_id>  
  * Expected: 200, dettagli job  
  
* TC-A06: Stato Job - Non Esistente  
  * Expected: 404  
  
* TC-A07: Lista Job  
  * GET /api/analysis/jobs  
  * Expected: 200, array di job  
  
* TC-A08: Cancellazione Job  
  * POST /api/analysis/cancel/<job_id>  
  * Expected: 200  
  
* TC-A09: Log Job  
  * GET /api/analysis/logs/<job_id>  
  * Expected: 200, array di log  
  
---  
  
#### 2.3.2 Routes di File (11)  
  
* TC-F01: Upload CSV - Valido  
  * Expected: 200, filepath  
  
* TC-F02: Upload - Estensione Non Valida  
  * Expected: 400  
  
* TC-F03: Upload - Nessun File  
 * Expected: 400  
  
* TC-F04: Validazione Input - Esistente  
  * Expected: 200  
  
* TC-F05: Validazione Input - Non Esistente  
  * Expected: 400  
  
* TC-F06: Validazione Input - Path Mancante  
  * Expected: 400  
  
* TC-F07: Validazione Output - Valido  
  * Expected: 200  
  
* TC-F08: Validazione CSV - Valido  
  * Expected: 200  
  
* TC-F09: Download - File Esistente  
  * Expected: 200, contenuto file  
  
* TC-F10: Download - File Non Esistente  
  * Expected: 404  
  
* TC-F11: Lista File  
  * Expected: 200, array di file  
  
---  
  
#### 2.3.3 Routes di Risultati (12)  
  
* TC-R01: Lista Risultati - Path Valido  
  * GET /api/results/list?output_path=X  
  * Expected: 200, consumers/producers  
  
* TC-R02: Lista - Path Mancante  
  * Expected: 400  
  
* TC-R03: Lista - Path Non Esistente  
  * Expected: 404  
  
* TC-R04: Visualizza CSV - Valido  
  * Expected: 200, headers/rows  
  
* TC-R05: Visualizza - Con Paginazione  
  * Expected: 200, dati paginati  
  
* TC-R06: Visualizza - Filepath Mancante  
  * Expected: 400  
  
* TC-R07: Visualizza - File Non Esistente  
  * Expected: 404  
  
* TC-R08: Statistiche Risultati  
  * Expected: 200, statistiche  
  
* TC-R09: Ricerca - Query Valida  
  * Expected: 200, risultati  
  
* TC-R10: Ricerca - Con Filtro Colonna  
  * Expected: 200, risultati filtrati  
  
* TC-R11: Ricerca - Filepath Mancante  
  * Expected: 400  
  
* TC-R12: Ricerca - Query Mancante  
  * Expected: 400  
  
---  
  
#### 2.3.4 Test di Integrazione (6)  
  
* TC-INT-01: Analisi E2E Senza Cloner  
  1. Valida path  
  1. Avvia job  
  1. Poll status  
  1. Lista risultati  
  1. Visualizza CSV  
  
* TC-INT-02: E2E Con Cloner  
  1. Upload CSV  
  1. Avvia con run_cloner  
  1. Verifica repos clonati  
  1. Risultati disponibili  
  
* TC-INT-03: Job Concorrenti  
  * Avvia 2 job simultaneamente  
  * Entrambi completano indipendentemente  
  
* TC-INT-04: Cancellazione Job  
  * Avvia job → Cancella → Verifica fallimento  
  
* TC-INT-05: Path Input Invalido  
  * Job fallisce con errore  
  
* TC-INT-06: CSV Malformato  
  * API ritorna 400  
  
---  
  
### 2.4 Regression Testing  
  
#### 2.4.1 exec_analysis_test  
**Location:** Functional_Test/original_tests/exec_analysis_test/  
  
**Tests:** 10 cases (EA_0 to EA_9)  
- EA_0: Non-existent input  
- EA_1: Empty input  
- EA_2: ML producer  
- EA_3: ML consumer    
- EA_4: Both producer/consumer  
- EA_5: No ML patterns  
- EA_6: Mixed projects  
- EA_7: Only consumers  
- EA_8: Multiple producers  
- EA_9: Complex scenario  
  
**Note:**  
- I test sono stati **modificati** per renderli funzionanti con le nuove dipendenze e l'architettura corrente  
- I **dati di input mancanti** sono stati **generati** per permettere l'esecuzione completa della suite di test  
- Le modifiche includono aggiornamenti ai path, fix di compatibilità con pandas, e adattamenti per i nuovi output CSV  
  
**Run:**  
`bash  
cd exec_analysis_test  
python -m unittest exec_analysis_test.py  
`  
  
#### 2.4.2 cloner_test  
**Location:** Functional_Test/original_tests/cloner_test/  
  
**Note:**  
- Test suite verificata e aggiornata per compatibilità con il nuovo backend  
  
**Run:**  
`bash  
cd cloner_test  
python -m unittest cloner_test.py  
`  
  
---  
  
### 2.5 Test Execution  
  
#### 2.5.1 Struttura  
  
`  
Functional_Test/  
 web_backend_tests/  
    test_analysis_routes.py  
    test_file_routes.py  
    test_results_routes.py  
    test_integration.py  
 original_tests/  
     exec_analysis_test/  
     cloner_test/  
`  
  
#### 2.5.2 Comandi  
  
**API Tests:**  
`bash  
pytest Functional_Test/web_backend_tests/test_*_routes.py -v  
`  
  
**Integration:**  
`bash  
pytest Functional_Test/web_backend_tests/test_integration.py -v  
`  
  
**Regression:**  
`bash  
cd Functional_Test/original_tests/exec_analysis_test  
python -m unittest exec_analysis_test.py  
`  
  
---  
  
### 2.6 Criteri di Successo  
  
- 33 API tests passati  
- 6 integration tests passati  
- exec_analysis regression tests passati  
- cloner regression tests passati  
- 0 bug critici  
  
---  
  
### Appendice: Category Partition Tables  
  
#### Analysis Start  
  
| TC | input | output | csv | cloner | Status |  
|----|-------|--------|-----|--------|--------|  
| A01 | valid | valid | null | false | 200 |  
| A02 | missing | valid | null | false | 400 |  
| A03 | valid | missing | null | false | 400 |  
| A04 | valid | valid | valid | true | 200 |  
  
#### File Upload  
  
| TC | file | extension | Status |  
|----|------|-----------|--------|  
| F01 | yes | csv | 200 |  
| F02 | yes | txt | 400 |  
| F03 | no | - | 400 |  
  
#### Results View  
  
| TC | filepath | Status |  
|----|----------|--------|  
| R04 | valid | 200 |  
| R06 | missing | 400 |  
| R07 | invalid | 404 |  
  
## 3 Test Plan Frontend  
  
**In Scope:**  
- Interazione con API  
- Funzionamento UI  
  
### 3.1 Strategia di testing  
  
**Obiettivi di test**:  
- Verificare che le funzionalità UI introdotte dalla CR1 siano corrette e stabili.  
- Verificare che le chiamate AJAX/Fetch dal frontend verso gli endpoint previsti funzionino e gestiscano correttamente gli stati (success / error / loading).  
- Verificare l'esperienza utente per i flussi principali: clone repository, avvio analisi, visualizzazione risultati, navigazione tra tab e gestione messaggi di errore.  
  
**Strategia e approccio**:  
- Eseguire unit test JS per i moduli locali con `npm test` / `jest`.  
- Utilizzo di mock (Jest + fetch-mock) per simulare interazione frontend/backend.  
- Test manuale dell'interfaccia grafica.  
  
**Criteri di accettazione**:  
- Tutti i test devono essere passati con successo.  
- Nessun bug critico.  
  
### 3.2 Test Cases  
  
#### Modulo: analysis_requests.js  
Questo modulo gestisce le richieste di avvio analisi e polling dello stato dei job verso l'endpoint `/api/analysis`.  
  
* **TC-FR-A01**: requestStatus - Endpoint corretto e parsing risposta  
  - **Descrizione**: Verifica che la funzione `requestStatus` chiami l'endpoint corretto (`GET /api/analysis/status/{jobId}`) e restituisca il JSON parsato.  
  - **Precondizioni**: Mock di fetch disponibile, endpoint `/api/analysis/status/job-1` configurato.  
  - **Passi**:  
    1. Invocare `requestStatus('job-1')`  
    2. Verificare che fetch sia stato chiamato con URL corretto e metodo GET  
    3. Verificare che gli header contengano `Accept: application/json`  
    4. Verificare che il risultato sia il JSON parsato  
  - **Input**: Job ID = `'job-1'`  
  - **Risultato atteso**: Oggetto con `{ id: 'job-1', status: 'done' }`  
  - **Postcondizioni**: Nessuna modifica di stato locale  
  
* **TC-FR-A02**: requestStatus - Lancio eccezione su errore backend  
  - **Descrizione**: Verifica che `requestStatus` lanci un'eccezione con il messaggio di errore fornito dal backend quando la risposta è `ok: false`.  
  - **Precondizioni**: Mock fetch configurato per restituire risposta con `ok: false` e messaggio errore.  
  - **Passi**:  
    1. Invocare `requestStatus('job-1')` con mock errore  
    2. Verificare che venga lanciata un'eccezione  
    3. Verificare che il messaggio sia quello fornito dal backend (`'Invalid ID'`)  
  - **Input**: Response mock con `ok: false, status: 400, message: 'Invalid ID'`  
  - **Risultato atteso**: Eccezione lanciata con messaggio `'Invalid ID'`  
  - **Postcondizioni**: Nessun effetto collaterale  
  
* **TC-FR-A03**: requestStatus - Messaggio generico se backend non fornisce dettagli  
  - **Descrizione**: Verifica che `requestStatus` lanci un'eccezione con messaggio generico quando il backend restituisce errore senza messaggio specifico.  
  - **Precondizioni**: Mock fetch per errore senza campo `message`.  
  - **Passi**:  
    1. Invocare `requestStatus('job-1')` con mock errore privo di messaggio  
    2. Verificare che venga lanciata eccezione  
    3. Verificare che il messaggio sia generico: `'Server error: 500'`  
  - **Input**: Response mock con `ok: false, status: 500`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 500'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-A04**: requestStart - POST con header e body corretti  
  - **Descrizione**: Verifica che `requestStart` invii una richiesta POST all'endpoint `/api/analysis/start` con header Content-Type corretto e body JSON contenente input_path e output_path.  
  - **Precondizioni**: Mock fetch, endpoint `/api/analysis/start` disponibile.  
  - **Passi**:  
    1. Invocare `requestStart('input.txt', 'outdir')`  
    2. Verificare che fetch sia stato chiamato con URL corretto  
    3. Verificare metodo POST  
    4. Verificare header `Content-Type: application/json` e `Accept: application/json`  
    5. Verificare body JSON contiene `input_path` e `output_path`  
  - **Input**: `input_path: 'input.txt'`, `output_path: 'outdir'`  
  - **Risultato atteso**: Risposta contiene `{ jobId: 'job-99' }`  
  - **Postcondizioni**: Job ID restituito  
  
* **TC-FR-A05**: requestStart - Inclusione parametri opzionali  
  - **Descrizione**: Verifica che `requestStart` includa il parametro opzionale `github_csv` nel body se fornito, e imposti `run_cloner` a true.  
  - **Precondizioni**: Mock fetch, parametri opzionali supportati.  
  - **Passi**:  
    1. Invocare `requestStart('in', 'out', 'repos.csv')`  
    2. Estrarre il body dalla chiamata a fetch  
    3. Verificare che `github_csv: 'repos.csv'` sia presente nel JSON  
    4. Verificare che `run_cloner: true` sia presente  
  - **Input**: `input_path: 'in'`, `output_path: 'out'`, `github_csv: 'repos.csv'`  
  - **Risultato atteso**: Body contiene `{ github_csv: 'repos.csv', run_cloner: true }`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-A06**: requestStart - Lancio eccezione su errore server  
  - **Descrizione**: Verifica che `requestStart` lanci eccezione quando il server restituisce errore 502 (Bad Gateway).  
  - **Precondizioni**: Mock fetch configurato per errore 502.  
  - **Passi**:  
    1. Invocare `requestStart('in', 'out')` con mock errore 502  
    2. Verificare che venga lanciata eccezione  
    3. Verificare messaggio sia `'Server error: 502'`  
  - **Input**: Response mock con `ok: false, status: 502`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 502'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-A07**: handleResponse - Ritorno oggetto vuoto se JSON malformato (successo)  
  - **Descrizione**: Verifica che quando la risposta è `ok: true` ma il JSON è invalido, la funzione ritorni un oggetto vuoto `{}` invece di lanciare eccezione.  
  - **Precondizioni**: Mock fetch con risposta ok ma JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestStatus('job-1')` con mock JSON invalido  
    2. Verificare che non venga lanciata eccezione  
    3. Verificare che il risultato sia `{}`  
  - **Input**: Response mock con `ok: true, json: () => throw new Error('invalid JSON')`  
  - **Risultato atteso**: Ritorno `{}`  
  - **Postcondizioni**: Degradazione graceful senza crash  
  
---  
  
#### Modulo: file_requests.js  
Questo modulo gestisce le richieste di validazione file verso l'endpoint `/api/file`.  
  
* **TC-FR-F01**: requestValidateInputFolder - POST con JSON body e ritorno parsato  
  - **Descrizione**: Verifica che `requestValidateInputFolder` invii una richiesta POST con il path della cartella e restituisca la risposta parsata.  
  - **Precondizioni**: Mock fetch, endpoint `/api/file/validate/input` configurato.  
  - **Passi**:  
    1. Invocare `requestValidateInputFolder('/path/to/input')`  
    2. Verificare che fetch sia stato chiamato con URL e metodo POST corretti  
    3. Verificare header `Content-Type: application/json`  
    4. Verificare body JSON contiene `path: '/path/to/input'`  
    5. Verificare ritorno della risposta parsata  
  - **Input**: `path: '/path/to/input'`  
  - **Risultato atteso**: `{ valid: true }`  
  - **Postcondizioni**: Validazione completata  
  
* **TC-FR-F02**: requestValidateInputFolder - Messaggio errore backend  
  - **Descrizione**: Verifica che quando il backend restituisce errore con messaggio, questo sia lanciato come eccezione.  
  - **Precondizioni**: Mock fetch con errore 400 e messaggio specifico.  
  - **Passi**:  
    1. Invocare `requestValidateInputFolder('/bad')` con mock errore  
    2. Verificare che venga lanciata eccezione  
    3. Verificare che il messaggio sia `'Invalid folder'`  
  - **Input**: Response mock con `ok: false, status: 400, message: 'Invalid folder'`  
  - **Risultato atteso**: Eccezione lanciata con messaggio `'Invalid folder'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-F03**: requestValidateInputFolder - Messaggio generico su errore senza dettagli  
  - **Descrizione**: Verifica il fallback a messaggio generico quando backend non fornisce dettagli dell'errore.  
  - **Precondizioni**: Mock fetch con errore 500 senza messaggio.  
  - **Passi**:  
    1. Invocare `requestValidateInputFolder('/error')` con mock errore generico  
    2. Verificare che venga lanciata eccezione con messaggio `'Server error: 500'`  
  - **Input**: Response mock con `ok: false, status: 500`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 500'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-F04**: requestValidateOutputFolder - POST all'endpoint corretto  
  - **Descrizione**: Verifica che `requestValidateOutputFolder` invii POST a `/api/file/validate/output` con body JSON contentente il path.  
  - **Precondizioni**: Mock fetch, endpoint configurato.  
  - **Passi**:  
    1. Invocare `requestValidateOutputFolder('/path/to/output')`  
    2. Verificare URL endpoint corretto  
    3. Verificare metodo POST  
    4. Verificare body JSON contiene `path: '/path/to/output'`  
    5. Verificare ritorno risposta parsata con `writable: true`  
  - **Input**: `path: '/path/to/output'`  
  - **Risultato atteso**: `{ writable: true }`  
  - **Postcondizioni**: Validazione output completata  
  
* **TC-FR-F05**: requestValidateOutputFolder - Eccezione con messaggio backend  
  - **Descrizione**: Verifica che errori 403 (Permission denied) siano gestiti correttamente.  
  - **Precondizioni**: Mock fetch con errore 403.  
  - **Passi**:  
    1. Invocare `requestValidateOutputFolder('/readonly')` con mock errore  
    2. Verificare che venga lanciata eccezione con messaggio `'Permission denied'`  
  - **Input**: Response mock con `ok: false, status: 403, message: 'Permission denied'`  
  - **Risultato atteso**: Eccezione con messaggio `'Permission denied'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-F06**: requestValidateCSV - POST con filepath e ritorno parsato  
  - **Descrizione**: Verifica che `requestValidateCSV` invii POST a `/api/file/validate/csv` con il filepath nel body e restituisca la validazione e il numero di righe.  
  - **Precondizioni**: Mock fetch, endpoint configurato.  
  - **Passi**:  
    1. Invocare `requestValidateCSV('data.csv')`  
    2. Verificare URL endpoint corretto  
    3. Verificare metodo POST  
    4. Verificare body contiene `filepath: 'data.csv'`  
    5. Verificare ritorno `{ valid: true, rows: 42 }`  
  - **Input**: `filepath: 'data.csv'`  
  - **Risultato atteso**: `{ valid: true, rows: 42 }`  
  - **Postcondizioni**: CSV validato  
  
* **TC-FR-F07**: requestValidateCSV - Errore generico se backend fallisce  
  - **Descrizione**: Verifica che un errore 404 (file non trovato) sia gestito correttamente.  
  - **Precondizioni**: Mock fetch con errore 404 senza messaggio.  
  - **Passi**:  
    1. Invocare `requestValidateCSV('missing.csv')` con mock errore  
    2. Verificare che venga lanciata eccezione con messaggio generico  
  - **Input**: Response mock con `ok: false, status: 404`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 404'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-F08**: handleResponse edge - Oggetto vuoto se JSON malformato (successo)  
  - **Descrizione**: Verifica che il parsing di un JSON invalido su risposta ok ritorni `{}`.  
  - **Precondizioni**: Mock fetch con `ok: true` ma JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestValidateCSV('broken.csv')` con mock JSON invalido  
    2. Verificare che non venga lanciata eccezione  
    3. Verificare ritorno `{}`  
  - **Input**: Response mock con `ok: true, json: () => throw new Error('invalid')`  
  - **Risultato atteso**: Ritorno `{}`  
  - **Postcondizioni**: Degradazione graceful  
  
* **TC-FR-F09**: handleResponse edge - Eccezione su JSON malformato con errore  
  - **Descrizione**: Verifica che quando JSON è invalido E la risposta ha errore, il messaggio di errore sia corretto.  
  - **Precondizioni**: Mock fetch con `ok: false` e JSON non parsabile.  
  - **Passi**:  
    1. Invocare `requestValidateCSV('broken.csv')` con mock errore e JSON corrotto  
    2. Verificare che venga lanciata eccezione  
    3. Verificare che il messaggio sia generico: `'Server error: 500'`  
  - **Input**: Response mock con `ok: false, status: 500, json: () => throw Error('parse fail')`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 500'`  
  - **Postcondizioni**: Nessuno  
  
---  
  
#### Modulo: results_requests.js  
Questo modulo gestisce le richieste di listing e visualizzazione risultati verso l'endpoint `/api/results`.  
  
* **TC-FR-R01**: requestList - GET con query params e ritorno parsato  
  - **Descrizione**: Verifica che `requestList` invii una richiesta GET con URL-encoded query parameter `output_path` e restituisca la lista di file parsata.  
  - **Precondizioni**: Mock fetch, endpoint `/api/results/list` configurato.  
  - **Passi**:  
    1. Invocare `requestList('/output/path')`  
    2. Verificare che fetch sia stato chiamato con URL codificato correttamente  
    3. Verificare metodo GET  
    4. Verificare header `Accept: application/json`  
    5. Verificare ritorno `{ files: ['a.csv', 'b.csv'] }`  
  - **Input**: `output_path: '/output/path'`  
  - **Risultato atteso**: `{ files: ['a.csv', 'b.csv'] }`  
  - **Postcondizioni**: Lista risultati ottenuta  
  
* **TC-FR-R02**: requestList - Eccezione con messaggio backend  
  - **Descrizione**: Verifica che un errore 400 con messaggio specifico sia lanciato come eccezione.  
  - **Precondizioni**: Mock fetch con errore 400.  
  - **Passi**:  
    1. Invocare `requestList('/bad/path')` con mock errore  
    2. Verificare che venga lanciata eccezione con messaggio `'Bad output path'`  
  - **Input**: Response mock con `ok: false, status: 400, message: 'Bad output path'`  
  - **Risultato atteso**: Eccezione lanciata con messaggio `'Bad output path'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R03**: requestList - Messaggio generico su errore 404  
  - **Descrizione**: Verifica il fallback a messaggio generico quando backend non fornisce dettagli.  
  - **Precondizioni**: Mock fetch con errore 404 senza messaggio.  
  - **Passi**:  
    1. Invocare `requestList('/missing')` con mock errore  
    2. Verificare che venga lanciata eccezione con messaggio `'Server error: 404'`  
  - **Input**: Response mock con `ok: false, status: 404`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 404'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R04**: requestList - Oggetto vuoto se JSON invalido (ok=true)  
  - **Descrizione**: Verifica che il parsing di un JSON invalido su risposta ok ritorni `{}`.  
  - **Precondizioni**: Mock fetch con `ok: true` ma JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestList('/corrupted')` con mock JSON invalido  
    2. Verificare ritorno `{}`  
  - **Input**: Response mock con `ok: true, json: () => throw Error('invalid json')`  
  - **Risultato atteso**: Ritorno `{}`  
  - **Postcondizioni**: Degradazione graceful  
  
* **TC-FR-R05**: requestList - Server error se ok=false e JSON invalido  
  - **Descrizione**: Verifica che l'errore generico sia lanciato anche se il JSON di errore è invalido.  
  - **Precondizioni**: Mock fetch con `ok: false` e JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestList('/crash')` con mock errore e JSON non parsabile  
    2. Verificare che venga lanciata eccezione con messaggio generico  
  - **Input**: Response mock con `ok: false, status: 500, json: () => throw Error('parse fail')`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 500'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R06**: requestView - GET con solo filepath  
  - **Descrizione**: Verifica che `requestView` invii GET a `/api/results/view` con filepath come query parameter.  
  - **Precondizioni**: Mock fetch, endpoint configurato.  
  - **Passi**:  
    1. Invocare `requestView('/data/result.csv')`  
    2. Verificare URL con query param `filepath` URL-encoded  
    3. Verificare metodo GET  
    4. Verificare header `Accept: application/json`  
    5. Verificare ritorno `{ rows: [1, 2, 3] }`  
  - **Input**: `filepath: '/data/result.csv'`  
  - **Risultato atteso**: `{ rows: [1, 2, 3] }`  
  - **Postcondizioni**: File risultati visualizzato  
  
* **TC-FR-R07**: requestView - GET con limit e offset  
  - **Descrizione**: Verifica che `requestView` supporti parametri opzionali `limit` e `offset` per la paginazione.  
  - **Precondizioni**: Mock fetch, endpoint supporta paginazione.  
  - **Passi**:  
    1. Invocare `requestView('/data/file.csv', 10, 20)`  
    2. Verificare URL contiene `limit=10&offset=20`  
    3. Verificare ritorno parsato  
  - **Input**: `filepath: '/data/file.csv'`, `limit: 10`, `offset: 20`  
  - **Risultato atteso**: `{ rows: ['limited'] }` con query params corretti  
  - **Postcondizioni**: Pagina di risultati ottenuta  
  
* **TC-FR-R08**: requestView - Eccezione con messaggio backend  
  - **Descrizione**: Verifica che un errore 400 con messaggio sia lanciato correttamente.  
  - **Precondizioni**: Mock fetch con errore 400.  
  - **Passi**:  
    1. Invocare `requestView('/badfile.csv')` con mock errore  
    2. Verificare che venga lanciata eccezione con messaggio `'Invalid file path'`  
  - **Input**: Response mock con `ok: false, status: 400, message: 'Invalid file path'`  
  - **Risultato atteso**: Eccezione lanciata con messaggio `'Invalid file path'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R09**: requestView - Messaggio generico su errore senza dettagli  
  - **Descrizione**: Verifica il fallback a messaggio generico su errore 500 senza dettagli.  
  - **Precondizioni**: Mock fetch con errore 500.  
  - **Passi**:  
    1. Invocare `requestView('/badfile.csv')` con mock errore generico  
    2. Verificare che venga lanciata eccezione con messaggio `'Server error: 500'`  
  - **Input**: Response mock con `ok: false, status: 500`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 500'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R10**: requestView - Oggetto vuoto se JSON invalido (ok=true)  
  - **Descrizione**: Verifica che il parsing di un JSON invalido su risposta ok ritorni `{}`.  
  - **Precondizioni**: Mock fetch con `ok: true` ma JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestView('/corrupted.csv')` con mock JSON invalido  
    2. Verificare ritorno `{}`  
  - **Input**: Response mock con `ok: true, json: () => throw Error('parse error')`  
  - **Risultato atteso**: Ritorno `{}`  
  - **Postcondizioni**: Degradazione graceful  
  
* **TC-FR-R11**: requestView - Server error se ok=false e JSON invalido  
  - **Descrizione**: Verifica che l'errore generico sia lanciato anche se il JSON di errore non è parsabile.  
  - **Precondizioni**: Mock fetch con `ok: false` e JSON corrotto.  
  - **Passi**:  
    1. Invocare `requestView('/error.csv')` con mock errore e JSON non parsabile  
    2. Verificare che venga lanciata eccezione con messaggio generico  
  - **Input**: Response mock con `ok: false, status: 503, json: () => throw Error('parse fail')`  
  - **Risultato atteso**: Eccezione con messaggio `'Server error: 503'`  
  - **Postcondizioni**: Nessuno  
  
* **TC-FR-R12**: Network failure - Eccezione su fallimento fetch  
  - **Descrizione**: Verifica che quando fetch stesso fallisce (network error), l'eccezione sia propagata correttamente.  
  - **Precondizioni**: Mock fetch configurato per rifiutare la promessa.  
  - **Passi**:  
    1. Configurare fetch per lanciare errore di rete  
    2. Invocare `requestList('/any')`   
    3. Verificare che venga lanciata eccezione con messaggio di rete  
  - **Input**: fetch mock rifiuta con `Error('Network unreachable')`  
  - **Risultato atteso**: Eccezione lanciata con messaggio `'Network unreachable'`  
  - **Postcondizioni**: Nessuno  
  
---  
  
#### Test Interfaccia Utente  
I seguenti test possono essere eseguiti manualmente aprendo il browser e interagendo direttamente con l'interfaccia web o attraverso tool di automazione (Selenium, Playwright).  
  
* **TC-GUI-M01**: Dialog di caricamento all'avvio dell'analisi  
  - **Descrizione**: Verificare che al click del pulsante "Start Analysis" compaia un dialog di caricamento che descrive il processo in corso.  
  - **Precondizioni**: Applicazione web in esecuzione su `http://localhost:5000`, file CSV caricato con successo, tab "Input" visibile con dati input configurati.  
  - **Passi**:  
    1. Navigare alla tab "Input"  
    2. Configurare i path di input e output necessari  
    3. Cliccare il pulsante "Start Analysis"  
    4. Osservare se compaia un dialog/popup di caricamento  
    5. Verificare il testo descrittivo nel dialog  
  - **Input**: Click su "Start Analysis" dopo configurazione input/output  
  - **Risultato atteso**: Dialog di caricamento visibile, con messaggio descrittivo del processo; nessun errore JavaScript in console  
  - **Postcondizioni**: Dialog rimane visibile durante il processing  
  
* **TC-GUI-M02**: Completamento analisi e messaggio di notifica nel dialog  
  - **Descrizione**: Verificare che al completamento dell'analisi il dialog mostri un messaggio di completamento e un pulsante di chiusura.  
  - **Precondizioni**: Dialog di caricamento attivo (vedi TC-GUI-M01), analisi in esecuzione nel backend.  
  - **Passi**:  
    1. Attendere il completamento dell'analisi (il backend processa e restituisce i risultati)  
    2. Osservare il dialog durante l'attesa  
    3. Verificare che il messaggio nel dialog cambi a notifica di completamento (es. "Analisi completata!" o "Processing finished!")  
    4. Verificare la presenza del pulsante di chiusura "OK"  
  - **Input**: Completamento elaborazione backend  
  - **Risultato atteso**: Messaggio di completamento visibile nel dialog, pulsante di chiusura presente e cliccabile  
  - **Postcondizioni**: Dialog pronto per la chiusura  
  
* **TC-GUI-M03**: Chiusura dialog e navigazione automatica alla tab "Output"  
  - **Descrizione**: Verificare che il click del pulsante di chiusura nel dialog chiuda il dialog e mostri automaticamente la tab "Output" con i dati dei risultati.  
  - **Precondizioni**: Dialog di completamento visibile (vedi TC-GUI-M02), pulsante di chiusura disponibile.  
  - **Passi**:  
    1. Cliccare il pulsante di chiusura nel dialog (es. "Chiudi")  
    2. Osservare la scomparsa del dialog  
    3. Verificare che la tab "Output" sia automaticamente attivata e visualizzata  
    4. Verificare che i dati di output (Consumers e Producers) siano presenti nella tab  
  - **Input**: Click sul pulsante di chiusura del dialog  
  - **Risultato atteso**: Dialog scompare, tab "Output" diventa attiva e mostra i dati di analisi (liste Consumers e Producers)  
  - **Postcondizioni**: UI pronta per la visualizzazione dei dettagli  
  
* **TC-GUI-M04**: Apertura tab CSV al click su elemento Consumers/Producers  
  - **Descrizione**: Verificare che il click su un elemento nella lista Consumers o Producers apra una nuova tab con il file CSV corrispondente.  
  - **Precondizioni**: Tab "Output" visibile con dati di Consumers e Producers disponibili.  
  - **Passi**:  
    1. Navigare alla tab "Output"  
    2. Selezionare un elemento dalla lista Consumers (es. "consumer_0.csv")  
    3. Cliccare sull'elemento per aprirlo  
    4. Osservare se una nuova tab si apra  
    5. Verificare che il contenuto della tab mostri una tabella con i dati del CSV  
    6. Verificare che l'header della tabella contenga: ProjectName, Is ML consumer, where, keyword, line_number, libraries, keywords  
  - **Input**: Click su elemento Consumers o Producers nella tab Output  
  - **Risultato atteso**: Nuova tab creata e attivata, tabella visibile con dati CSV, header colonne corretti (ProjectName, Is ML consumer, where, keyword, line_number, libraries, keywords)  
  - **Postcondizioni**: Nuova tab aperта e navigabile  
  
* **TC-GUI-M05**: Navigazione tra tab  
  - **Descrizione**: Verificare che il click su ciascuna tab mostri il contenuto corrispondente e che la navigazione sia fluida.  
  - **Precondizioni**: Interfaccia con multiple tab visibili (es. "Input", "Output", tab CSV aperte).  
  - **Passi**:  
    1. Verificare che le tab siano visibili nella barra di navigazione  
    2. Cliccare su ciascuna tab (Input → Output → tab CSV aperta)  
    3. Per ogni click, verificare che il contenuto della tab corrispondente sia visualizzato  
    4. Verificare che i dati delle tab precedenti siano conservati (quando si ritorna a una tab già visitata)  
    5. Aprire DevTools e verificare assenza di errori JavaScript  
  - **Input**: Click su diverse tab dell'interfaccia  
  - **Risultato atteso**: Transizioni fluide tra tab, contenuto corretto visualizzato per ogni tab, dati persistenti, nessun errore in console  
  - **Postcondizioni**: Tutte le tab accessibili e funzionanti  
  
* **TC-GUI-M06**: Chiusura tab CSV con pulsante "x"  
  - **Descrizione**: Verificare che il pulsante "x" su una tab CSV consenta di chiudere la tab e torni automaticamente alla tab "Output".  
  - **Precondizioni**: Tab CSV aperta (vedi TC-GUI-M04), pulsante di chiusura visibile in alto a destra della tab.  
  - **Passi**:  
    1. Aprire una tab CSV (es. consumer_0.csv)  
    2. Identificare il pulsante "x" in alto a destra della tab  
    3. Cliccare il pulsante "x"  
    4. Osservare la chiusura della tab CSV  
    5. Verificare che la tab "Output" diventi automaticamente attiva e visibile  
    6. Verificare che i dati della tab Output siano conservati (liste Consumers e Producers ancora presenti)  
  - **Input**: Click sul pulsante "x" della tab CSV  
  - **Risultato atteso**: Tab CSV chiusa, tab "Output" automaticamente attivata, dati Output conservati e visibili  
  - **Postcondizioni**: Utente ritorna alla visualizzazione complessiva dei risultati