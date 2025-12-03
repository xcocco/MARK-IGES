# Frontend Tests - CR2 (Analytics Dashboard)

Test suite per le funzionalità frontend della CR2 - Analytics Dashboard.

## Setup

Installare le dipendenze:

```bash
npm install
```

## Esecuzione Test

Per eseguire tutti i test:

```bash
npm test
```

Per eseguire con coverage:

```bash
npm test -- --coverage
```

## Struttura Test

### analytics_requests.test.js

Test per il modulo `analytics_requests.js` che gestisce le chiamate API al backend Analytics.

#### Test Coverage

- **TC-FR-ANA-01 to TC-FR-ANA-04**: Test `getSummary()`
  - Chiamata endpoint corretta
  - Gestione errori backend
  - Gestione JSON invalido

- **TC-FR-ANA-05 to TC-FR-ANA-06**: Test `getDistribution()`
  - Recupero distribuzione consumer/producer
  - Gestione errori

- **TC-FR-ANA-07 to TC-FR-ANA-09**: Test `getKeywords()`
  - Chiamata con limit di default
  - Chiamata con limit personalizzato
  - Gestione errori limit invalido

- **TC-FR-ANA-10 to TC-FR-ANA-11**: Test `getLibraries()`
  - Chiamata con limit di default e personalizzato
  - Gestione liste librerie

- **TC-FR-ANA-12 to TC-FR-ANA-14**: Test `filterByType()`
  - Filtro per consumer
  - Filtro per producer
  - Gestione tipo invalido

- **TC-FR-ANA-15 to TC-FR-ANA-16**: Test `filterByKeyword()`
  - Filtro per keyword
  - Gestione caratteri speciali

- **TC-FR-ANA-17 to TC-FR-ANA-18**: Test `filterByLibrary()`
  - Filtro per libreria
  - Gestione caratteri speciali

- **TC-FR-ANA-19 to TC-FR-ANA-21**: Test `filterResults()` (filtri multipli)
  - Filtro con criteri multipli
  - Filtro con tutti i criteri
  - Filtro senza criteri (lista completa)

- **TC-FR-ANA-22 to TC-FR-ANA-23**: Test `checkHealth()`
  - Health check successo
  - Health check failure

- **TC-FR-ANA-24 to TC-FR-ANA-25**: Test error handling
  - Gestione errori di rete
  - Gestione campo error nella risposta

## Totale Test

- **25 test cases** che coprono tutte le funzioni API analytics
- **100% code coverage** delle funzioni esportate
- Tutti i test verificano:
  - Chiamate fetch corrette (URL, method, headers)
  - Parsing JSON delle risposte
  - Gestione errori backend
  - Gestione errori di rete
  - Encoding corretto dei parametri URL

## Note

I test utilizzano Jest con mock di `fetch` per simulare le risposte del backend.
Tutti i test sono completamente isolati e non richiedono un server backend attivo.
