# Documento di Comprensione del Sistema MARK-Tool

## Introduzione
Il tool MARK è uno strumento di analisi statica sviluppato con l’obiettivo di classificare automaticamente i progetti di machine learning in due categorie principali: ML Consumer e ML Producer. Tale classificazione consente di determinare il ruolo funzionale di ciascun progetto nell'ambito del machine learning, supportando gli sviluppatori e gli analisti nella comprensione delle finalità, delle dipendenze e del livello di contributo del progetto stesso.

## Obiettivi del Sistema
- **Supporto alla comprensione del ruolo progettuale**: Consentire a sviluppatori e analisti di individuare la funzione svolta da un progetto all’interno dell’ecosistema ML.
- **Classificazione automatica**: Fornire un meccanismo di classificazione automatico in grado di distinguere i progetti di machine learning nelle due categorie principali: ML Consumer e ML Producer.
- **Analisi statica**: Esaminare il codice sorgente e le sue dipendenze per determinare la categoria del progetto.
- **Standardizzazione della classificazione**: Offrire criteri oggettivi e ripetibili per la categorizzazione dei progetti in modo consistente.

## Funzionalità Principali
- **Gestione delle fonti dei progetti**:
    - Possibilità di selezionare uno o più progetti locali da analizzare, indicando una cartella contenente i sorgenti.

    - Possibilità di clonare automaticamente uno o più repository da GitHub, integrando così progetti remoti nell’analisi.

    - Definizione di una cartella di input che funge da contenitore dei progetti (sia locali che clonati da remoto).

- **Definizione della cartella di output**: MARK consente di specificare una cartella di output dedicata, dove vengono salvati i risultati dell’analisi statica prodotti in formato strutturato.

- **Analisi statica basata su regole**:
    - Il tool effettua un’ispezione statica del codice sorgente, che utilizza una knowledge base, contenente regole e pattern per il riconoscimento delle principali API e librerie di Machine Learning.
    
    - Rileva e classifica l’utilizzo di API ML (ad es. TensorFlow, Keras, ecc.), distinguendo tra progetti che utilizzano modelli esistenti (ML Consumers) e quelli che invece producono modelli propri (ML Producers).

- **Classificazione automatica dei progetti ML**: in base alle API individuate e alle regole della knowledge base, MARK classifica automaticamente ogni progetto nella categoria appropriata. L'output fornisce anche dettagli su ciò che ha individuato durante l'analisi che ha permesso la classificazione.

- **Interfaccia Grafica**: MARK mette a disposizione un'interfaccia grafica che semplifica l’utilizzo dello strumento: tramite un’interfaccia intuitiva l’utente può facilmente selezionare la cartella di input e di output, oltre a clonare repository da GitHub senza dover ricorrere a comandi manuali. Inoltre il tool consente di ispezionare l'output prodotto dall'analisi direttamente dall'interfaccia grafica.

## Panoramica del Sistema

MARK è una desktop app dotata di interfaccia grafica che opera sul principio che diversi tipi di attività ML lasciano "impronte digitali" distinte nel codice sorgente. Analizzando questi modelli sistematicamente, il sistema può classificare automaticamente i progetti senza intervento umano.

### Architettura del Sistema

#### Componenti di Alto Livello

```
┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  LIVELLO INPUT   │    │LIVELLO ELABORAZ.│    │ LIVELLO OUTPUT  │
├──────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Codice Sorgente│───>│ • Riconoscimento│───>| • Report di     │
│ • Repository     │    │   Pattern       │    │   Classificaz.  │
│ • Progetti       │    │ • Matching Base │    │ • Evidenze      │
│ • File           │    │   Conoscenza    │    │   Statistiche   │
└──────────────────┘    │ • Motore Regole │    └─────────────────┘
                        └─────────────────┘
```

#### Livello di Input
- **Repository di Codice Sorgente**: Progetti GitHub, codebase locali
- **Formati Multipli**: File Python, notebook Jupyter
- **Collezioni di Progetti**: Capacità di elaborazione batch
- **Fonti Flessibili**: Directory locali, repository remoti

#### Livello di Elaborazione
- **Motore di Riconoscimento Pattern**: Identifica pattern di codice specifici ML
- **Sistema Base di Conoscenza**: Database curato di firme di framework ML
- **Classificazione Basata su Regole**: Logica di decisione intelligente
- **Raccolta di Evidenze**: Traccia il ragionamento dietro le classificazioni

#### Livello di Output
- **Risultati di Classificazione**: Categorizzazione chiara Produttore/Consumatore
- **Report Dettagliati**: Spiegazioni basate su evidenze
- **Riassunti Statistici**: Insights aggregati attraverso i progetti
- **Dati Esportabili**: Formati CSV per ulteriori analisi

### Interfaccia Grafica Utente (GUI)
La schermata principale è composta da due sezioni organizzate in tabs:
**input** e **output**.
- Sezione **input**: presenta tre campi di testo per l'inserimento del path della cartella di input, output e di un file contenente gli URL delle repository GitHub da clonare.
Per ogni campo di testo è presente un pulsante **browse** che permette di selezionare il path tramite una finestra di navigazione grafica di directory del sistema.
Infine il pulsante **Start Analysis** consente di avviare l'analisi.
- Sezione **output**: questa sezione è divisa a sua volta in altre due sezioni: **Consumer** e **Producer**, in cui vengono mostrati i file generati dell'analisi.
Cliccando su uno di questi file si apre una finestra in cui vengono mostrate informazioni come *keywords*, *nome del file* e *classe*, organizzate in una tabella.

## Flusso di Lavoro del Sistema

### Fase 1: Elaborazione Input
1. **Ingestione Repository**: Accettare varie fonti di input
2. **Normalizzazione Formato**: Convertire diversi tipi di file in formato analizzabile
3. **Scoperta File**: Identificare file di codice sorgente rilevanti
4. **Preprocessamento**: Preparare file per l'analisi dei pattern

### Fase 2: Motore di Analisi
1. **Rilevamento Librerie**: Identificare framework ML in uso
2. **Matching Pattern**: Cercare pattern di codice specifici ML
3. **Analisi del Contesto**: Comprendere lo scopo dell'utilizzo ML
4. **Raccolta Evidenze**: Raccogliere informazioni di supporto

### Fase 3: Logica di Classificazione
1. **Applicazione Regole**: Applicare regole di classificazione intelligenti
2. **Valutazione Confidenza**: Valutare la forza delle evidenze
3. **Risoluzione Conflitti**: Gestire casi ambigui
4. **Presa di Decisione**: Assegnare classificazioni finali

### Fase 4: Generazione Risultati
1. **Creazione Report**: Generare report di analisi dettagliati
2. **Documentazione Evidenze**: Fornire ragionamento per le decisioni
3. **Esportazione Dati**: Formattare risultati per uso esterno
4. **Statistiche Riassuntive**: Creare insights aggregati

## Caratteristiche di Intelligenza del Sistema

### Riconoscimento Pattern Adattivo
- **Consapevolezza del Contesto**: Comprende diversi contesti di utilizzo ML
- **Evoluzione Framework**: Si adatta a nuove librerie e pattern ML
- **Riduzione Falsi Positivi**: Filtraggio intelligente di codice test/esempio
- **Punteggio di Confidenza**: Fornisce metriche di affidabilità per le classificazioni

### Meccanismi di Garanzia Qualità
- **Validazione Multi-Evidenza**: Richiede indicatori multipli per la classificazione
- **Controllo Incrociato**: Valida risultati contro fonti multiple
- **Filtraggio Rumore**: Esclude codice irrilevante (test, esempi, documentazione)
- **Controllo Coerenza**: Assicura coerenza logica nelle classificazioni

### Caratteristiche di Scalabilità
- **Elaborazione Batch**: Gestisce collezioni di progetti grandi in modo efficiente
- **Analisi Parallela**: Elabora progetti multipli simultaneamente
- **Ottimizzazione Memoria**: Uso efficiente delle risorse per codebase grandi
- **Tracciamento Progresso**: Monitora progresso dell'analisi per task a lunga durata

## Casi d'Uso e Applicazioni

### Ricerca Accademica
- **Studi su Larga Scala**: Analizzare migliaia di progetti ML per la ricerca
- **Analisi Trend**: Tracciare pattern di adozione ML nel tempo
- **Confronto Framework**: Studiare popolarità relativa degli strumenti ML
- **Evoluzione Ecosistema**: Monitorare cambiamenti nelle pratiche di sviluppo ML

### Applicazioni Aziendali
- **Auditing Codebase**: Comprendere l'utilizzo ML attraverso l'organizzazione
- **Valutazione Tecnologica**: Valutare lo stack tecnologico ML attuale
- **Pianificazione Migrazione**: Pianificare transizioni tra framework ML
- **Monitoraggio Conformità**: Assicurare che l'utilizzo ML sia allineato alle politiche

## Benefici del Sistema

### Guadagni di Efficienza
- **Analisi Automatizzata**: Elimina requisiti di revisione manuale del codice
- **Risultati Consistenti**: Fornisce criteri di classificazione uniformi
- **Elaborazione Rapida**: Analizza progetti molto più velocemente dei metodi manuali
- **Riduzione Errori**: Minimizza errori di classificazione umani

### Generazione Insights
- **Scoperta Pattern**: Rivela trend nascosti nello sviluppo ML
- **Analytics di Utilizzo**: Comprende come gli strumenti ML vengono effettivamente usati
- **Mappatura Ecosistema**: Crea viste comprehensive dei paesaggi ML
- **Supporto Decisionale**: Informa decisioni tecnologiche strategiche

### Abilitazione Ricerca
- **Risultati Riproducibili**: Metodologia consistente attraverso gli studi
- **Analisi su Larga Scala**: Abilita ricerca a scala senza precedenti
- **Studi Comparativi**: Facilita confronti di framework e approcci
- **Tracciamento Longitudinale**: Monitora cambiamenti nel tempo

## Limitazioni del Sistema e Considerazioni

### Ambito
- **Focus Linguaggio**: Principalmente progettato per progetti ML basati su Python
- **Dipendenza Pattern**: Si basa su pattern di codice riconoscibili
- **Analisi Statica**: Non può comprendere comportamento runtime
- **Copertura Framework**: Limitato a framework ML conosciuti

### Considerazioni di Accuratezza
- **Sensibilità Contesto**: Può avere difficoltà con codice altamente astratto
- **Pattern in Evoluzione**: Richiede aggiornamenti mentre le pratiche ML cambiano
- **Casi Ambigui**: Alcuni progetti possono genuinamente rientrare in entrambe le categorie
- **Implementazioni Personalizzate**: Può perdere implementazioni ML non-standard

### Requisiti Operazionali
- **Manutenzione Base Conoscenza**: Aggiornamenti regolari necessari per nuovi framework
- **Garanzia Qualità**: Validazione periodica dell'accuratezza di classificazione
- **Monitoraggio Prestazioni**: Assicurare efficienza del sistema su scala
- **Formazione Utenti**: Comprensione dell'interpretazione dei risultati
