# CR2 - Test Plan  

## Informazione Documento  
  
Versione: 1.0  
Data: 2025-11-26  
Autore: De Pasquale Luca, De Pasquale Marco, Turco Luigi

---  

## 1 Introduzione  
### 1.1 Scopo  
Questo documento definisce il Test Plan per la Change Request 2 (CR2) del progetto MARK-Tool.   
L'obiettivo è descrivere l'approccio, i requisiti di test,   
i casi di test principali e i criteri di   
accettazione per validare le funzionalità frontend/backend introdotte   
nella CR2 per l'aggiunta e implementazione di nuove funzionalità. 

## 3 Unit Test

Nuovi test suggeriti:

```text
# tests/web_gui/test_analytics_service.py
- test_consumer_producer_counts_from_sample_csv()
- test_percentages_sum_to_100()
- test_top_keywords_limit()

# tests/web_gui/test_analytics_routes.py
- test_analytics_summary_endpoint()
- test_consumer_producer_distribution_endpoint()
- test_keywords_endpoint()
```

## 4 Test di Integrazione

```text
# tests/integration/test_web_analytics_flow.py
- test_full_analytics_workflow()        # analisi + chiamata endpoint + verifica grafici lato frontend (parziale)
```

## 5 Checklist di Test Manuale

- [ ] Eseguire un’analisi su un progetto di esempio.  
- [ ] Verificare caricamento dashboard senza errori JS.  
- [ ] Controllare che la somma `consumer + producer + altro` coincida col totale.  
- [ ] Verificare che le percentuali nel pie chart siano coerenti con i conteggi.  
- [ ] Verificare che le keywords mostrate siano effettivamente presenti nei risultati.  
- [ ] Testare la dashboard su almeno 2 browser.  
- [ ] (Se implementato) Verificare il funzionamento dei filtri tramite click sui grafici.

---