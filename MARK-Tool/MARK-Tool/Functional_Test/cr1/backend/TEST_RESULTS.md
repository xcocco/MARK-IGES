# Report Test Backend MARK-Tool

**Data Esecuzione:** 02/12/2025 17:01:55

## Sommario

- **Test Totali:** 65
- **Passati:** 65 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100.0%

---

## Route di Analisi

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-A01 | Start analysis valid | valid-valid-None-False-200-success | ✅ PASS | 0.003s |
| TC-A01 | Start analysis valid | valid-valid-valid-True-200-success | ✅ PASS | 0.002s |
| TC-A02 | Start analysis missing fields | input_path-input_path is required | ✅ PASS | 0.001s |
| TC-A02 | Start analysis missing fields | output_path-output_path is required | ✅ PASS | 0.001s |
| TC-A02 | Start analysis no data | N/A | ✅ PASS | 0.001s |
| TC-A05 | Get job status existing | N/A | ✅ PASS | 0.002s |
| TC-A06 | Get job status nonexistent | N/A | ✅ PASS | 0.001s |
| TC-A07 | List jobs | N/A | ✅ PASS | 0.003s |
| TC-A07 | List jobs empty | N/A | ✅ PASS | 0.001s |
| TC-A08 | Cancel job | N/A | ✅ PASS | 0.002s |
| TC-A08 | Cancel nonexistent job | N/A | ✅ PASS | 0.001s |
| TC-A09 | Get job logs | N/A | ✅ PASS | 0.008s |
| TC-A09 | Get job logs with limit | N/A | ✅ PASS | 0.005s |
| TC-A09 | Get logs nonexistent job | N/A | ✅ PASS | 0.001s |

---

## Route dei File

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-F01 | Upload file with extension | csv-200-True | ✅ PASS | 0.050s |
| TC-F01 | Upload file with extension | txt-400-False | ✅ PASS | 0.002s |
| TC-F01 | Upload file with extension | xlsx-400-False | ✅ PASS | 0.002s |
| TC-F03 | Upload file no file | N/A | ✅ PASS | 0.001s |
| TC-F03 | Upload file empty filename | N/A | ✅ PASS | 0.001s |
| TC-F04 | Validate input folder existing | N/A | ✅ PASS | 0.001s |
| TC-F05 | Validate input folder nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F06 | Validate input folder missing path | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder valid | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder creatable | N/A | ✅ PASS | 0.001s |
| TC-F07 | Validate output folder missing path | N/A | ✅ PASS | 0.001s |
| TC-F08 | Validate csv valid | N/A | ✅ PASS | 0.002s |
| TC-F08 | Validate csv nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F08 | Validate csv missing filepath | N/A | ✅ PASS | 0.001s |
| TC-F09 | Download file existing | N/A | ✅ PASS | 0.003s |
| TC-F10 | Download file nonexistent | N/A | ✅ PASS | 0.001s |
| TC-F10 | Download file missing filepath | N/A | ✅ PASS | 0.001s |
| TC-F10 | Download directory instead of file | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files | N/A | ✅ PASS | 0.003s |
| TC-F11 | List files empty directory | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files missing directory | N/A | ✅ PASS | 0.001s |
| TC-F11 | List files nonexistent directory | N/A | ✅ PASS | 0.001s |

---

## Route dei Risultati

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-R01 | List results valid path | N/A | ✅ PASS | 0.004s |
| TC-R02 | List results missing path | N/A | ✅ PASS | 0.001s |
| TC-R03 | List results nonexistent path | N/A | ✅ PASS | 0.001s |
| TC-R04 | View csv valid | N/A | ✅ PASS | 0.003s |
| TC-R05 | View csv with pagination | 1-0-1 | ✅ PASS | 0.004s |
| TC-R05 | View csv with pagination | 10-0-10 | ✅ PASS | 0.002s |
| TC-R05 | View csv with pagination | 5-1-5 | ✅ PASS | 0.002s |
| TC-R06 | View csv missing filepath | N/A | ✅ PASS | 0.001s |
| TC-R07 | View csv nonexistent file | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get results statistics | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get stats missing path | N/A | ✅ PASS | 0.001s |
| TC-R08 | Get stats nonexistent path | N/A | ✅ PASS | 0.001s |
| TC-R09 | Search results valid query | N/A | ✅ PASS | 0.002s |
| TC-R10 | Search results with column filter | N/A | ✅ PASS | 0.002s |
| TC-R10 | Search results no matches | N/A | ✅ PASS | 0.002s |
| TC-R11 | Search results missing filepath | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results missing query | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results invalid filepath | N/A | ✅ PASS | 0.001s |
| TC-R12 | Search results invalid column | N/A | ✅ PASS | 0.002s |

---

## Test di Integrazione

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-INT-01 | Analysis e2e without cloner | N/A | ✅ PASS | 1.012s |
| TC-INT-02 | Analysis e2e with cloner | N/A | ✅ PASS | 0.049s |
| TC-INT-03 | Concurrent jobs | N/A | ✅ PASS | 0.004s |
| TC-INT-04 | Job cancellation workflow | N/A | ✅ PASS | 0.003s |
| TC-INT-05 | Invalid input path handling | N/A | ✅ PASS | 0.002s |
| TC-INT-06 | Malformed csv handling | N/A | ✅ PASS | 0.006s |
| TC-INT-07 | Results workflow with search | N/A | ✅ PASS | 0.007s |
| TC-INT-08 | File upload and download workflow | N/A | ✅ PASS | 0.005s |
| TC-INT-09 | Health check endpoint | N/A | ✅ PASS | 0.001s |
| TC-INT-10 | Root endpoint documentation | N/A | ✅ PASS | 0.001s |

---

## Note

- ✅ PASS: Test superato con successo
- ❌ FAIL: Test fallito
- ⏭️ SKIP: Test saltato

*Report generato automaticamente il 02/12/2025 alle 17:01:55*