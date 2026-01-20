"""
LLM Service - Manages LLM interactions and conversation history

This service handles:
- LLM manager initialization (LM Studio)
- Loading and caching system prompts
- Building context from analysis results
- Managing conversation history
- Generating explanations and answering questions
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import uuid
from datetime import datetime

from modules.llm_factory import LLMFactory, LLMConfig
from services.context_builder_service import ContextBuilderService


logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for managing LLM interactions in MARK analysis context.
    
    Handles conversation sessions, context building, and response generation
    for explaining ML project classifications.
    """
    
    def __init__(
        self,
        config: LLMConfig,
        prompts_dir: Optional[str] = None
    ):
        """
        Initialize LLM service.
        
        Args:
            config: LLMConfig instance with provider settings
            prompts_dir: Directory containing prompt files
        """
        self.config = config
        self.prompts_dir = prompts_dir or os.path.join(
            Path(__file__).parent.parent, 'prompts'
        )
        
        # Load system prompts
        self.mark_expert_prompt = self.load_system_prompt('mark_expert_prompt.txt')
        self.classification_explainer_prompt = self.load_system_prompt('classification_explainer_prompt.txt')
        
        # Set starting prompt in config if not already set
        if not config.starting_prompt:
            config.starting_prompt = self.mark_expert_prompt
        
        # Initialize LLM manager using factory pattern
        try:
            self.llm_manager = LLMFactory.create_manager(config)
            logger.info(
                f"LLM Service initialized with {config.llm_type}: "
                f"model={config.model}, temperature={config.temperature}"
            )
            
            # Test connection
            if not self.llm_manager.test_connection():
                logger.warning("LLM connection test failed - service may not be available")
        
        except Exception as e:
            logger.error(f"Failed to initialize LLM manager: {e}")
            self.llm_manager = None
        
        # Conversation sessions storage
        self.sessions: Dict[str, Dict] = {}
        
        # Response cache for common queries
        self.cache: Dict[str, str] = {}
    
    def load_system_prompt(self, prompt_file: str) -> str:
        """
        Load system prompt from file.
        
        Args:
            prompt_file: Filename of prompt in prompts directory
            
        Returns:
            Prompt content or default prompt if file not found
        """
        try:
            prompt_path = os.path.join(self.prompts_dir, prompt_file)
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Loaded prompt: {prompt_file}")
                return content
        except Exception as e:
            logger.error(f"Error loading prompt {prompt_file}: {e}")
            return "You are a helpful ML project analysis assistant."
    
    def is_available(self) -> bool:
        """
        Check if LLM service is available.
        
        Returns:
            True if LLM manager is initialized and connected
        """
        return self.llm_manager is not None and self.llm_manager.test_connection()
    
    def explain_classification(
        self,
        input_path: str,
        output_path: str,
        project_name: Optional[str] = None
    ) -> str:
        """
        Generate automatic explanation for projects classification.
        
        Args:
            input_path: Path to analyzed projects directory
            output_path: Path to analysis results
            project_name: Optional project name (for filtering)
            
        Returns:
            Explanation text
        """
        if not self.llm_manager:
            return "Servizio LLM non disponibile. Verificare che LM Studio sia in esecuzione."
        
        try:
            # Build context - this will throw ValueError if no data found
            context = ContextBuilderService.build_full_context(
                output_path, input_path
            )
            
            # Format context for LLM
            context_text = ContextBuilderService.format_context_for_llm(context)
            
            # Check cache
            cache_key = f"explain_{context['total_projects']}_{context['producer_count']}_{context['consumer_count']}"
            if cache_key in self.cache:
                logger.info(f"Using cached explanation for analysis")
                return self.cache[cache_key]
            
            # Build enhanced prompt with context embedded
            system_prompt_with_context = f"""{self.classification_explainer_prompt}

## CURRENT ANALYSIS CONTEXT

{context_text}

---
Remember: Use EXACT project names from the context above!
"""
            
            # Generate explanation
            prompt = f"""Analizza i risultati MARK e fornisci una spiegazione chiara delle classificazioni.

Fornisci una spiegazione strutturata che includa:
1. Panoramica generale (numero di progetti, distribuzione delle classificazioni)
2. Per ciascun progetto: classificazione e motivazione
3. Evidenze specifiche (keywords, file, librerie)
4. Possibili domini applicativi (se inferibili)
5. Livello di confidenza nelle classificazioni

Rispondi in italiano.
"""
            
            explanation = self.llm_manager.generate_response(
                prompt,
                starting_prompt=system_prompt_with_context
            )
            
            # Cache result
            self.cache[cache_key] = explanation
            
            logger.info(f"Generated explanation for {context['total_projects']} projects")
            return explanation
        
        except ValueError as e:
            # Validation error - no data found
            logger.error(f"Validation error: {e}")
            return str(e)
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Errore nella generazione della spiegazione: {str(e)}"
    
    def ask_question(
        self,
        question: str,
        input_path: str,
        output_path: str,
        session_id: Optional[str] = None,
        history: Optional[List[Dict]] = None
    ) -> Tuple[str, str, List[Dict]]:
        """
        Answer user question about analyzed projects.
        
        Args:
            question: User's question
            input_path: Path to analyzed projects directory
            output_path: Path to analysis results
            session_id: Optional session ID for conversation continuity
            history: Optional conversation history
            
        Returns:
            Tuple of (answer, session_id, updated_history)
        """
        if not self.llm_manager:
            return (
                "Servizio LLM non disponibile. Verificare che LM Studio sia in esecuzione.",
                session_id or str(uuid.uuid4()),
                history or []
            )
        
        try:
            # Get or create session
            if session_id and session_id in self.sessions:
                session = self.sessions[session_id]
                logger.info(f"Using existing session {session_id}")
            else:
                session_id = str(uuid.uuid4())
                # Build context for new session - will throw ValueError if no data
                context = ContextBuilderService.build_full_context(output_path, input_path)
                context_text = ContextBuilderService.format_context_for_llm(context)
                
                session = {
                    'session_id': session_id,
                    'created_at': datetime.now(),
                    'context': context,
                    'context_text': context_text,
                    'history': history or []
                }
                self.sessions[session_id] = session
                logger.info(f"Created new session {session_id} with context for {context['total_projects']} projects")
            
            # Generate response with history
            # Create a temporary manager with session history using factory
            # This preserves conversation context while allowing per-session customization
            temp_config = LLMConfig(
                llm_type=self.config.llm_type,
                base_url=self.config.base_url,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
                api_key=self.config.api_key,
                starting_prompt=self.mark_expert_prompt
            )
            temp_manager = LLMFactory.create_manager(temp_config)
            
            # Build messages array with context included in system prompt
            # CRITICAL: Include analysis context in the system prompt so LLM always has it
            system_prompt_with_context = f"""{self.mark_expert_prompt}

## CURRENT ANALYSIS CONTEXT

{session['context_text']}

---
Remember: Use EXACT project names from the context above. Never use placeholders!
"""
            
            # Initialize messages with enhanced system prompt
            messages = [{"role": "system", "content": system_prompt_with_context}]
            
            # Add conversation history
            if session['history']:
                messages.extend(session['history'])
            
            temp_manager.messages = messages
            
            # Fix Issue 4: Include context reminder with the question to ensure LLM has fresh access to data
            # This prevents the LLM from "forgetting" the context in longer conversations
            question_with_context = f"{question}\n\n[Context Reminder: You have analysis data for {session['context']['total_projects']} projects. Refer to the CURRENT ANALYSIS CONTEXT in the system prompt.]"
            
            # Generate response with context-enhanced question
            answer = temp_manager.generate_response_history(question_with_context)
            
            # Update session history
            session['history'].append({"role": "user", "content": question})
            session['history'].append({"role": "assistant", "content": answer})
            
            logger.info(f"Answered question in session {session_id}")
            
            return answer, session_id, session['history']
        
        except ValueError as e:
            # Validation error - no data found
            logger.error(f"Validation error: {e}")
            return (
                str(e),
                session_id or str(uuid.uuid4()),
                history or []
            )
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return (
                f"Errore nell'elaborazione della domanda: {str(e)}",
                session_id or str(uuid.uuid4()),
                history or []
            )
    
    def get_project_summary(
        self,
        input_path: str,
        output_path: str,
        project_name: Optional[str] = None
    ) -> str:
        """
        Generate a concise summary of the analyzed projects.
        
        Args:
            input_path: Path to analyzed projects directory
            output_path: Path to analysis results
            project_name: Optional project name (for filtering)
            
        Returns:
            Summary text
        """
        if not self.llm_manager:
            return "Servizio LLM non disponibile."
        
        try:
            context = ContextBuilderService.build_full_context(
                output_path, input_path
            )
            context_text = ContextBuilderService.format_context_for_llm(context)
            
            # Build enhanced prompt with context embedded
            system_prompt_with_context = f"""{self.mark_expert_prompt}

## CURRENT ANALYSIS CONTEXT

{context_text}

---
Remember: Use EXACT project names from the context above!
"""
            
            prompt = f"""Fornisci un sommario conciso (3-5 punti chiave) dell'analisi MARK:

Includi: 
- Numero totale di progetti analizzati
- Distribuzione delle classificazioni (Producer/Consumer/Hybrid)
- Librerie ML principali rilevate
- Possibili domini applicativi

Rispondi in italiano in modo strutturato e conciso.
"""
            
            summary = self.llm_manager.generate_response(
                prompt,
                starting_prompt=system_prompt_with_context
            )
            
            logger.info(f"Generated summary for {context['total_projects']} projects")
            return summary
        
        except ValueError as e:
            # Validation error - no data found
            logger.error(f"Validation error: {e}")
            return str(e)
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Errore nella generazione del sommario: {str(e)}"
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get conversation session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session dictionary or None
        """
        return self.sessions.get(session_id)
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear conversation session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session was cleared, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session {session_id}")
            return True
        return False
    
    def get_all_sessions(self) -> List[Dict]:
        """
        Get all active sessions.
        
        Returns:
            List of session summaries
        """
        return [
            {
                'session_id': sid,
                'created_at': session['created_at'].isoformat(),
                'total_projects': session['context']['total_projects'],
                'message_count': len(session['history'])
            }
            for sid, session in self.sessions.items()
        ]
    
    def clear_cache(self):
        """Clear response cache."""
        self.cache.clear()
        logger.info("Cleared LLM response cache")
    
    def get_status(self) -> Dict:
        """
        Get service status.
        
        Returns:
            Dictionary with service status information
        """
        status = {
            'llm_type': self.config.llm_type,
            'model': self.config.model,
            'temperature': self.config.temperature,
            'max_tokens': self.config.max_tokens,
            'available': self.is_available(),
            'active_sessions': len(self.sessions),
            'cache_size': len(self.cache)
        }
        
        if self.llm_manager:
            status['model_info'] = self.llm_manager.get_model_info()
        
        return status
