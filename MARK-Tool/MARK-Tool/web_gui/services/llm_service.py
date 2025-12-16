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

from modules.lmstudio_manager import LMStudioManager
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
        llm_type: str = 'lmstudio',
        base_url: str = 'http://localhost:1234/v1',
        model: str = 'local-model',
        temperature: float = 0.3,
        max_tokens: int = 2000,
        prompts_dir: Optional[str] = None
    ):
        """
        Initialize LLM service.
        
        Args:
            llm_type: Type of LLM provider ('lmstudio')
            base_url: LM Studio server endpoint
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            prompts_dir: Directory containing prompt files
        """
        self.llm_type = llm_type
        self.prompts_dir = prompts_dir or os.path.join(
            Path(__file__).parent.parent, 'prompts'
        )
        
        # Load system prompts
        self.mark_expert_prompt = self.load_system_prompt('mark_expert_prompt.txt')
        self.classification_explainer_prompt = self.load_system_prompt('classification_explainer_prompt.txt')
        
        # Initialize LLM manager
        try:
            if llm_type == 'lmstudio':
                self.llm_manager = LMStudioManager(
                    base_url=base_url,
                    model=model,
                    starting_prompt=self.mark_expert_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                logger.info(f"LLM Service initialized with LM Studio: {base_url}")
            else:
                raise ValueError(f"Unsupported LLM type: {llm_type}")
            
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
        Generate automatic explanation for project classification.
        
        Args:
            input_path: Path to analyzed project
            output_path: Path to analysis results
            project_name: Optional project name
            
        Returns:
            Explanation text
        """
        if not self.llm_manager:
            return "Servizio LLM non disponibile. Verificare che LM Studio sia in esecuzione."
        
        try:
            # Build context
            context = ContextBuilderService.build_full_context(
                input_path, output_path, project_name
            )
            
            # Format context for LLM
            context_text = ContextBuilderService.format_context_for_llm(context)
            
            # Check cache
            cache_key = f"explain_{context['project_name']}_{context['analysis_results']['classification']}"
            if cache_key in self.cache:
                logger.info(f"Using cached explanation for {context['project_name']}")
                return self.cache[cache_key]
            
            # Generate explanation
            prompt = f"""Analizza i risultati MARK per questo progetto e fornisci una spiegazione chiara della classificazione.

{context_text}

Fornisci una spiegazione strutturata che includa:
1. Classificazione e sua motivazione
2. Evidenze specifiche (keywords, file, righe)
3. Librerie ML utilizzate e loro scopo
4. Possibile dominio applicativo (se inferibile)
5. Livello di confidenza nella classificazione
"""
            
            explanation = self.llm_manager.generate_response(
                prompt,
                starting_prompt=self.classification_explainer_prompt
            )
            
            # Cache result
            self.cache[cache_key] = explanation
            
            logger.info(f"Generated explanation for {context['project_name']}")
            return explanation
        
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
        Answer user question about analyzed project.
        
        Args:
            question: User's question
            input_path: Path to analyzed project
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
            else:
                session_id = str(uuid.uuid4())
                # Build context for new session
                context = ContextBuilderService.build_full_context(input_path, output_path)
                context_text = ContextBuilderService.format_context_for_llm(context)
                
                session = {
                    'session_id': session_id,
                    'created_at': datetime.now(),
                    'context': context,
                    'context_text': context_text,
                    'history': history or []
                }
                self.sessions[session_id] = session
            
            # Prepare message with context
            if not session['history']:
                # First message - include full context
                full_question = f"""Contesto del progetto analizzato:

{session['context_text']}

Domanda dell'utente: {question}
"""
            else:
                # Follow-up question - context already provided
                full_question = question
            
            # Generate response with history
            # Create a temporary manager with session history
            temp_manager = LMStudioManager(
                base_url=self.llm_manager.base_url,
                model=self.llm_manager.model,
                starting_prompt=self.mark_expert_prompt,
                temperature=self.llm_manager.temperature,
                max_tokens=self.llm_manager.max_tokens
            )
            
            # Load history into manager
            if session['history']:
                temp_manager.messages = [
                    {"role": "system", "content": self.mark_expert_prompt}
                ] + session['history']
            
            # Generate response
            answer = temp_manager.generate_response_history(full_question)
            
            # Update session history
            session['history'].append({"role": "user", "content": question})
            session['history'].append({"role": "assistant", "content": answer})
            
            logger.info(f"Answered question in session {session_id}")
            
            return answer, session_id, session['history']
        
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
        Generate a concise summary of the analyzed project.
        
        Args:
            input_path: Path to analyzed project
            output_path: Path to analysis results
            project_name: Optional project name
            
        Returns:
            Summary text
        """
        if not self.llm_manager:
            return "Servizio LLM non disponibile."
        
        try:
            context = ContextBuilderService.build_full_context(
                input_path, output_path, project_name
            )
            context_text = ContextBuilderService.format_context_for_llm(context)
            
            prompt = f"""Fornisci un sommario conciso (3-5 punti chiave) di questo progetto ML:

{context_text}

Includi: classificazione, librerie principali, possibile dominio applicativo.
"""
            
            summary = self.llm_manager.generate_response(prompt)
            
            logger.info(f"Generated summary for {context.get('project_name')}")
            return summary
        
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
                'project_name': session['context']['project_name'],
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
            'llm_type': self.llm_type,
            'available': self.is_available(),
            'active_sessions': len(self.sessions),
            'cache_size': len(self.cache)
        }
        
        if self.llm_manager:
            status['model_info'] = self.llm_manager.get_model_info()
        
        return status
