# CR2 - Analytics Dashboard Tests

Test suite per la Change Request 2 (CR2) del MARK-Tool, che aggiunge la dashboard di analytics con visualizzazione grafica dei risultati.

## Struttura

```
cr2/
├── backend/
│   ├── test_analytics_service.py      # 20 unit tests AnalyticsService
│   ├── test_analytics_routes.py       # 30 API tests (da implementare)
│   ├── test_integration_analytics.py  # 4 integration tests (da implementare)
│   ├── conftest.py                    # Pytest fixtures
│   ├── pytest.ini                     # Pytest configuration
│   ├── pytest_md_reporter.py          # Markdown report generator
│   ├── requirements-test.txt          # Test dependencies
│   ├── run_tests_cr2.py              # Test runner script
│   └── TEST_RESULTS.md               # Auto-generated test report
├── frontend/                          # Frontend tests (da implementare)
├── test_analytics_api.py              # Script E2E manuale
└── __init__.py
```

## Setup

### Prerequisiti
- Python 3.8+
- Flask server MARK-Tool in esecuzione (per E2E tests)

### Installazione dipendenze
```bash
cd backend
pip install -r requirements-test.txt
```

## Esecuzione Test

### Tutti i test CR2 backend
```bash
cd backend
python run_tests_cr2.py
```

**Note**: Eseguendo `run_tests_cr2.py`, verrà automaticamente generato un file `TEST_RESULTS.md` con un report dettagliato dei risultati dei test in formato Markdown.

### Unit tests AnalyticsService (20 tests)
```bash
pytest test_analytics_service.py -v
```

### API tests (quando implementati)
```bash
pytest test_analytics_routes.py -v
```

### Integration tests (quando implementati)
```bash
pytest test_integration_analytics.py -v
```

### Test specifici con markers
```bash
pytest -m unit -v              # Solo unit tests
pytest -m api -v               # Solo API tests
pytest -m integration -v       # Solo integration tests
```

### Coverage report
```bash
pytest --cov=../../../web_gui/services --cov-report=html --cov-report=term
```

### Manual E2E Test
```bash
# Con Flask server in esecuzione su http://127.0.0.1:5000
cd ..
python test_analytics_api.py
```

## Test Coverage

### Implementati ✅
- **AnalyticsService Unit Tests (20)**: Test delle funzioni core analytics
  - Validazione path
  - Summary calculations
  - Consumer/Producer distribution
  - Keywords aggregation
  - Library distribution
  - Filtering logic

### Da Implementare ⏳
- **Analytics API Tests (30)**: Test degli endpoint REST
- **Integration Tests (4)**: Test E2E workflow analytics
- **Frontend Tests (20)**: Test dashboard UI

## Test Plan

Riferimento completo: `Deliverables/CR2/MARK-Tool-CR2-Test-Plan.md`

### Criteri di Successo
- ✅ 20 unit tests AnalyticsService passati
- ⏳ 30 API tests analytics endpoints
- ⏳ 4 integration tests analytics workflows
- ⏳ Test regression core MARK-Tool
- ⏳ Test regression CR1 web GUI

## Troubleshooting

### Import errors
Se vedi errori di import dei moduli `services.*`:
```bash
# Verifica che il path web_gui sia corretto
cd backend
python -c "import sys; print(sys.path)"
```

### File non trovati
Assicurati di eseguire i comandi dalla directory corretta:
- `run_tests_cr2.py` → da `cr2/backend/`
- `test_analytics_api.py` → da `cr2/`

### Flask server non risponde
Per i test E2E, il server deve essere in esecuzione:
```bash
cd ../../../web_gui
python app.py
```

## Report Markdown

Quando esegui i test con `run_tests_cr2.py`, viene automaticamente generato un report dettagliato in `backend/TEST_RESULTS.md` che include:

- 📊 Sommario con statistiche (totale, passati, falliti, saltati, tasso di successo)
- 📋 Tabelle organizzate per suite di test
- ⏱️ Durata di esecuzione di ogni test
- ❌ Dettagli degli errori per i test falliti
- 🔖 Codici test standardizzati (TC-AS01, TC-API01, TC-INT01, ecc.)

Il report è compatibile con il formato usato da CR1 e viene rigenerato automaticamente ad ogni esecuzione.

## Note

- I test sono isolati e non modificano il database di produzione
- Usa fixture pytest per creare dati temporanei
- Ogni test è indipendente (no shared state)
- I test di regressione verificano che CR2 non rompa CR1
- Il file `TEST_RESULTS.md` viene generato automaticamente e può essere versionato
