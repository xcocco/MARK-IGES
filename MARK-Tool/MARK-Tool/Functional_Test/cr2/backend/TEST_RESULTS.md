# Report Test CR2 - Analytics Dashboard

**Data Esecuzione:** 02/12/2025 16:57:25

## Sommario

- **Test Totali:** 55
- **Passati:** 55 ✅
- **Falliti:** 0 ❌
- **Saltati:** 0 ⏭️
- **Tasso di Successo:** 100.0%

---

## Test Unitari AnalyticsService

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-AS-01 | Validate output path valid | N/A | ✅ PASS | 0.001s |
| TC-AS-02 | Validate output path invalid | N/A | ✅ PASS | 0.001s |
| TC-AS-03 | Validate output path not directory | N/A | ✅ PASS | 0.002s |
| TC-AS-04 | Validate output path missing csv | N/A | ✅ PASS | 0.003s |
| TC-AS-05 | Get summary | N/A | ✅ PASS | 0.004s |
| TC-AS-06 | Get summary unique projects | N/A | ✅ PASS | 0.005s |
| TC-AS-07 | Get summary unique libraries | N/A | ✅ PASS | 0.004s |
| TC-AS-08 | Get consumer producer distribution | N/A | ✅ PASS | 0.004s |
| TC-AS-09 | Empty csv handling | N/A | ✅ PASS | 0.009s |
| TC-AS-09 | Get consumer producer distribution empty | N/A | ✅ PASS | 0.005s |
| TC-AS-10 | Get top keywords | N/A | ✅ PASS | 0.003s |
| TC-AS-11 | Get top keywords limit respected | N/A | ✅ PASS | 0.004s |
| TC-AS-12 | Get top keywords empty dataset | N/A | ✅ PASS | 0.004s |
| TC-AS-13 | Get library distribution | N/A | ✅ PASS | 0.004s |
| TC-AS-14 | Get library distribution limit respected | N/A | ✅ PASS | 0.006s |
| TC-AS-15 | Get filtered results by type | N/A | ✅ PASS | 0.003s |
| TC-AS-16 | Get filtered results by type producer | N/A | ✅ PASS | 0.003s |
| TC-AS-17 | Get filtered results by keyword | N/A | ✅ PASS | 0.004s |
| TC-AS-18 | Get filtered results by library | N/A | ✅ PASS | 0.004s |
| TC-AS-19 | Get filtered results multiple filters | N/A | ✅ PASS | 0.003s |
| TC-AS-20 | Get filtered results limit respected | N/A | ✅ PASS | 0.015s |

---

## Test API Analytics

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-ANA-01 | Summary valid output path | N/A | ✅ PASS | 0.004s |
| TC-ANA-02 | Summary missing output path | N/A | ✅ PASS | 0.002s |
| TC-ANA-03 | Summary nonexistent path | N/A | ✅ PASS | 0.002s |
| TC-ANA-04 | Summary missing csv files | N/A | ✅ PASS | 0.003s |
| TC-ANA-05 | Summary correct values | N/A | ✅ PASS | 0.004s |
| TC-ANA-06 | Distribution valid output path | N/A | ✅ PASS | 0.004s |
| TC-ANA-07 | Distribution missing output path | N/A | ✅ PASS | 0.003s |
| TC-ANA-08 | Distribution correct percentages | N/A | ✅ PASS | 0.010s |
| TC-ANA-09 | Distribution empty dataset | N/A | ✅ PASS | 0.006s |
| TC-ANA-10 | Distribution only consumers | N/A | ✅ PASS | 0.005s |
| TC-ANA-11 | Keywords default limit | N/A | ✅ PASS | 0.004s |
| TC-ANA-12 | Keywords custom limit | N/A | ✅ PASS | 0.004s |
| TC-ANA-13 | Keywords boundary limit 1 | N/A | ✅ PASS | 0.004s |
| TC-ANA-14 | Keywords boundary limit 100 | N/A | ✅ PASS | 0.004s |
| TC-ANA-15 | Keywords invalid limit low | N/A | ✅ PASS | 0.003s |
| TC-ANA-16 | Keywords invalid limit high | N/A | ✅ PASS | 0.002s |
| TC-ANA-17 | Libraries default limit | N/A | ✅ PASS | 0.004s |
| TC-ANA-18 | Libraries custom limit | N/A | ✅ PASS | 0.005s |
| TC-ANA-19 | Libraries boundary limit 1 | N/A | ✅ PASS | 0.004s |
| TC-ANA-20 | Libraries boundary limit 100 | N/A | ✅ PASS | 0.004s |
| TC-ANA-21 | Libraries invalid limit low | N/A | ✅ PASS | 0.002s |
| TC-ANA-22 | Libraries invalid limit high | N/A | ✅ PASS | 0.002s |
| TC-ANA-23 | Filter type consumer | N/A | ✅ PASS | 0.003s |
| TC-ANA-24 | Filter type producer | N/A | ✅ PASS | 0.004s |
| TC-ANA-25 | Filter invalid type | N/A | ✅ PASS | 0.003s |
| TC-ANA-26 | Filter by keyword | N/A | ✅ PASS | 0.004s |
| TC-ANA-27 | Filter by library | N/A | ✅ PASS | 0.004s |
| TC-ANA-28 | Filter multiple filters | N/A | ✅ PASS | 0.004s |
| TC-ANA-29 | Filter limit boundary | N/A | ✅ PASS | 0.029s |
| TC-ANA-30 | Health check | N/A | ✅ PASS | 0.002s |

---

## Test di Integrazione

| Codice Test | Nome Test | Parametri | Risultato | Durata |
|-------------|-----------|-----------|-----------|---------|
| TC-INT-ANA-01 | Complete analytics workflow | N/A | ✅ PASS | 0.010s |
| TC-INT-ANA-02 | Filter and visualization workflow | N/A | ✅ PASS | 0.005s |
| TC-INT-ANA-03 | Empty dataset handling | N/A | ✅ PASS | 0.011s |
| TC-INT-ANA-04 | Large dataset performance | N/A | ✅ PASS | 0.045s |

---

## Note

- ✅ PASS: Test superato con successo
- ❌ FAIL: Test fallito
- ⏭️ SKIP: Test saltato

*Report generato automaticamente il 02/12/2025 alle 16:57:25*