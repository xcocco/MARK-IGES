# Report Test Funzionali MARK-Tool (Originali)

**Data Esecuzione:** 02/12/2025 14:02:31

## Sommario

- **Test Totali:** 16
- **Passati:** 13 ✅
- **Falliti:** 1 ❌
- **Saltati:** 2 ⏭️
- **Tasso di Successo:** 81.2%

---

## Exec Analysis Tests

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| EA_0 | Directory input non esistente | ✅ PASS | 0.730s |
| EA_1 | Directory input vuota | ✅ PASS | 0.710s |
| EA_2 | Singolo progetto ML producer | ❌ FAIL | 0.771s |
| EA_3 | Singolo progetto ML consumer | ✅ PASS | 0.624s |
| EA_4 | Progetto producer e consumer | ✅ PASS | 0.599s |
| EA_5 | Progetti senza pattern ML | ✅ PASS | 0.585s |
| EA_6 | Un producer e un consumer | ✅ PASS | 0.625s |
| EA_7 | Solo consumer (multipli) | ✅ PASS | 0.675s |
| EA_8 | Multipli producer, un consumer | ✅ PASS | 0.597s |
| EA_9 | Multipli producer e consumer | ✅ PASS | 0.648s |

### ❌ Errori in Exec Analysis Tests

**EA_2 - Singolo progetto ML producer**
```
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\Lib\unittest\case.py", line 58, in testPartExecutor
    yield
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\Lib\unittest\case.py", line 651, in run
    self._callTestMethod(testMethod)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.
```

---

## Cloner Tests

| Codice Test | Descrizione | Risultato | Durata |
|-------------|-------------|-----------|---------|
| CL_0 | File CSV non esistente | ✅ PASS | 1.855s |
| CL_1 | File CSV vuoto | ✅ PASS | 0.711s |
| CL_2 | Singola repository | ✅ PASS | 7.790s |
| CL_3 | Multiple repository | ✅ PASS | 4.213s |

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

*Report generato automaticamente il 02/12/2025 alle 14:02:45*