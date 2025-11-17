# Report Test Funzionali MARK-Tool (Originali)

**Data Esecuzione:** 17/11/2025 16:11:57

## Sommario

- **Test Totali:** 16
- **Passati:** 14 ✅
- **Falliti:** 0 ❌
- **Saltati:** 2 ⏭️
- **Tasso di Successo:** 87.5%

---

## Exec Analysis Tests

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| EA_0 | Directory input non esistente | ✅ PASS | 0.594s |
| EA_1 | Directory input vuota | ✅ PASS | 0.586s |
| EA_2 | Singolo progetto ML producer | ✅ PASS | 0.857s |
| EA_3 | Singolo progetto ML consumer | ✅ PASS | 0.576s |
| EA_4 | Progetto producer e consumer | ✅ PASS | 0.574s |
| EA_5 | Progetti senza pattern ML | ✅ PASS | 0.578s |
| EA_6 | Un producer e un consumer | ✅ PASS | 0.656s |
| EA_7 | Solo consumer (multipli) | ✅ PASS | 0.635s |
| EA_8 | Multipli producer, un consumer | ✅ PASS | 0.588s |
| EA_9 | Multipli producer e consumer | ✅ PASS | 0.653s |

---

## Cloner Tests

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| CL_0 | File CSV non esistente | ✅ PASS | 0.702s |
| CL_1 | File CSV vuoto | ✅ PASS | 0.691s |
| CL_2 | Singola repository | ✅ PASS | 4.813s |
| CL_3 | Multiple repository | ✅ PASS | 4.133s |

---

## Altri Test

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| OT_XX | Unknown | ⏭️ SKIP | 0.000s |
| OT_XX | Unknown | ⏭️ SKIP | 0.000s |

---

## Note

- ✅ PASS: Test superato con successo
- ❌ FAIL: Test fallito
- ⏭️ SKIP: Test saltato

## Descrizione Test

### Exec Analysis Tests (EA_X)
Test funzionali per `exec_analysis.py` - analisi di progetti ML per identificare producer e consumer.

### Cloner Tests (CL_X)
Test funzionali per `cloner.py` - clonazione di repository GitHub da file CSV.

*Report generato automaticamente il 17/11/2025 alle 16:12:07*