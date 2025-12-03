# MARK-Tool - Report di Esecuzione Test CR2

**Progetto:** MARK-Tool
<br>
**Data Esecuzione:** 2 Dicembre 2025
<br>
**Eseguito da:** De Pasquale Luca, De Pasquale Marco, Turco Luigi


## Backend

---

### 1. Sommario Esecutivo

Questo documento presenta i risultati completi dell'esecuzione dei test per la CR2 del progetto MARK-Tool, includendo sia i **test di regressione** sui componenti esistenti che i **test sui nuovi componenti Analytics** sviluppati.

#### 1.1 Risultati Complessivi

| Categoria | Test Totali | Passati | Falliti | Saltati | Tasso di Successo |
|-----------|-------------|---------|---------|---------|-------------------|
| **Test di Regressione** | 14 | 14 | 0 | 0 | 100% |
| **Test Nuovi Componenti CR1** | 65 | 65 | 0 | 0 | 100% |
| **Test Nuovi Componenti CR2** | 57 | 57 | 0 | 0 | 100% |
| **TOTALE** | **136** | **136** | **0** | **0** | **100%** |

#### 1.2 Conclusioni

✅ **Tutti i test sono stati superati con successo**

- I componenti esistenti funzionano correttamente (test di regressione)
- I nuovi componenti Analytics backend rispettano tutti i requisiti funzionali
- Nessuna regressione rilevata sui componenti CR1
- Sistema pronto per il deployment

---

### 2. Test di Regressione

I test di regressione verificano che le funzionalità esistenti del sistema continuino a funzionare correttamente dopo le modifiche.

#### 2.1 Sommario Test di Regressione

**Data Esecuzione:** 02/12/2025  
**Durata Totale:** ~17 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 14
- **Passati:** 14 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

#### 2.2 Test di Exec Analysis (EA_0 - EA_9)

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

#### 2.3 Test di Cloner (CL_0 - CL_3)

Test funzionali per `cloner.py` - clonazione di repository GitHub da file CSV.

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| CL_0 | File CSV non esistente | ✅ PASS | 0.078s |
| CL_1 | File CSV vuoto | ✅ PASS | 0.091s |
| CL_2 | Singola repository | ✅ PASS | 0.069s |
| CL_3 | Multiple repository | ✅ PASS | 0.072s |

**Totale Test Cloner:** 4 test - 4 passati (100%)

---

### 3. Test di Regressione CR1

I test di regressione CR1 verificano che le funzionalità della CR1 continuino a funzionare dopo l'implementazione della CR2.

#### 3.1 Sommario Test Regressione CR1

**Data Esecuzione:** 02/12/2025  
**Durata Totale:** ~3 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 65
- **Passati:** 65 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

#### 3.2 Route di Analisi (TC-A01 - TC-A09)

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

#### 3.3 Route dei File (TC-F01 - TC-F11)

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

#### 3.4 Route dei Risultati (TC-R01 - TC-R12)

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

#### 3.5 Test di Integrazione CR1 (TC-INT-01 - TC-INT-10)

Test end-to-end che verificano i workflow completi della CR1.

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

**Totale Test di Integrazione CR1:** 10 test - 10 passati (100%)

---

### 4. Test sui Nuovi Componenti CR2 (Analytics API)

I test sui nuovi componenti CR2 verificano le funzionalità del nuovo Analytics API sviluppato per MARK-Tool.

#### 4.1 Sommario Test Nuovi Componenti CR2

**Data Esecuzione:** 02/12/2025  
**Durata Totale:** ~4.5 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 57
- **Passati:** 57 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

#### 4.2 Test Analytics Service (TC-AS-01 - TC-AS-20)

Test unitari per il servizio Analytics (`analytics_service.py`).

| Codice Test | Nome Test | Descrizione | Risultato | Durata |
|-------------|-----------|-------------|-----------|---------|
| TC-AS-01 | test_validate_output_path_valid | Validazione path valido | ✅ PASS | 0.002s |
| TC-AS-02 | test_validate_output_path_invalid | Validazione path inesistente | ✅ PASS | 0.001s |
| TC-AS-03 | test_validate_output_path_not_directory | Validazione path non directory | ✅ PASS | 0.003s |
| TC-AS-04 | test_validate_output_path_missing_csv | Validazione path senza CSV | ✅ PASS | 0.004s |
| TC-AS-05 | test_get_summary | Recupero summary dati | ✅ PASS | 0.005s |
| TC-AS-06 | test_get_summary_unique_projects | Conteggio progetti unici | ✅ PASS | 0.004s |
| TC-AS-07 | test_get_summary_unique_libraries | Conteggio librerie uniche | ✅ PASS | 0.004s |
| TC-AS-08 | test_get_consumer_producer_distribution | Distribuzione consumer/producer | ✅ PASS | 0.004s |
| TC-AS-09 | test_get_consumer_producer_distribution_empty | Distribuzione con dataset vuoto | ✅ PASS | 0.006s |
| TC-AS-10 | test_get_top_keywords | Recupero top keywords | ✅ PASS | 0.004s |
| TC-AS-11 | test_get_top_keywords_limit_respected | Verifica rispetto del limit | ✅ PASS | 0.015s |
| TC-AS-12 | test_get_top_keywords_empty_dataset | Keywords con dataset vuoto | ✅ PASS | 0.005s |
| TC-AS-13 | test_get_library_distribution | Distribuzione librerie | ✅ PASS | 0.004s |
| TC-AS-14 | test_get_library_distribution_limit_respected | Verifica rispetto del limit | ✅ PASS | 0.014s |
| TC-AS-15 | test_get_filtered_results_by_type | Filtro per tipo (consumer) | ✅ PASS | 0.005s |
| TC-AS-16 | test_get_filtered_results_by_type_producer | Filtro per tipo (producer) | ✅ PASS | 0.004s |
| TC-AS-17 | test_get_filtered_results_by_keyword | Filtro per keyword | ✅ PASS | 0.004s |
| TC-AS-18 | test_get_filtered_results_by_library | Filtro per library | ✅ PASS | 0.004s |
| TC-AS-19 | test_get_filtered_results_multiple_filters | Filtri multipli (AND logic) | ✅ PASS | 0.005s |
| TC-AS-20 | test_get_filtered_results_limit_respected | Verifica rispetto del limit | ✅ PASS | 0.045s |
| TC-AS-21 | test_empty_csv_handling | Gestione CSV vuoti | ✅ PASS | 0.006s |

**Totale Test Analytics Service:** 21 test - 21 passati (100%)

#### 4.3 Test Analytics API Routes (TC-ANA-01 - TC-ANA-30)

Test per gli endpoint API Analytics.

| Codice Test | Nome Test | Endpoint | Risultato | Durata |
|-------------|-----------|----------|-----------|---------|
| TC-ANA-01 | test_summary_valid_output_path | GET /api/analytics/summary | ✅ PASS | 0.006s |
| TC-ANA-02 | test_summary_missing_output_path | GET /api/analytics/summary | ✅ PASS | 0.002s |
| TC-ANA-03 | test_summary_nonexistent_path | GET /api/analytics/summary | ✅ PASS | 0.002s |
| TC-ANA-04 | test_summary_missing_csv_files | GET /api/analytics/summary | ✅ PASS | 0.005s |
| TC-ANA-05 | test_summary_correct_values | GET /api/analytics/summary | ✅ PASS | 0.005s |
| TC-ANA-06 | test_distribution_valid_output_path | GET /api/analytics/consumer-producer-distribution | ✅ PASS | 0.005s |
| TC-ANA-07 | test_distribution_missing_output_path | GET /api/analytics/consumer-producer-distribution | ✅ PASS | 0.002s |
| TC-ANA-08 | test_distribution_correct_percentages | GET /api/analytics/consumer-producer-distribution | ✅ PASS | 0.005s |
| TC-ANA-09 | test_distribution_empty_dataset | GET /api/analytics/consumer-producer-distribution | ✅ PASS | 0.007s |
| TC-ANA-10 | test_distribution_only_consumers | GET /api/analytics/consumer-producer-distribution | ✅ PASS | 0.008s |
| TC-ANA-11 | test_keywords_default_limit | GET /api/analytics/keywords | ✅ PASS | 0.005s |
| TC-ANA-12 | test_keywords_custom_limit | GET /api/analytics/keywords | ✅ PASS | 0.005s |
| TC-ANA-13 | test_keywords_boundary_limit_1 | GET /api/analytics/keywords | ✅ PASS | 0.005s |
| TC-ANA-14 | test_keywords_boundary_limit_100 | GET /api/analytics/keywords | ✅ PASS | 0.005s |
| TC-ANA-15 | test_keywords_invalid_limit_low | GET /api/analytics/keywords | ✅ PASS | 0.002s |
| TC-ANA-16 | test_keywords_invalid_limit_high | GET /api/analytics/keywords | ✅ PASS | 0.002s |
| TC-ANA-17 | test_libraries_default_limit | GET /api/analytics/libraries | ✅ PASS | 0.005s |
| TC-ANA-18 | test_libraries_custom_limit | GET /api/analytics/libraries | ✅ PASS | 0.005s |
| TC-ANA-19 | test_libraries_boundary_limit_1 | GET /api/analytics/libraries | ✅ PASS | 0.005s |
| TC-ANA-20 | test_libraries_boundary_limit_100 | GET /api/analytics/libraries | ✅ PASS | 0.005s |
| TC-ANA-21 | test_libraries_invalid_limit_low | GET /api/analytics/libraries | ✅ PASS | 0.002s |
| TC-ANA-22 | test_libraries_invalid_limit_high | GET /api/analytics/libraries | ✅ PASS | 0.002s |
| TC-ANA-23 | test_filter_type_consumer | GET /api/analytics/filter | ✅ PASS | 0.006s |
| TC-ANA-24 | test_filter_type_producer | GET /api/analytics/filter | ✅ PASS | 0.006s |
| TC-ANA-25 | test_filter_invalid_type | GET /api/analytics/filter | ✅ PASS | 0.002s |
| TC-ANA-26 | test_filter_by_keyword | GET /api/analytics/filter | ✅ PASS | 0.006s |
| TC-ANA-27 | test_filter_by_library | GET /api/analytics/filter | ✅ PASS | 0.006s |
| TC-ANA-28 | test_filter_multiple_filters | GET /api/analytics/filter | ✅ PASS | 0.006s |
| TC-ANA-29 | test_filter_limit_boundary | GET /api/analytics/filter | ✅ PASS | 0.065s |
| TC-ANA-30 | test_health_check | GET /api/analytics/health | ✅ PASS | 0.002s |

**Totale Test Analytics API Routes:** 30 test - 30 passati (100%)

#### 4.4 Test di Integrazione CR2 (TC-INT-ANA-01 - TC-INT-ANA-04)

Test end-to-end che verificano i workflow completi Analytics.

| Codice Test | Nome Test | Descrizione | Risultato | Durata |
|-------------|-----------|-------------|-----------|---------|
| TC-INT-ANA-01 | test_complete_analytics_workflow | Workflow completo analytics end-to-end | ✅ PASS | 0.035s |
| TC-INT-ANA-02 | test_filter_and_visualization_workflow | Workflow filtro e visualizzazione | ✅ PASS | 0.018s |
| TC-INT-ANA-03 | test_empty_dataset_handling | Gestione dataset vuoto end-to-end | ✅ PASS | 0.045s |
| TC-INT-ANA-04 | test_large_dataset_performance | Test performance con dataset grande | ✅ PASS | 0.185s |

**Totale Test di Integrazione CR2:** 6 test - 6 passati (100%)

**Nota:** TC-INT-ANA-04 include test di performance su 1200+ records, verificando che i tempi di risposta siano < 2 secondi per tutti gli endpoint.

---

### 5. Analisi della Copertura

#### 5.1 Componenti Testati

#### Test di Regressione
- ✅ **exec_analysis.py** - Analisi progetti ML (10 test)
- ✅ **cloner.py** - Clonazione repository GitHub (4 test)

#### Componenti CR1 (Regressione)
- ✅ **Analysis Routes** - Gestione job di analisi (14 test)
- ✅ **File Routes** - Upload, validazione, download file (22 test)
- ✅ **Results Routes** - Visualizzazione e ricerca risultati (19 test)
- ✅ **Integration CR1** - Workflow end-to-end (10 test)

#### Nuovi Componenti CR2
- ✅ **Analytics Service** - Logica di business analytics (21 test)
- ✅ **Analytics API Routes** - Endpoint REST API analytics (30 test)
- ✅ **Integration CR2** - Workflow analytics end-to-end (6 test)

#### 5.2 Tipologie di Test

| Tipologia | Numero Test | Percentuale |
|-----------|-------------|-------------|
| Unit Test | 106 | 77.9% |
| Integration Test | 16 | 11.8% |
| Regression Test | 14 | 10.3% |
| **TOTALE** | **136** | **100%** |

#### 5.3 Copertura Funzionale CR2

| Funzionalità | Endpoint | Test Coverage | Status |
|--------------|----------|---------------|--------|
| Summary Analytics | `/api/analytics/summary` | 5 test | ✅ 100% |
| Distribution Analytics | `/api/analytics/consumer-producer-distribution` | 5 test | ✅ 100% |
| Keywords Analytics | `/api/analytics/keywords` | 6 test | ✅ 100% |
| Libraries Analytics | `/api/analytics/libraries` | 6 test | ✅ 100% |
| Filter Results | `/api/analytics/filter` | 7 test | ✅ 100% |
| Health Check | `/api/analytics/health` | 1 test | ✅ 100% |
| Integration Workflows | N/A | 6 test | ✅ 100% |
| Service Layer | N/A | 21 test | ✅ 100% |

---

### 6. Problemi Rilevati

**Nessun problema rilevato** - Tutti i test sono stati superati con successo.

## Frontend

---

### 1. Sommario Esecutivo

Questa sezione riporta i risultati dell'esecuzione dei test sul frontend per la CR2 del progetto MARK-Tool.

#### 1.1 Risultati Complessivi

| Categoria                | Test Totali | Passati | Falliti | Saltati | Tasso di Successo |
|-------------------------|-------------|---------|---------|---------|-------------------|
| **Frontend CR1 (Regressione)** | 28          | 28      | 0       | 0       | 100%              |
| **Frontend CR2 (Analytics API)** | 25          | 25      | 0       | 0       | 100%              |
| **TOTALE**              | **53**      | **53**  | **0**   | **0**   | **100%**          |

#### 1.2 Conclusioni

✅ **Tutti i test frontend sono stati superati con successo**

- Le funzionalità frontend CR1 continuano a funzionare correttamente
- Le nuove funzionalità Analytics API (CR2) sono completamente testate
- Nessuna regressione rilevata
- Test manuali GUI completati con successo

---

### 2. Test Automatizzati Frontend

#### 2.1 Test di Regressione Frontend CR1

**Data Esecuzione:** 02/12/2025  
**Durata Totale:** ~2.4 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 28
- **Passati:** 28 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%
#### 2.2 Tabella Dettagliata Test Case CR1

#### 2.1 Tabella Dettagliata Test Case CR1

| ID Test | Suite | Descrizione | Stato |
|--------|-------|-------------|-------|
| TC-FR-A01 | analysis_requests | Verifica chiamata endpoint status e parsing risposta | ✅ PASS |
| TC-FR-A02 | analysis_requests | Gestione errore backend con messaggio | ✅ PASS |
| TC-FR-A03 | analysis_requests | Gestione errore backend senza messaggio | ✅ PASS |
| TC-FR-A04 | analysis_requests | Verifica POST start con header/body corretti | ✅ PASS |
| TC-FR-A05 | analysis_requests | Verifica parametri opzionali github_csv e run_cloner | ✅ PASS |
| TC-FR-A06 | analysis_requests | Gestione errore server in start | ✅ PASS |
| TC-FR-A07 | analysis_requests | Gestione parsing JSON non valido (status) | ✅ PASS |
| TC-FR-F01 | file_requests | Verifica POST validazione input folder e parsing | ✅ PASS |
| TC-FR-F02 | file_requests | Gestione errore backend con messaggio (input folder) | ✅ PASS |
| TC-FR-F03 | file_requests | Gestione errore backend senza messaggio (input folder) | ✅ PASS |
| TC-FR-F04 | file_requests | Verifica POST validazione output folder e parsing | ✅ PASS |
| TC-FR-F05 | file_requests | Gestione errore backend con messaggio (output folder) | ✅ PASS |
| TC-FR-F06 | file_requests | Verifica POST validazione CSV e parsing | ✅ PASS |
| TC-FR-R01 | results_requests | Verifica GET list con query params e parsing | ✅ PASS |
| TC-FR-R02 | results_requests | Gestione errore backend con messaggio (list) | ✅ PASS |
| TC-FR-R03 | results_requests | Gestione errore backend senza messaggio (list) | ✅ PASS |
| TC-FR-R04 | results_requests | Gestione parsing JSON non valido (list) | ✅ PASS |
| TC-FR-R05 | results_requests | Gestione errore server e parsing fallito (list) | ✅ PASS |
| TC-FR-R06 | results_requests | Verifica GET view solo filepath e parsing | ✅ PASS |
| TC-FR-R07 | results_requests | Verifica GET view con limit/offset e parsing | ✅ PASS |
| TC-FR-R08 | results_requests | Gestione errore backend con messaggio (view) | ✅ PASS |
| TC-FR-R09 | results_requests | Gestione errore backend senza messaggio (view) | ✅ PASS |
| TC-FR-R10 | results_requests | Gestione parsing JSON non valido (view) | ✅ PASS |
| TC-FR-R11 | results_requests | Gestione errore server e parsing fallito (view) | ✅ PASS |
| TC-FR-R12 | results_requests | Gestione errore di rete (fetch rejects) | ✅ PASS |

---

#### 2.3 Test Frontend CR2 (Analytics API Requests)

**Data Esecuzione:** 02/12/2025  
**Durata Totale:** ~0.5 secondi  
**Risultato:** ✅ **TUTTI I TEST PASSATI**

- **Test Totali:** 25
- **Passati:** 25 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100%

#### 2.4 Tabella Dettagliata Test Case CR2 (analytics_requests.js)

| ID Test | Funzione | Descrizione | Stato |
|---------|----------|-------------|-------|
| TC-FR-ANA-01 | getSummary | Chiamata endpoint corretta e parsing dati | ✅ PASS |
| TC-FR-ANA-02 | getSummary | Gestione errore backend con messaggio | ✅ PASS |
| TC-FR-ANA-03 | getSummary | Gestione errore generico senza messaggio | ✅ PASS |
| TC-FR-ANA-04 | getSummary | Gestione JSON invalido | ✅ PASS |
| TC-FR-ANA-05 | getDistribution | Chiamata endpoint distribuzione corretta | ✅ PASS |
| TC-FR-ANA-06 | getDistribution | Gestione errore risposta | ✅ PASS |
| TC-FR-ANA-07 | getKeywords | Chiamata con limit di default (10) | ✅ PASS |
| TC-FR-ANA-08 | getKeywords | Chiamata con limit personalizzato | ✅ PASS |
| TC-FR-ANA-09 | getKeywords | Gestione errore limit invalido | ✅ PASS |
| TC-FR-ANA-10 | getLibraries | Chiamata con limit di default (10) | ✅ PASS |
| TC-FR-ANA-11 | getLibraries | Chiamata con limit personalizzato | ✅ PASS |
| TC-FR-ANA-12 | filterByType | Filtro per tipo consumer | ✅ PASS |
| TC-FR-ANA-13 | filterByType | Filtro per tipo producer | ✅ PASS |
| TC-FR-ANA-14 | filterByType | Gestione tipo invalido | ✅ PASS |
| TC-FR-ANA-15 | filterByKeyword | Filtro per keyword | ✅ PASS |
| TC-FR-ANA-16 | filterByKeyword | Gestione caratteri speciali in keyword | ✅ PASS |
| TC-FR-ANA-17 | filterByLibrary | Filtro per library | ✅ PASS |
| TC-FR-ANA-18 | filterByLibrary | Gestione caratteri speciali in library | ✅ PASS |
| TC-FR-ANA-19 | filterResults | Filtri multipli (AND logic) | ✅ PASS |
| TC-FR-ANA-20 | filterResults | Filtro con tutti i criteri | ✅ PASS |
| TC-FR-ANA-21 | filterResults | Filtro senza criteri (lista completa) | ✅ PASS |
| TC-FR-ANA-22 | checkHealth | Chiamata health endpoint | ✅ PASS |
| TC-FR-ANA-23 | checkHealth | Gestione health check failure | ✅ PASS |
| TC-FR-ANA-24 | Error handling | Propagazione errori di rete | ✅ PASS |
| TC-FR-ANA-25 | Error handling | Gestione campo error nella risposta | ✅ PASS |

---

#### 4.1 Componenti Testati

**CR1 (Regressione - Automatizzati)**
- **analysis_requests.js**: API analisi, polling, error handling (7 test)
- **file_requests.js**: Validazione input/output/CSV, error handling (6 test)
- **results_requests.js**: Listing risultati, visualizzazione CSV, errori di rete (15 test)

**CR2 (Automatizzati)**
- **analytics_requests.js**: API analytics, filtri, distribuzione, keywords, libraries (25 test)

**CR2 (Manuali)**
- **Dashboard Analytics**: Visualizzazione statistiche e grafici (7 test)
- **Filtri e Ricerca**: Funzionalità di filtraggio risultati (6 test)

#### 4.2 Statistiche Test Automatizzati vs Manuali

| Tipo | Numero Test | Percentuale |
|------|-------------|-------------|
| Test Automatizzati (Jest) | 53 | 80.3% |
| Test Manuali GUI | 13 | 19.7% |
| **TOTALE** | **66** | **100%** | ✅ PASS |
| TC-GUI-CR2-03 | Visualizzazione tabella Top Keywords con conteggi corretti | ✅ PASS |
| TC-GUI-CR2-04 | Visualizzazione tabella Top Libraries con conteggi corretti | ✅ PASS |
| TC-GUI-CR2-05 | Aggiornamento automatico dashboard dopo analisi completata | ✅ PASS |
| TC-GUI-CR2-06 | Gestione errori di caricamento dati analytics | ✅ PASS |
| TC-GUI-CR2-07 | Responsive design dashboard su diverse risoluzioni | ✅ PASS |

#### 3.2 Filtri e Ricerca

| ID Test | Descrizione | Stato |
|---------|-------------|-------|
| TC-GUI-CR2-08 | Filtro per tipo (Consumer/Producer) funzionante | ✅ PASS |
| TC-GUI-CR2-09 | Filtro per keyword funzionante | ✅ PASS |
| TC-GUI-CR2-10 | Filtro per library funzionante | ✅ PASS |
| TC-GUI-CR2-11 | Applicazione filtri multipli (AND logic) | ✅ PASS |
| TC-GUI-CR2-12 | Reset filtri funzionante | ✅ PASS |
| TC-GUI-CR2-13 | Visualizzazione risultati filtrati in tabella | ✅ PASS |

#### 3.3 Test di Regressione GUI CR1

| ID Test | Descrizione | Stato |
|---------|-------------|-------|
| TC-GUI-M01 | Dialog di caricamento all'avvio dell'analisi | ✅ PASS |
| TC-GUI-M02 | Completamento analisi e messaggio di notifica nel dialog | ✅ PASS |
| TC-GUI-M03 | Chiusura dialog e navigazione automatica alla tab "Output" | ✅ PASS |
| TC-GUI-M04 | Apertura tab CSV al click su elemento Consumers/Producers | ✅ PASS |
| TC-GUI-M05 | Navigazione tra tab | ✅ PASS |
| TC-GUI-M06 | Chiusura tab CSV con pulsante "x" | ✅ PASS |

**Nota:** Tutti i test manuali GUI sono stati superati con successo. Le funzionalità analytics sono state integrate senza impattare negativamente le funzionalità CR1 esistenti.

---

### 4. Analisi della Copertura Frontend

#### 4.1 Componenti Testati

**CR1 (Regressione)**
- **analysis_requests.js**: API analisi, polling, error handling (7 test)
- **file_requests.js**: Validazione input/output/CSV, error handling (6 test)
- **results_requests.js**: Listing risultati, visualizzazione CSV, errori di rete (15 test)

**CR2 (Manuali)**
- **Dashboard Analytics**: Visualizzazione statistiche e grafici (7 test)
- **Filtri e Ricerca**: Funzionalità di filtraggio risultati (6 test)

---

### 5. Problemi Rilevati

**Nessun problema rilevato** - Tutti i test sono stati superati con successo.

---

## Appendice A: Legenda

### Codici Test
- **EA_X:** Exec Analysis Test (Test di regressione)
- **CL_X:** Cloner Test (Test di regressione)
- **TC-AXX:** Test Analysis Routes (CR1)
- **TC-FXX:** Test File Routes (CR1)
- **TC-RXX:** Test Results Routes (CR1)
- **TC-INT-XX:** Test di Integrazione (CR1)
- **TC-AS-XX:** Test Analytics Service (CR2)
- **TC-ANA-XX:** Test Analytics API Routes (CR2)
- **TC-INT-ANA-XX:** Test di Integrazione Analytics (CR2)
- **TC-FR-AXX:** Test analysis_requests.js (Frontend CR1)
- **TC-FR-FXX:** Test file_requests.js (Frontend CR1)
- **TC-FR-RXX:** Test results_requests.js (Frontend CR1)
- **TC-FR-ANA-XX:** Test analytics_requests.js (Frontend CR2)
- **TC-GUI-MXX:** Test GUI manuali (CR1)
- **TC-GUI-CR2-XX:** Test GUI manuali (CR2)

### Risultati
- ✅ **PASS:** Test superato con successo
- ❌ **FAIL:** Test fallito
- ⏭️ **SKIP:** Test saltato

### Endpoint Analytics API (CR2)
- **GET /api/analytics/summary** - Ottiene statistiche riassuntive
- **GET /api/analytics/consumer-producer-distribution** - Distribuzione consumer/producer
- **GET /api/analytics/keywords** - Top keywords utilizzate
- **GET /api/analytics/libraries** - Distribuzione librerie ML
- **GET /api/analytics/filter** - Filtra risultati per tipo/keyword/library
- **GET /api/analytics/health** - Health check del servizio analytics
