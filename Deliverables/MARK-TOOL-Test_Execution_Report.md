# MARK-Tool - Report di Esecuzione Test

**Progetto:** MARK-Tool 
**Data Esecuzione:** 17 Novembre 2025  
**Versione:** CR1 - Backend Testing  
**Eseguito da:** Sistema di Test Automatizzato  

---

## 1. Sommario Esecutivo

Questo documento presenta i risultati completi dell'esecuzione dei test per il progetto MARK-Tool, includendo sia i **test di regressione** sui componenti esistenti che i **test sui nuovi componenti** sviluppati.

### 1.1 Risultati Complessivi

| Categoria | Test Totali | Passati | Falliti | Saltati | Tasso di Successo |
|-----------|-------------|---------|---------|---------|-------------------|
| **Test di Regressione** | 14 | 14 | 0 | 0 | 100% |
| **Test Nuovi Componenti** | 65 | 65 | 0 | 0 | 100% |
| **TOTALE** | **79** | **79** | **0** | **0** | **100%** |

### 1.2 Conclusioni

✅ **Tutti i test sono stati superati con successo**

- I componenti esistenti funzionano correttamente (test di regressione)
- I nuovi componenti backend rispettano tutti i requisiti funzionali
- Nessuna regressione rilevata
- Sistema pronto per il deployment

---

## 2. Test di Regressione

I test di regressione verificano che le funzionalità esistenti del sistema continuino a funzionare correttamente dopo le modifiche.

### 2.1 Sommario Test di Regressione

**Data Esecuzione:** 17/11/2025  
**Durata Totale:** ~17 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 14
- **Passati:** 14 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

### 2.2 Test di Exec Analysis (EA_0 - EA_9)

Test funzionali per `exec_analysis.py` - analisi di progetti ML per identificare producer e consumer.

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| EA_0 | Directory input non esistente | ✅ PASS | 0.597s |
| EA_1 | Directory input vuota | ✅ PASS | 0.701s |
| EA_2 | Singolo progetto ML producer | ✅ PASS | 0.995s |
| EA_3 | Singolo progetto ML consumer | ✅ PASS | 0.620s |
| EA_4 | Progetto producer e consumer | ✅ PASS | 0.610s |
| EA_5 | Progetti senza pattern ML | ✅ PASS | 0.630s |
| EA_6 | Un producer e un consumer | ✅ PASS | 0.617s |
| EA_7 | Solo consumer (multipli) | ✅ PASS | 0.677s |
| EA_8 | Multipli producer, un consumer | ✅ PASS | 0.601s |
| EA_9 | Multipli producer e consumer | ✅ PASS | 0.613s |

**Totale Test Exec Analysis:** 10 test - 10 passati (100%)

### 2.3 Test di Cloner (CL_0 - CL_3)

Test funzionali per `cloner.py` - clonazione di repository GitHub da file CSV.

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| CL_0 | File CSV non esistente | ✅ PASS | 0.078s |
| CL_1 | File CSV vuoto | ✅ PASS | 0.091s |
| CL_2 | Singola repository | ✅ PASS | 0.069s |
| CL_3 | Multiple repository | ✅ PASS | 0.072s |

**Totale Test Cloner:** 4 test - 4 passati (100%)

---

## 3. Test sui Nuovi Componenti (Backend API)

I test sui nuovi componenti verificano le funzionalità del nuovo backend API sviluppato per MARK-Tool.

### 3.1 Sommario Test Nuovi Componenti

**Data Esecuzione:** 17/11/2025  
**Durata Totale:** ~3 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 65
- **Passati:** 65 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

### 3.2 Route di Analisi (TC-A01 - TC-A09)

API endpoints per la gestione delle analisi ML.

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-A01 | Start analysis valid | valid-valid-None-False-200-success | ✅ PASS | 0.004s |
| TC-A01 | Start analysis valid | valid-valid-valid-True-200-success | ✅ PASS | 0.003s |
| TC-A02 | Start analysis missing fields | input_path-input_path is required | ✅ PASS | 0.002s |
| TC-A02 | Start analysis missing fields | output_path-output_path is required | ✅ PASS | 0.009s |
| TC-A02 | Start analysis no data | N/A | ✅ PASS | 0.001s |
| TC-A05 | Get job status existing | N/A | ✅ PASS | 0.003s |
| TC-A06 | Get job status nonexistent | N/A | ✅ PASS | 0.001s |
| TC-A07 | List jobs | N/A | ✅ PASS | 0.013s |
| TC-A07 | List jobs empty | N/A | ✅ PASS | 0.001s |
| TC-A08 | Cancel job | N/A | ✅ PASS | 0.011s |
| TC-A08 | Cancel nonexistent job | N/A | ✅ PASS | 0.011s |
| TC-A09 | Get job logs | N/A | ✅ PASS | 0.008s |
| TC-A09 | Get job logs with limit | N/A | ✅ PASS | 0.009s |
| TC-A09 | Get logs nonexistent job | N/A | ✅ PASS | 0.001s |

**Totale Test Route di Analisi:** 14 test - 14 passati (100%)

### 3.3 Route dei File (TC-F01 - TC-F11)

API endpoints per la gestione dei file.

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-F01 | Upload file with extension | csv-200-True | ✅ PASS | 0.052s |
| TC-F01 | Upload file with extension | txt-400-False | ✅ PASS | 0.001s |
| TC-F01 | Upload file with extension | xlsx-400-False | ✅ PASS | 0.001s |
| TC-F03 | Upload file no file | N/A | ✅ PASS | 0.001s |
| TC-F03 | Upload file empty filename | N/A | ✅ PASS | 0.001s |
| TC-F04 | Validate input folder existing | N/A | ✅ PASS | 0.001s |
| TC-F05 | Validate input folder nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F06 | Validate input folder missing path | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder valid | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder creatable | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder missing path | N/A | ✅ PASS | 0.001s |
| TC-F08 | Validate csv valid | N/A | ✅ PASS | 0.001s |
| TC-F08 | Validate csv nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F08 | Validate csv missing filepath | N/A | ✅ PASS | 0.001s |
| TC-F09 | Download file existing | N/A | ✅ PASS | 0.001s |
| TC-F10 | Download file nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F10 | Download file missing filepath | N/A | ✅ PASS | 0.001s |
| TC-F10 | Download directory instead of file | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files | N/A | ✅ PASS | 0.019s |
| TC-F11 | List files empty directory | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files missing directory | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files nonexistent directory | N/A | ✅ PASS | 0.001s |

**Totale Test Route dei File:** 22 test - 22 passati (100%)

### 3.4 Route dei Risultati (TC-R01 - TC-R12)

API endpoints per la visualizzazione e ricerca dei risultati.

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-R01 | List results valid path | N/A | ✅ PASS | 0.003s |
| TC-R02 | List results missing path | N/A | ✅ PASS | 0.001s |
| TC-R03 | List results nonexistent path | N/A | ✅ PASS | 0.001s |
| TC-R04 | View csv valid | N/A | ✅ PASS | 0.001s |
| TC-R05 | View csv with pagination | 1-0-1 | ✅ PASS | 0.001s |
| TC-R05 | View csv with pagination | 10-0-10 | ✅ PASS | 0.001s |
| TC-R05 | View csv with pagination | 5-1-5 | ✅ PASS | 0.001s |
| TC-R06 | View csv missing filepath | N/A | ✅ PASS | 0.001s |
| TC-R07 | View csv nonexistent file | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get results statistics | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get stats missing path | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get stats nonexistent path | N/A | ✅ PASS | 0.001s |
| TC-R09 | Search results valid query | N/A | ✅ PASS | 0.001s |
| TC-R10 | Search results with column filter | N/A | ✅ PASS | 0.002s |
| TC-R10 | Search results no matches | N/A | ✅ PASS | 0.001s |
| TC-R11 | Search results missing filepath | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results missing query | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results invalid filepath | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results invalid column | N/A | ✅ PASS | 0.001s |

**Totale Test Route dei Risultati:** 19 test - 19 passati (100%)

### 3.5 Test di Integrazione (TC-INT-01 - TC-INT-10)

Test end-to-end che verificano i workflow completi.

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-INT-01 | Analysis e2e without cloner | N/A | ✅ PASS | 1.011s |
| TC-INT-02 | Analysis e2e with cloner | N/A | ✅ PASS | 0.046s |
| TC-INT-03 | Concurrent jobs | N/A | ✅ PASS | 0.005s |
| TC-INT-04 | Job cancellation workflow | N/A | ✅ PASS | 0.003s |
| TC-INT-05 | Invalid input path handling | N/A | ✅ PASS | 0.003s |
| TC-INT-06 | Malformed csv handling | N/A | ✅ PASS | 0.004s |
| TC-INT-07 | Results workflow with search | N/A | ✅ PASS | 0.005s |
| TC-INT-08 | File upload and download workflow | N/A | ✅ PASS | 0.005s |
| TC-INT-09 | Health check endpoint | N/A | ✅ PASS | 0.001s |
| TC-INT-10 | Root endpoint documentation | N/A | ✅ PASS | 0.001s |

**Totale Test di Integrazione:** 10 test - 10 passati (100%)

---

## 4. Analisi della Copertura

### 4.1 Componenti Testati

#### Test di Regressione
- ✅ **exec_analysis.py** - Analisi progetti ML (10 test)
- ✅ **cloner.py** - Clonazione repository GitHub (4 test)

#### Nuovi Componenti
- ✅ **Analysis Routes** - Gestione job di analisi (14 test)
- ✅ **File Routes** - Upload, validazione, download file (22 test)
- ✅ **Results Routes** - Visualizzazione e ricerca risultati (19 test)
- ✅ **Integration** - Workflow end-to-end (10 test)

### 4.2 Tipologie di Test

| Tipologia | Numero Test | Percentuale |
|-----------|-------------|-------------|
| Unit Test | 55 | 69.6% |
| Integration Test | 10 | 12.7% |
| Regression Test | 14 | 17.7% |
| **TOTALE** | **79** | **100%** |

---

## 5. Problemi Rilevati

**Nessun problema rilevato** - Tutti i test sono stati superati con successo.

---

## Appendice A: Legenda

### Codici Test
- **EA_X:** Exec Analysis Test (Test di regressione)
- **CL_X:** Cloner Test (Test di regressione)
- **TC-AXX:** Test Analysis Routes (Nuovi componenti)
- **TC-FXX:** Test File Routes (Nuovi componenti)
- **TC-RXX:** Test Results Routes (Nuovi componenti)
- **TC-INT-XX:** Test di Integrazione (Nuovi componenti)

### Risultati
- ✅ **PASS:** Test superato con successo
- ❌ **FAIL:** Test fallito
- ⏭️ **SKIP:** Test saltato

