# Test Planning - MARK-Tool Backend API

## Informazioni Documento

**Versione**: 1.0  
**Data**: 13 Novembre 2025  
**Autore**: Turco Luigi  
**Change Request**: CR1 - Backend Testing

---

## 1. Introduzione

### 1.1 Scopo

Piano di test per il backend Flask del MARK Analysis Tool basato su **category partitioning** e **regression testing** dei componenti esistenti.

### 1.2 Ambito

**In Scope:**
- API endpoints Flask (15 endpoints totali)
- Regression: exec_analysis_test, cloner_test
- Integration testing E2E

**Out of Scope:**
- Frontend testing
- Componenti di analisi ML (già testati)

---

## 2. Strategia di Testing

### 2.1 Livelli

| Livello | Strumenti | Focus |
|---------|-----------|-------|
| API Testing | pytest + Flask client | 15 endpoints |
| Integration | pytest | E2E workflows |
| Regression | unittest | exec_analysis, cloner |

### 2.2 Approccio

- **Category Partition** per ridurre test cases
- **Equivalence Partitioning** 
- **Boundary Value Analysis**

### 2.3 Criteri Accettazione

-  100% endpoint coverage
-  Regression tests pass
-  Gestione errori HTTP corretta

---

## 3. Category Partition

### 3.1 POST /api/analysis/start

**Categories:**
- input_path: [valid, invalid, missing]
- output_path: [valid, invalid, missing]
- github_csv: [valid, null]
- run_cloner: [true, false]

**Constraints:**
- If input_path OR output_path missing  400

**Test Cases:** 4

---

### 3.2 POST /api/file/upload

**Categories:**
- file: [csv, non_csv, missing]

**Test Cases:** 3

---

### 3.3 GET /api/results/view

**Categories:**
- filepath: [valid, invalid, missing]
- limit: [default, custom]

**Test Cases:** 3

---

## 4. Casi di Test API (33 totali)

### 4.1 Routes di Analisi (9)

#### TC-A01: Avvio Analisi - Input Validi
- POST /api/analysis/start
- Body: {input_path, output_path}
- Expected: 200, job_id restituito

#### TC-A02: input_path Mancante
- Expected: 400, "input_path is required"

#### TC-A03: output_path Mancante
- Expected: 400, "output_path is required"

#### TC-A04: Con Cloner
- Body: {input_path, output_path, github_csv, run_cloner: true}
- Expected: 200

#### TC-A05: Stato Job - Esistente
- GET /api/analysis/status/<job_id>
- Expected: 200, dettagli job

#### TC-A06: Stato Job - Non Esistente
- Expected: 404

#### TC-A07: Lista Job
- GET /api/analysis/jobs
- Expected: 200, array di job

#### TC-A08: Cancellazione Job
- POST /api/analysis/cancel/<job_id>
- Expected: 200

#### TC-A09: Log Job
- GET /api/analysis/logs/<job_id>
- Expected: 200, array di log

---

### 4.2 Routes di File (11)

#### TC-F01: Upload CSV - Valido
- Expected: 200, filepath

#### TC-F02: Upload - Estensione Non Valida
- Expected: 400

#### TC-F03: Upload - Nessun File
- Expected: 400

#### TC-F04: Validazione Input - Esistente
- Expected: 200

#### TC-F05: Validazione Input - Non Esistente
- Expected: 400

#### TC-F06: Validazione Input - Path Mancante
- Expected: 400

#### TC-F07: Validazione Output - Valido
- Expected: 200

#### TC-F08: Validazione CSV - Valido
- Expected: 200

#### TC-F09: Download - File Esistente
- Expected: 200, contenuto file

#### TC-F10: Download - File Non Esistente
- Expected: 404

#### TC-F11: Lista File
- Expected: 200, array di file

---

### 4.3 Routes di Risultati (12)

#### TC-R01: Lista Risultati - Path Valido
- GET /api/results/list?output_path=X
- Expected: 200, consumers/producers

#### TC-R02: Lista - Path Mancante
- Expected: 400

#### TC-R03: Lista - Path Non Esistente
- Expected: 404

#### TC-R04: Visualizza CSV - Valido
- Expected: 200, headers/rows

#### TC-R05: Visualizza - Con Paginazione
- Expected: 200, dati paginati

#### TC-R06: Visualizza - Filepath Mancante
- Expected: 400

#### TC-R07: Visualizza - File Non Esistente
- Expected: 404

#### TC-R08: Statistiche Risultati
- Expected: 200, statistiche

#### TC-R09: Ricerca - Query Valida
- Expected: 200, risultati

#### TC-R10: Ricerca - Con Filtro Colonna
- Expected: 200, risultati filtrati

#### TC-R11: Ricerca - Filepath Mancante
- Expected: 400

#### TC-R12: Ricerca - Query Mancante
- Expected: 400

---

## 5. Test di Integrazione (6)

### TC-INT-01: Analisi E2E Senza Cloner
1. Valida path
2. Avvia job
3. Poll status
4. Lista risultati
5. Visualizza CSV

### TC-INT-02: E2E Con Cloner
1. Upload CSV
2. Avvia con run_cloner
3. Verifica repos clonati
4. Risultati disponibili

### TC-INT-03: Job Concorrenti
- Avvia 2 job simultaneamente
- Entrambi completano indipendentemente

### TC-INT-04: Cancellazione Job
- Avvia job → Cancella → Verifica fallimento

### TC-INT-05: Path Input Invalido
- Job fallisce con errore

### TC-INT-06: CSV Malformato
- API ritorna 400

---

## 6. Regression Testing

### 6.1 exec_analysis_test

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

### 6.2 cloner_test

**Location:** Functional_Test/original_tests/cloner_test/

**Note:**
- Test suite verificata e aggiornata per compatibilità con il nuovo backend

**Run:**
`bash
cd cloner_test
python -m unittest cloner_test.py
`

---

## 7. Test Execution

### 7.1 Struttura

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

### 7.2 Comandi

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

## 8. Criteri di Successo

-  33 API tests passati
-  6 integration tests passati
-  exec_analysis regression tests passati
-  cloner regression tests passati
-  0 bug critici

---

## Appendice: Category Partition Tables

### Analysis Start

| TC | input | output | csv | cloner | Status |
|----|-------|--------|-----|--------|--------|
| A01 | valid | valid | null | false | 200 |
| A02 | missing | valid | null | false | 400 |
| A03 | valid | missing | null | false | 400 |
| A04 | valid | valid | valid | true | 200 |

### File Upload

| TC | file | extension | Status |
|----|------|-----------|--------|
| F01 | yes | csv | 200 |
| F02 | yes | txt | 400 |
| F03 | no | - | 400 |

### Results View

| TC | filepath | Status |
|----|----------|--------|
| R04 | valid | 200 |
| R06 | missing | 400 |
| R07 | invalid | 404 |
