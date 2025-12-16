# Analisi di Impatto: Integrazione Componente LLM per Assistenza Intelligente

## Informazioni Documento

**Versione**: 1.0  
**Data**: 2025-12-05  
**Autore**: Turco Luigi

## Descrizione Documento

Questo documento fornisce un'analisi di impatto per l'integrazione di una componente Large Language Model (LLM) nel MARK Analysis Tool. La componente consentirà di formulare interrogazioni relative al dominio applicativo del progetto di Machine Learning fornito in input al sistema, al fine di supportarne l'analisi e la comprensione da parte dell'utente.

**Stato Attuale**: GUI web con dashboard analytics (CR1+CR2), risultati presentati in forma tabellare e grafica  
**Stato Proposto**: GUI web arricchita con assistente LLM conversazionale per spiegazioni contestuali e interrogazioni sul progetto analizzato  
**Complessità della Change Request**: Media–Alta  
**Sforzo Stimato**: 2–3 settimane (building sulla base dell'architettura web già introdotta in CR1 e CR2)

---

## 1. Architettura Attuale della GUI Web (post-CR1+CR2)

### 1.1 Implementazione Esistente

**Percorso**: `MARK-Tool/MARK-Tool/web_gui/`

**File principali** (da CR1+CR2):
- `app.py` – Entry point Flask
- `config.py` – Configurazione
- `routes/analysis_routes.py` – Endpoint avvio analisi
- `routes/file_routes.py` – Endpoint upload/download file
- `routes/results_routes.py` – Endpoint visualizzazione risultati (lista CSV, viewer)
- `routes/analytics_routes.py` – Endpoint dashboard analytics
- `services/analysis_service.py` – Ponte verso `exec_analysis.py`
- `services/file_service.py` – Gestione upload/validazione
- `services/analytics_service.py` – Aggregazione dati per dashboard
- `templates/` – `index.html`, `dashboard.html`
- `static/` – CSS/JS, Chart.js per grafici

### 1.2 Funzionalità Attuali Rilevanti

#### Input/Workflow
1. Form web per:
   - percorso cartella input,
   - percorso cartella output,
   - upload CSV GitHub (opzionale).
2. Endpoint backend per avvio analisi via `analysis_service`.
3. Persistenza dei risultati in CSV (Producer/Consumer).

#### Output
1. Elenco file risultati per Consumers e Producers (lista CSV).
2. Viewer CSV web (tabella con scrolling).
3. Dashboard analytics con grafici (pie chart consumer/producer, istogrammi, keywords).
4. **Nessuna capacità di spiegazione contestuale automatica o interazione conversazionale**.

### 1.3 Punti di Forza
- Architettura già separata in routes/services/templates.
- Riutilizzo della logica di analisi esistente (`exec_analysis.py`).
- Dashboard analytics già implementata (CR2).
- Struttura pronta per estensioni API.

### 1.4 Limiti Attuali
- Interfaccia puramente visuale (grafici/tabelle), senza interpretazione semantica.
- Manca un layer intelligente che possa:
  - spiegare il **perché** di una classificazione Producer/Consumer;
  - inferire il **dominio applicativo** del progetto analizzato;
  - rispondere a **domande specifiche** dell'utente sul progetto.
- L'utente deve interpretare manualmente i risultati tecnici (keywords, librerie).

---

## 2. Architettura Proposta (Estensione con LLM)

### 2.1 Obiettivi della Change Request

1. **Abilitare comprensione facilitata** dei risultati MARK tramite spiegazioni generate da LLM.
2. **Introdurre assistente conversazionale** che permetta all'utente di:
   - porre domande sul progetto analizzato (es. "Perché è un Producer?"),
   - inferire il dominio applicativo (es. "Computer Vision", "NLP"),
   - ottenere spiegazioni tecniche sulle API rilevate.
3. **Esporre dati aggregati e contesto via nuovi endpoint backend** dedicati all'LLM, in grado di:
   - fornire contesto progetto (README, dependencies, risultati analisi);
   - gestire conversazioni con history;
   - generare spiegazioni automatiche al completamento dell'analisi.

### 2.2 Stack Tecnologico (LLM locale)

- **LLM Engine**: LM Studio con modelli locali (LLaMA 3.1 8B Instruct).
- **Architettura Riutilizzabile**: Classe base da progetto esistente SENEM Smart Student (`textGenerationManager.py`).
- **Nuovo Adapter**: `lmstudio_manager.py` per connessione LM Studio.
- **System Prompts**: File dedicati che insegnano all'LLM la metodologia MARK (Producer/Consumer, Knowledge Base).

### 2.3 Nuovi Endpoint API Proposti

All'interno di un nuovo modulo `llm_routes.py`:

#### Opzione Scelta: LM Studio con LLaMA Locale

**Vantaggi**:
- ✅ **Privacy**: Nessun dato inviato a servizi esterni
- ✅ **Costi**: Nessun costo API ricorrente
- ✅ **Controllo**: Modello locale configurabile
- ✅ **Offline**: Funziona senza connessione internet
- ✅ **OpenAI-compatible API**: Riutilizzo codice esistente

**Setup**:
1. **LM Studio** installato localmente
2. **Modello suggerito**: LLaMA 3.1 8B Instruct
3. **Server locale**: `http://localhost:1234/v1`
4. **Configurazione**: 4-8 GB VRAM, context window 4096+ tokens

#### Alternative Considerate

| Opzione | Pro | Contro | Scelta |
|---------|-----|--------|--------|
| **LM Studio + LLaMA** | Privacy, no costi, offline | Setup iniziale, richiede GPU | ✅ **Scelta** |
| OpenAI GPT-4 | Qualità alta, zero setup | Costi API, privacy concerns | ❌ |
| Azure OpenAI | Integrazione enterprise | Costi, complessità setup | ❌ |
| Ollama | Leggero, CLI-friendly | Meno UI-friendly di LM Studio | ⚠️ Alternativa |

### 3.2 Architettura Componenti

```
web_gui/
├── services/
│   ├── analysis_service.py         # [ESISTENTE]
│   ├── file_service.py             # [ESISTENTE]
│   ├── analytics_service.py        # [ESISTENTE]
│   ├── llm_service.py              # [NUOVO] Gestione LLM
│   └── context_builder_service.py  # [NUOVO] Estrazione contesto progetto
├── routes/
│   ├── analysis_routes.py          # [ESISTENTE]
│   ├── results_routes.py           # [ESISTENTE]
│   ├── analytics_routes.py         # [ESISTENTE]
│   └── llm_routes.py               # [NUOVO] Endpoint conversazione LLM
├── modules/                        # [NUOVO] Package riutilizzabile
│   ├── __init__.py
│   ├── textGenerationManager.py    # [IMPORT] Classe base astratta
│   └── lmstudio_manager.py         # [NUOVO] Adapter per LM Studio
├── prompts/                        # [NUOVO] System prompts
│   ├── mark_expert_prompt.txt      # Prompt metodologia MARK
│   └── classification_explainer_prompt.txt
├── templates/
│   ├── index.html                  # [MODIFICA] Aggiungere tab LLM
│   └── components/
│       └── llm_assistant.html      # [NUOVO] Componente chat
└── static/
    └── js/
        └── llm_chat.js             # [NUOVO] Frontend chat LLM
```

---

## 4. Analisi di Impatto Dettagliata

### 4.1 Nuovi File da Creare

#### Backend - Moduli Base (Riutilizzo codice esistente)
```
MARK-Tool/MARK-Tool/web_gui/modules/
├── __init__.py                     # [NUOVO]
├── textGenerationManager.py        # [COPIA] Da Smart_Student_Server
```

**Modifiche necessarie a file copiati**:
- ✅ Nessuna modifica a `textGenerationManager.py` (classe base astratta)

#### Backend - Adapter LM Studio
```
MARK-Tool/MARK-Tool/web_gui/modules/lmstudio_manager.py  # [NUOVO]
```

**Responsabilità**:
- Estende `TextGenerationManager`
- Connessione a LM Studio via OpenAI-compatible API
- Gestione errori connessione locale
- Configurazione endpoint personalizzato

**Codice schema**:
```python
from modules.textGenerationManager import TextGenerationManager
import openai

class LMStudioManager(TextGenerationManager):
    """
    Manager for LM Studio local LLM with OpenAI-compatible API
    """
    
    MODELS = [
        "local-model",  # Nome generico per modello LM Studio
    ]
    
    def __init__(self, base_url="http://localhost:1234/v1", 
                 model="local-model", starting_prompt=""):
        
        super().__init__(None, model, starting_prompt)
        
        # Configure OpenAI client for local endpoint
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key="not-needed"  # LM Studio non richiede API key
        )
    
    def api_call(self, messages):
        """Make API call to LM Studio"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LM Studio: {str(e)}"
    
    def generate_response_history(self, message):
        """Generate with conversation history"""
        self.messages.append({"role": "user", "content": message})
        response = self.api_call(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def generate_response(self, message, starting_prompt=""):
        """Generate without history"""
        if starting_prompt:
            msgs = [
                {"role": "system", "content": starting_prompt},
                {"role": "user", "content": message}
            ]
        else:
            msgs = [
                {"role": "system", "content": self.starting_prompt},
                {"role": "user", "content": message}
            ]
        return self.api_call(msgs)
```

#### Backend - LLM Service
```
MARK-Tool/MARK-Tool/web_gui/services/llm_service.py  # [NUOVO]
```

**Responsabilità**:
1. Inizializzazione LLM manager (LM Studio o OpenAI)
2. Caricamento system prompts da file
3. Costruzione contesto analisi da risultati MARK
4. Gestione conversazioni con history
5. Generazione spiegazioni automatiche
6. Cache risposte comuni per performance

**Dipendenze**:
- `modules.lmstudio_manager.LMStudioManager`
- `services.context_builder_service.ContextBuilderService`
- Risultati analisi (CSV Producer/Consumer)

**Metodi principali**:
```python
class LLMService:
    def __init__(self, llm_type='lmstudio', **config)
    def load_system_prompt(self, prompt_file: str) -> str
    def explain_classification(self, job_id: str) -> str
    def ask_question(self, question: str, job_id: str, history: list) -> tuple
    def get_project_summary(self, job_id: str) -> str
    def suggest_improvements(self, job_id: str) -> list
    def _build_analysis_context(self, results: dict) -> str
```

#### Backend - Context Builder Service
```
MARK-Tool/MARK-Tool/web_gui/services/context_builder_service.py  # [NUOVO]
```

**Responsabilità**:
1. Estrazione README da progetto analizzato
2. Parsing requirements.txt / pyproject.toml / setup.py
3. Aggregazione risultati CSV (count libraries, keywords, files)
4. Estrazione snippet codice rilevanti (prime righe file con keywords)
5. Costruzione contesto formattato per LLM

**Metodi principali**:
```python
class ContextBuilderService:
    @staticmethod
    def extract_readme(project_path: str) -> str
    @staticmethod
    def extract_dependencies(project_path: str) -> dict
    @staticmethod
    def aggregate_analysis_results(producer_csv: str, consumer_csv: str) -> dict
    @staticmethod
    def extract_code_snippets(files: list, max_snippets: int = 3) -> list
    @staticmethod
    def build_full_context(job_id: str, analysis_service: AnalysisService) -> dict
```

#### Backend - LLM Routes
```
MARK-Tool/MARK-Tool/web_gui/routes/llm_routes.py  # [NUOVO]
```

**Endpoint proposti**:

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/llm/explain/<job_id>` | GET | Spiegazione automatica classificazione |
| `/api/llm/ask` | POST | Interrogazione conversazionale |
| `/api/llm/summary/<job_id>` | GET | Sommario progetto analizzato |
| `/api/llm/history/<session_id>` | GET | Recupera history conversazione |
| `/api/llm/clear/<session_id>` | DELETE | Cancella history conversazione |

**Esempio endpoint `/api/llm/ask`**:
```python
@llm_bp.route('/ask', methods=['POST'])
def ask_llm():
    """
    Interrogazione conversazionale LLM
    
    Body JSON:
    {
        "job_id": "uuid-string",
        "question": "Why is this a Producer?",
        "session_id": "optional-session-id",
        "history": [...]  # optional conversation history
    }
    
    Response:
    {
        "answer": "This project is classified as...",
        "session_id": "uuid",
        "timestamp": "2025-12-05T10:30:00"
    }
    """
    data = request.json
    job_id = data.get('job_id')
    question = data.get('question')
    session_id = data.get('session_id', str(uuid.uuid4()))
    history = data.get('history', [])
    
    # Validate job exists
    job = analysis_service.get_job(job_id)
    if not job or job.status != 'completed':
        return jsonify({'error': 'Job not found or not completed'}), 404
    
    # Get LLM response
    answer, updated_history = llm_service.ask_question(
        question, job_id, history
    )
    
    return jsonify({
        'answer': answer,
        'session_id': session_id,
        'history': updated_history,
        'timestamp': datetime.now().isoformat()
    })
```

#### System Prompts
```
MARK-Tool/MARK-Tool/web_gui/prompts/
├── mark_expert_prompt.txt           # [NUOVO]
└── classification_explainer_prompt.txt  # [NUOVO]
```

**`mark_expert_prompt.txt`** (System prompt principale):
```
You are an expert ML project analyst specializing in the MARK tool methodology.

## MARK Classification System

MARK analyzes Python ML projects using static code analysis to classify them into:

### 1. ML-MODEL PRODUCERS
Projects that CREATE, TRAIN, or FINE-TUNE machine learning models.

**Detection Method:**
- Scans for TRAINING-related API calls in Python files
- Uses Knowledge Base of ~56 training keywords from popular ML libraries

**Examples:**
- TensorFlow/Keras: .fit(), .train_on_batch(), .fit_generator()
- PyTorch: .backward(), optimizer.step(), loss.backward()
- Scikit-learn: .fit()
- XGBoost/LightGBM: .train(), .cv()
- FastAI: .fine_tune(), .fit_one_cycle()

**Logic:** If ANY file contains training keywords → Producer

### 2. ML-MODEL CONSUMERS
Projects that USE pre-trained models for predictions/inference.

**Detection Method:**
- Scans for INFERENCE-related API calls
- Uses separate Consumer Knowledge Base (~34 keywords)

**Examples:**
- Keras/TensorFlow: .predict(), .predict_on_batch()
- PyTorch: torch.no_grad(), model.eval()
- Scikit-learn: .predict(), .predict_proba()
- Model loading: pretrained=True, torch.load()

**Logic with Exclusion Rule:**
1. File has consumer keywords AND producer keywords → NOT pure Consumer
2. File has consumer keywords BUT NO producer keywords → Consumer

### 3. HYBRID (Producer & Consumer)
Projects with BOTH training and inference code.

## Knowledge Base Structure

**Libraries Covered:**
- Deep Learning: TensorFlow, Keras, PyTorch, MXNet, Chainer, Lightning
- Classical ML: Scikit-learn, XGBoost, LightGBM
- Frameworks: FastAI, H2O

**KB Format:**
- library, Keyword, ML_Category, Link (to documentation)
- Each keyword linked to specific API documentation

## Analysis Output

Results provided as CSV with columns:
- ProjectName: Repository analyzed
- Is ML producer/consumer: Yes/No
- libraries: Detected framework (e.g., 'tensorflow', 'sklearn')
- where: Absolute file path with match
- keywords: Specific API call found (e.g., '.fit(', '.predict(')
- line_number: Exact line in source code

## Your Role

When answering user questions:

1. **Explain Classifications**: Use detected keywords to explain WHY a project was classified
2. **Contextualize APIs**: Explain what detected APIs do (training vs inference)
3. **Infer Application Domain**: Based on project structure, README, dependencies
4. **Be Technical Yet Accessible**: Balance accuracy with clarity
5. **Ground in Evidence**: Always reference specific keywords/files from analysis results
6. **Admit Limitations**: If README/docs are missing, state uncertainty about domain

**Tone**: Professional, helpful, educational. Assume user has basic ML knowledge but may not understand MARK methodology.

**Language**: Always respond in Italian unless explicitly asked otherwise.
```

#### Frontend - Componente Chat
```
MARK-Tool/MARK-Tool/web_gui/templates/components/llm_assistant.html  # [NUOVO]
MARK-Tool/MARK-Tool/web_gui/static/js/llm_chat.js  # [NUOVO]
MARK-Tool/MARK-Tool/web_gui/static/css/llm_chat.css  # [NUOVO]
```

**Funzionalità UI**:
- Tab dedicato "Assistente LLM" nella GUI principale
- Sezione "Spiegazione Automatica" (generata al completamento job)
- Chat interattiva con input testuale e cronologia messaggi
- Indicatori di caricamento durante elaborazione LLM
- Pulsante "Cancella Conversazione"
- Visualizzazione timestamp messaggi
- Supporto markdown nelle risposte LLM

### 4.2 File da Modificare

#### `web_gui/app.py`
**Modifiche**:
```python
# Aggiungere import
from .services.llm_service import LLMService
from .services.context_builder_service import ContextBuilderService
from .routes import llm_routes

def create_app(config_name=None):
    # ... existing code ...
    
    # Initialize LLM service [NUOVO]
    llm_service = LLMService(
        llm_type=app.config['LLM_TYPE'],
        base_url=app.config['LLM_BASE_URL'],
        model=app.config['LLM_MODEL']
    )
    app.llm_service = llm_service
    
    # Register blueprints [ESISTENTE + NUOVO]
    app.register_blueprint(analysis_routes.analysis_bp)
    app.register_blueprint(file_routes.file_bp)
    app.register_blueprint(results_routes.results_bp)
    app.register_blueprint(analytics_routes.analytics_bp)
    app.register_blueprint(llm_routes.llm_bp)  # [NUOVO]
```

**Impatto**: Basso - Aggiunta di inizializzazione servizio e registrazione blueprint

#### `web_gui/config.py`
**Modifiche**:
```python
class Config:
    # ... existing config ...
    
    # LLM Configuration [NUOVO]
    LLM_TYPE = os.environ.get('LLM_TYPE', 'lmstudio')  # 'lmstudio' or 'openai'
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'http://localhost:1234/v1')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'local-model')
    LLM_API_KEY = os.environ.get('LLM_API_KEY', 'not-needed')
    LLM_MAX_TOKENS = int(os.environ.get('LLM_MAX_TOKENS', '2000'))
    LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', '0.3'))
    
    # Prompts paths [NUOVO]
    PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
    MARK_EXPERT_PROMPT = os.path.join(PROMPTS_DIR, 'mark_expert_prompt.txt')
```

**Impatto**: Basso - Aggiunta configurazioni, nessuna modifica a esistenti

#### `web_gui/requirements.txt`
**Modifiche**:
```txt
# Existing dependencies
Flask==3.0.0
Werkzeug==3.0.1
Flask-CORS==4.0.0

# LLM Integration [NUOVO]
pandas==2.0.3        # Già usato in Categorizer, esplicitare
```

**Impatto**: Basso - Aggiunta dipendenze minimali

#### `web_gui/templates/index.html`
**Modifiche**:
- Aggiungere tab "Assistente LLM" al menu principale
- Includere componente `llm_assistant.html`
- Aggiungere link a `llm_chat.js` e `llm_chat.css`

**Codice da aggiungere**:
```html
<!-- Aggiungere nel menu tab -->
<li class="nav-item">
    <a class="nav-link" id="llm-tab" data-bs-toggle="tab" href="#llm">
        <i class="fas fa-robot"></i> Assistente LLM
    </a>
</li>

<!-- Aggiungere nel contenuto tab -->
<div class="tab-pane fade" id="llm" role="tabpanel">
    {% include 'components/llm_assistant.html' %}
</div>

<!-- Aggiungere prima di </body> -->
<script src="{{ url_for('static', filename='js/llm_chat.js') }}"></script>
```

**Impatto**: Basso-Medio - Aggiunta UI, nessuna modifica a funzionalità esistenti

#### `web_gui/services/analysis_service.py`
**Modifiche opzionali**:
- Aggiungere callback al completamento job per trigger spiegazione LLM automatica
- Metodo helper per recuperare percorsi risultati job

```python
class AnalysisJob:
    def __init__(self, ...):
        # ... existing ...
        self.llm_explanation = None  # [NUOVO] Cache spiegazione LLM
        self.context_extracted = False  # [NUOVO] Flag contesto estratto

class AnalysisService:
    def _job_completed(self, job_id: str):
        """
        Called when job completes successfully
        """
        job = self.get_job(job_id)
        # ... existing completion logic ...
        
        # [NUOVO] Trigger LLM explanation if available
        if hasattr(self, 'llm_service'):
            try:
                explanation = self.llm_service.explain_classification(job_id)
                job.llm_explanation = explanation
            except Exception as e:
                logging.warning(f"Failed to generate LLM explanation: {e}")
```

**Impatto**: Basso - Modifiche opzionali, retrocompatibili

### 4.3 File Non Modificati (Nessun Impatto)

I seguenti moduli rimangono completamente invariati:

✅ **Core Analysis Logic**:
- `Categorizer/src/exec_analysis.py`
- `Categorizer/src/producer_classifier_by_dict.py`
- `Categorizer/src/consumer_classifier_by_dict.py`
- `Categorizer/src/analyzer_base.py`
- `Categorizer/src/components/static_analysis/library_extractor.py`

✅ **Knowledge Base**:
- `Categorizer/src/library_dictionary/*.csv`

✅ **Existing Services** (se non si aggiunge integrazione opzionale):
- `web_gui/services/file_service.py`
- `web_gui/services/analytics_service.py`

✅ **Existing Routes**:
- `web_gui/routes/analysis_routes.py`
- `web_gui/routes/file_routes.py`
- `web_gui/routes/results_routes.py`
- `web_gui/routes/analytics_routes.py`

---

## 5. Requisiti Tecnici e Dipendenze

### 5.1 Setup LM Studio

**Prerequisiti**:
1. **Hardware**:
   - CPU: Moderno (Intel i5/AMD Ryzen 5 o superiore)
   - RAM: 8 GB minimo (16 GB raccomandato)
   - GPU: NVIDIA con 6-8 GB VRAM (opzionale ma fortemente raccomandato)
   - Storage: 10 GB per modello LLaMA 8B

2. **Software**:
   - LM Studio versione 0.2.9+
   - CUDA Toolkit 11.8+ (se GPU NVIDIA)

**Installazione**:
1. Download LM Studio: https://lmstudio.ai/
2. Installare e avviare LM Studio
3. Scaricare modello tramite UI:
   - Cercare "LLaMA 3.1 8B Instruct"
   - Download modello quantizzato Q4 (bilancio qualità/performance)
4. Avviare server locale:
   - Tab "Local Server" → Start Server
   - Default endpoint: `http://localhost:1234/v1`
   - Verificare compatibilità OpenAI API

**Configurazione Modello**:
```json
{
  "temperature": 0.3,
  "max_tokens": 2000,
  "top_p": 0.9,
  "context_length": 4096,
  "gpu_layers": 35
}
```

### 5.2 Dipendenze Python

**Nuove dipendenze**:
```
pandas>=2.0.3        # Parsing CSV risultati (già usato)
```

**Dipendenze esistenti** (nessuna modifica):
```
Flask==3.0.0
Werkzeug==3.0.1
Flask-CORS==4.0.0
```

### 5.3 Variabili d'Ambiente

**Nuovo file**: `.env` (development) o configurazione sistema (production)

```bash
# LLM Configuration
LLM_TYPE=lmstudio
LLM_BASE_URL=http://localhost:1234/v1
LLM_MODEL=local-model          # Nome modello in LM Studio
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.3

# Flask Config (esistenti)
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

### 5.4 Compatibilità

**Python**: 3.8+ (già in uso)  
**Flask**: 3.0+ (già in uso)  
**Browser**: Chrome 90+, Firefox 88+, Safari 14+ (per frontend chat)  
**OS**: Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)

---

## 6. Piano di Implementazione

### 6.1 Fase 1: Setup Infrastruttura LLM (3-4 giorni)

**Task**:
1. ✅ Installazione e configurazione LM Studio
2. ✅ Download e test modello LLaMA/Mistral
3. ✅ Verifica connettività API locale
4. ✅ Creazione moduli base (`modules/`)
5. ✅ Copia e adattamento `textGenerationManager.py`
6. ✅ Implementazione `lmstudio_manager.py`
7. ✅ Test unitari manager LM Studio

**Deliverable**: Manager LLM funzionante e testato

**Rischi**:
- ⚠️ Problemi CUDA/GPU: Fallback a CPU (più lento)
- ⚠️ Modello troppo grande: Usare versione quantizzata Q4 o modello più piccolo

### 6.2 Fase 2: Backend LLM Services (4-5 giorni)

**Task**:
1. ✅ Creazione `prompts/mark_expert_prompt.txt`
2. ✅ Implementazione `ContextBuilderService`
   - Metodi estrazione README/requirements
   - Aggregazione risultati CSV
3. ✅ Implementazione `LLMService`
   - Inizializzazione manager
   - Metodo `explain_classification()`
   - Metodo `ask_question()` con history
   - Cache risposte comuni
4. ✅ Implementazione `llm_routes.py`
   - Endpoint `/api/llm/explain/<job_id>`
   - Endpoint `/api/llm/ask`
   - Endpoint `/api/llm/summary/<job_id>`
5. ✅ Integrazione in `app.py` e `config.py`
6. ✅ Test API con Postman/curl

**Deliverable**: API LLM funzionanti e documentate

**Rischi**:
- ⚠️ Context troppo grande: Implementare chunking/summarization
- ⚠️ Risposte LLM lente: Ottimizzare prompt, ridurre max_tokens

### 6.3 Fase 3: Frontend UI Chat (3-4 giorni)

**Task**:
1. ✅ Design UI componente chat (mockup/wireframe)
2. ✅ Implementazione `llm_assistant.html`
   - Sezione spiegazione automatica
   - Area chat con cronologia
   - Input utente e pulsante invio
3. ✅ Implementazione `llm_chat.js`
   - Fetch API per chiamate backend
   - Gestione history locale
   - Rendering messaggi con markdown
   - Loading states
4. ✅ Styling `llm_chat.css`
   - Bubbles messaggi (user vs assistant)
   - Responsive design
   - Animazioni smooth
5. ✅ Integrazione in `index.html` (nuovo tab)
6. ✅ Test cross-browser

**Deliverable**: UI chat funzionale e user-friendly

**Rischi**:
- ⚠️ UX confusa: Iterare con user testing
- ⚠️ Performance frontend: Debounce input, lazy load history

### 6.4 Fase 4: Testing e Ottimizzazione (3-4 giorni)

**Task**:
1. ✅ Test end-to-end workflow completo
   - Analisi progetto → Spiegazione automatica → Chat
2. ✅ Test con progetti reali (sample dal dataset)
3. ✅ Tuning system prompt (qualità risposte)
4. ✅ Ottimizzazione performance
   - Cache risposte comuni
   - Riduzione token context
5. ✅ Error handling robusto
   - LM Studio offline → Messaggio user-friendly
   - Timeout richieste lunghe
6. ✅ Documentazione utente (README sezione LLM)

**Deliverable**: Sistema stabile e ottimizzato

**Test Cases**:
| Scenario | Input | Output Atteso |
|----------|-------|---------------|
| Spiegazione Producer | Job con .fit() | "Progetto Producer perché trovato .fit() in train.py..." |
| Spiegazione Consumer | Job con .predict() | "Progetto Consumer perché usa solo inferenza..." |
| Domanda dominio | "Qual è il dominio?" | Risposta basata su README/dependencies |
| LM Studio offline | Qualsiasi query | "Errore: LLM non disponibile" |
| Context troppo grande | Progetto enorme | Summarization automatica |

### 6.5 Fase 5: Documentazione e Deployment (2-3 giorni)

**Task**:
1. ✅ Aggiornamento README principale con sezione LLM
2. ✅ Guida setup LM Studio per utenti finali
3. ✅ Documentazione API (`/api/llm/*` endpoints)
4. ✅ Video demo (opzionale)
5. ✅ Update requirements.txt e .env.example
6. ✅ Test deployment su ambiente staging

**Deliverable**: Sistema pronto per produzione
