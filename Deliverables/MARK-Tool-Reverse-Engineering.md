# MARK Tool Reverse Engineering Document

## Introduzione
Questo documento ha lo scopo di documentare il processo di **reverse engineering**
del tool Mark.

## Struttura progetto
Il processo di reverse engineering del software ha consentito di identificare diverse 
directory presenti all’interno del progetto. 
Tra queste, la directory di principale interesse è “MARK-Tool”, 
la quale contiene il codice sorgente, scritto in Python, del tool oggetto di analisi. 
Le restanti directory non risultano strettamente necessarie alla comprensione del 
funzionamento del software, in quanto non includono porzioni di 
codice ma prevalentemente file in formato CSV, che costituiscono 
la Knowledge Base del sistema. 
Per questo motivo, tali directory non verranno descritte in maniera approfondita nel presente documento.

#### Struttura generale del progetto
```
📁 .
├─ 📁 Dataset
├─ 📁 ExecutionOverview
├─ 🗎 LICENSE.md
├─ 📁 Libraries_API_Methods
├─ 📁 MARK-Configuration Study
├─ 📁 MARK-Tool
├─ 📁 ML Projects
├─ 🗎 README.MD
└─ 🗎 README.MD.docx
```
Di seguito vengono riportate sinteticamente le directory non centrali 
all’analisi, in quanto prive di codice sorgente:
- Dataset: Descrizione directory.
- ExecutionOverview: Descrizione directory.
- Libraries_API_Methods: Descrizione directory.
- MARK-Configuration Study: Descrizione directory.
- ML Projects: Descrizione directory.

#### Struttura del codice sorgente
Come precedentemente specificato, il codice sorgente del tool si trova
nella directory "MARK-Tool" la cui struttura interna è descritta
nell'albero sottostante:
```
📁 MARK-Tool
├─ 📁 MARK-Tool
│  ├─ 📁 Categorizer
│  ├─ 📁 Functional_Test
│  ├─ 🗎 LICENSE
│  ├─ 🗎 README.md
│  ├─ 🗎 __init__.py
│  └─ 📁 cloner
└─ 🗎 __init__.py
```

- **Categorizer**: Contiene la maggior parte del codice per l'analisi statica dei progetti. Strutturato come segue: 
```
📁 Categorizer
├─ 🗎 __init__.py
├─ 📁 oracle
├─ 📁 results
└─ 📁 src
   ├─ 📁 Consumers
   ├─ 📁 GUI
   ├─ 📁 Producers
   ├─ 🗎 __init__.py
   ├─ 🗎 analyzer_base.py
   ├─ 📁 components
   ├─ 🗎 consumer_classifier_by_dict.py
   ├─ 🗎 exec_analysis.py
   ├─ 📁 library_dictionary
   └─ 🗎 producer_classifier_by_dict.py
```
- **Functional_Test**: Contiene codice di test.
- **cloner**: Componenti per la clonazione di repository da GitHub.

## Moduli principali
| Nome modulo                        | Descrizione                                                                                                                                                                                                                                                               | Path nel progetto                                               |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| **exec_analysis.py**               | Punto di Ingresso Principale.<br>Orchestra l'intera pipeline di analisi.<br>Gestisce gli argomenti da riga di comando.<br>Coordina le fasi di analisi dei produttori e consumatori.<br>Gestisce la conversione dei notebook e la risoluzione dei percorsi.                | MARK-Tool/MARK-Tool/Categorizer/src/                            |
| **analyzer_base.py**               | Classe Base Astratta.<br>Definisce le funzionalità comuni per entrambi gli analizzatori.<br>Gestisce le operazioni sui file e la gestione CSV.<br>Fornisce metodi di utilità per la costruzione di pattern regex.<br>Gestisce l'inizializzazione delle cartelle di output | MARK-Tool/MARK-Tool/Categorizer/src/                            |
| **producer_classifier_by_dict.py** | Analisi Produttori.<br>Implementa la logica di rilevamento per i produttori ML.<br>Cerca pattern API relativi all'addestramento.<br>Utilizza la base di conoscenza specifica per i produttori.<br>Genera i risultati di classificazione per i produttori.                 | MARK-Tool/MARK-Tool/Categorizer/src/                            |
| **consumer_classifier_by_dict.py** | Analisi Consumatori.<br>Implementa la logica di rilevamento per i consumatori ML.<br>Cerca pattern API relativi all'inferenza.<br>Implementa regole di rilevamento configurabili (Regole 3 e 4).<br>Utilizza la base di conoscenza specifica per i consumatori.           | MARK-Tool/MARK-Tool/Categorizer/src/                            |
| **library_extractor.py**           | Nucleo dell'Analisi Statica.<br>Estrae le dichiarazioni import dai file Python.<br>Confronta le librerie importate con la base di conoscenza.<br>Gestisce diversi formati di codifica.<br>Fornisce analisi dell'utilizzo delle librerie                                   | MARK-Tool/MARK-Tool/Categorizer/src/components/static_analysis/ |
| **gui_analysis.py**                | Punto d'ingresso per eseguire il tool con interfaccia grafica. Utilizza il modulo **exec_analysis.py** per avviare l'analisi statica dei progetti.                                                                                                                        | MARK-Tool/MARK-Tool/Categorizer/src/GUI/                        |
