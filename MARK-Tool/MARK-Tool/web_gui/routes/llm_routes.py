"""
LLM Routes - API endpoints for LLM interactions

Provides endpoints for:
- Automatic classification explanations
- Interactive Q&A about analyzed projects
- Project summaries
- Session management
"""

from flask import Blueprint, request, jsonify, current_app
from typing import Optional
import logging
import uuid
from datetime import datetime

from services.llm_service import LLMService
from services.analysis_service import AnalysisService


logger = logging.getLogger(__name__)

# Create blueprint
llm_bp = Blueprint('llm', __name__, url_prefix='/api/llm')

# Service instances (will be initialized in app.py)
llm_service: Optional[LLMService] = None
analysis_service: Optional[AnalysisService] = None


def init_llm_service(service: LLMService):
    """Initialize the LLM service"""
    global llm_service
    llm_service = service


def init_analysis_service(service: AnalysisService):
    """Initialize the analysis service"""
    global analysis_service
    analysis_service = service


@llm_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get LLM service status
    
    Response JSON:
    {
        "success": true,
        "status": {
            "available": true/false,
            "llm_type": "lmstudio",
            "model_info": {...},
            "active_sessions": 0,
            "cache_size": 0
        }
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        status = llm_service.get_status()
        
        return jsonify({
            'success': True,
            'status': status
        })
    
    except Exception as e:
        logger.error(f"Error getting LLM status: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/explain', methods=['POST'])
def explain_classification():
    """
    Generate automatic explanation for project classification
    
    Request JSON:
    {
        "input_path": "/path/to/project",
        "output_path": "/path/to/results",
        "project_name": "optional-name"
    }
    
    Response JSON:
    {
        "success": true,
        "explanation": "...",
        "timestamp": "2025-12-06T10:30:00"
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        if not llm_service.is_available():
            return jsonify({
                'success': False,
                'message': 'LLM service not available. Verificare che LM Studio sia in esecuzione.'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        input_path = data.get('input_path')
        output_path = data.get('output_path')
        project_name = data.get('project_name')
        
        if not input_path or not output_path:
            return jsonify({
                'success': False,
                'message': 'input_path and output_path are required'
            }), 400
        
        # Generate explanation
        explanation = llm_service.explain_classification(
            input_path, output_path, project_name
        )
        
        return jsonify({
            'success': True,
            'explanation': explanation,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Ask a question about an analyzed project
    
    Request JSON:
    {
        "input_path": "/path/to/project",
        "output_path": "/path/to/results",
        "question": "Why is this a Producer?",
        "session_id": "optional-uuid",
        "history": [] (optional conversation history)
    }
    
    Response JSON:
    {
        "success": true,
        "answer": "...",
        "session_id": "uuid",
        "history": [...],
        "timestamp": "2025-12-06T10:30:00"
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        if not llm_service.is_available():
            return jsonify({
                'success': False,
                'message': 'LLM service not available. Verificare che LM Studio sia in esecuzione.'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        input_path = data.get('input_path')
        output_path = data.get('output_path')
        question = data.get('question')
        session_id = data.get('session_id')
        history = data.get('history', [])
        
        if not input_path or not output_path or not question:
            return jsonify({
                'success': False,
                'message': 'input_path, output_path, and question are required'
            }), 400
        
        # Get answer
        answer, session_id, updated_history = llm_service.ask_question(
            question, input_path, output_path, session_id, history
        )
        
        return jsonify({
            'success': True,
            'answer': answer,
            'session_id': session_id,
            'history': updated_history,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/summary', methods=['POST'])
def get_project_summary():
    """
    Get a concise summary of an analyzed project
    
    Request JSON:
    {
        "input_path": "/path/to/project",
        "output_path": "/path/to/results",
        "project_name": "optional-name"
    }
    
    Response JSON:
    {
        "success": true,
        "summary": "...",
        "timestamp": "2025-12-06T10:30:00"
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        if not llm_service.is_available():
            return jsonify({
                'success': False,
                'message': 'LLM service not available'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        input_path = data.get('input_path')
        output_path = data.get('output_path')
        project_name = data.get('project_name')
        
        if not input_path or not output_path:
            return jsonify({
                'success': False,
                'message': 'input_path and output_path are required'
            }), 400
        
        # Generate summary
        summary = llm_service.get_project_summary(
            input_path, output_path, project_name
        )
        
        return jsonify({
            'success': True,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """
    Get conversation session details
    
    Response JSON:
    {
        "success": true,
        "session": {
            "session_id": "uuid",
            "created_at": "2025-12-06T10:00:00",
            "project_name": "...",
            "history": [...]
        }
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        session = llm_service.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session': {
                'session_id': session['session_id'],
                'created_at': session['created_at'].isoformat(),
                'project_name': session['context']['project_name'],
                'history': session['history']
            }
        })
    
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/session/<session_id>', methods=['DELETE'])
def clear_session(session_id: str):
    """
    Clear conversation session
    
    Response JSON:
    {
        "success": true,
        "message": "Session cleared"
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        success = llm_service.clear_session(session_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Session cleared'
        })
    
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/sessions', methods=['GET'])
def get_all_sessions():
    """
    Get all active sessions
    
    Response JSON:
    {
        "success": true,
        "sessions": [
            {
                "session_id": "uuid",
                "created_at": "2025-12-06T10:00:00",
                "project_name": "...",
                "message_count": 4
            }
        ]
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        sessions = llm_service.get_all_sessions()
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
    
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@llm_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """
    Clear response cache
    
    Response JSON:
    {
        "success": true,
        "message": "Cache cleared"
    }
    """
    try:
        if not llm_service:
            return jsonify({
                'success': False,
                'message': 'LLM service not initialized'
            }), 503
        
        llm_service.clear_cache()
        
        return jsonify({
            'success': True,
            'message': 'Cache cleared'
        })
    
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
