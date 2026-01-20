"""
Analysis Routes - API endpoints for analysis operations
"""
from flask import Blueprint, request, jsonify, current_app
from services.analysis_service import AnalysisService


# Create blueprint
analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

# Service instance (will be initialized in app.py)
analysis_service: AnalysisService = None


def init_analysis_service(service: AnalysisService):
    """Initialize the analysis service"""
    global analysis_service
    analysis_service = service


@analysis_bp.route('/start', methods=['POST'])
def start_analysis():
    """
    Start a new analysis job
    
    Request JSON:
    {
        "input_path": "/path/to/repos",
        "output_path": "/path/to/results",
        "github_csv": "/path/to/csv" (optional),
        "run_cloner": true/false (optional, default: false)
    }
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "job_id": "...",
        "job": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validate required fields
        input_path = data.get('input_path')
        output_path = data.get('output_path')
        
        if not input_path:
            return jsonify({
                'success': False,
                'message': 'input_path is required'
            }), 400
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path is required'
            }), 400
        
        # Optional fields
        github_csv = data.get('github_csv')
        run_cloner = data.get('run_cloner', False)
        
        # Create job
        job_id = analysis_service.create_job(input_path, output_path, github_csv)
        
        # Start job
        success, message = analysis_service.start_job(job_id, run_cloner)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            }), 500
        
        # Get job details
        job = analysis_service.get_job(job_id)
        
        return jsonify({
            'success': True,
            'message': 'Analysis job started successfully',
            'job_id': job_id,
            'job': job.to_dict() if job else None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error starting analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error starting analysis: {str(e)}'
        }), 500


@analysis_bp.route('/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """
    Get the status of an analysis job
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "job": {...}
    }
    """
    try:
        job = analysis_service.get_job(job_id)
        
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Job found',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting job status: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting job status: {str(e)}'
        }), 500


@analysis_bp.route('/jobs', methods=['GET'])
def list_jobs():
    """
    List all analysis jobs
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "jobs": [...]
    }
    """
    try:
        jobs = analysis_service.get_all_jobs()
        
        return jsonify({
            'success': True,
            'message': f'Found {len(jobs)} jobs',
            'jobs': jobs
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error listing jobs: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error listing jobs: {str(e)}'
        }), 500


@analysis_bp.route('/cancel/<job_id>', methods=['POST'])
def cancel_job(job_id):
    """
    Cancel a running analysis job
    
    Response JSON:
    {
        "success": true/false,
        "message": "..."
    }
    """
    try:
        success, message = analysis_service.cancel_job(job_id)
        
        status_code = 200 if success else 400
        
        return jsonify({
            'success': success,
            'message': message
        }), status_code
        
    except Exception as e:
        current_app.logger.error(f"Error cancelling job: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error cancelling job: {str(e)}'
        }), 500


@analysis_bp.route('/logs/<job_id>', methods=['GET'])
def get_job_logs(job_id):
    """
    Get the logs for an analysis job
    
    Query parameters:
    - limit: Number of log entries to return (default: 50)
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "logs": [...]
    }
    """
    try:
        job = analysis_service.get_job(job_id)
        
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
        
        # Get limit from query params
        limit = request.args.get('limit', 50, type=int)
        
        # Get last N log entries
        logs = job.output_log[-limit:] if job.output_log else []
        
        return jsonify({
            'success': True,
            'message': f'Retrieved {len(logs)} log entries',
            'logs': logs
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting job logs: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting job logs: {str(e)}'
        }), 500
