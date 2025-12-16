"""
MARK Analysis Tool - Flask Application Entry Point
"""
import os
import sys
import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from config import get_config
from services.file_service import FileService
from services.analysis_service import AnalysisService
from services.analytics_service import AnalyticsService
from services.llm_service import LLMService
from routes import analysis_routes, file_routes, results_routes, analytics_routes, llm_routes


def create_app(config_name=None):
    """
    Create and configure the Flask application
    
    Args:
        config_name: Configuration environment name (development, production, testing)
        
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Setup logging
    setup_logging(app)
    
    # Enable CORS
    # TODO originale, vedere se lasciare qualunque origine
    #CORS(app, resources={
    #    r"/api/*": {
    #        "origins": app.config['CORS_ORIGINS']
    #    }
    #})
    # Accetta qualunque origine su tutti i path /api
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize services
    file_service = FileService(
        upload_folder=app.config['UPLOAD_FOLDER'],
        allowed_extensions=app.config['ALLOWED_EXTENSIONS']
    )
    
    analysis_service = AnalysisService(
        exec_analysis_path=app.config['EXEC_ANALYSIS_PATH'],
        cloner_path=app.config['CLONER_PATH']
    )
    
    analytics_service = AnalyticsService()
    
    # Initialize LLM service
    try:
        llm_service = LLMService(
            llm_type=app.config['LLM_TYPE'],
            base_url=app.config['LLM_BASE_URL'],
            model=app.config['LLM_MODEL'],
            temperature=app.config['LLM_TEMPERATURE'],
            max_tokens=app.config['LLM_MAX_TOKENS'],
            prompts_dir=app.config['PROMPTS_DIR']
        )
        app.logger.info('LLM Service initialized successfully')
    except Exception as e:
        app.logger.warning(f'LLM Service initialization failed: {e}')
        llm_service = None
    
    # Initialize routes with services
    analysis_routes.init_analysis_service(analysis_service)
    file_routes.init_file_service(file_service)
    results_routes.init_file_service(file_service)
    analytics_routes.init_analytics_service(analytics_service)
    llm_routes.init_llm_service(llm_service)
    llm_routes.init_analysis_service(analysis_service)
    
    # Register blueprints
    app.register_blueprint(analysis_routes.analysis_bp)
    app.register_blueprint(file_routes.file_bp)
    app.register_blueprint(results_routes.results_bp)
    app.register_blueprint(analytics_routes.analytics_bp)
    app.register_blueprint(llm_routes.llm_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register health check
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'MARK Analysis Tool API',
            'version': '1.0.0'
        }), 200
    
    # Register root endpoint
    @app.route('/')
    def index():
        """Root endpoint - serve the web application"""
        return render_template('index.html')
    
    # Register root endpoint
    @app.route('/endpoints')
    def endpoints():
        """Root endpoint - API information"""
        return jsonify({
            'service': 'MARK Analysis Tool API',
            'version': '1.0.0',
            'web_pages': {
                'home': '/'
            },
            'endpoints': {
                'health': '/health',
                'analysis': {
                    'start': 'POST /api/analysis/start',
                    'status': 'GET /api/analysis/status/<job_id>',
                    'jobs': 'GET /api/analysis/jobs',
                    'cancel': 'POST /api/analysis/cancel/<job_id>',
                    'logs': 'GET /api/analysis/logs/<job_id>'
                },
                'file': {
                    'upload': 'POST /api/file/upload',
                    'validate_input': 'POST /api/file/validate/input',
                    'validate_output': 'POST /api/file/validate/output',
                    'validate_csv': 'POST /api/file/validate/csv',
                    'download': 'GET /api/file/download',
                    'list': 'GET /api/file/list'
                },
                'results': {
                    'list': 'GET /api/results/list',
                    'view': 'GET /api/results/view',
                    'stats': 'GET /api/results/stats',
                    'search': 'POST /api/results/search'
                },
                'analytics': {
                    'summary': 'GET /api/analytics/summary',
                    'distribution': 'GET /api/analytics/consumer-producer-distribution',
                    'keywords': 'GET /api/analytics/keywords',
                    'libraries': 'GET /api/analytics/libraries',
                    'filter': 'GET /api/analytics/filter',
                    'health': 'GET /api/analytics/health'
                },
                'llm': {
                    'status': 'GET /api/llm/status',
                    'explain': 'POST /api/llm/explain',
                    'ask': 'POST /api/llm/ask',
                    'summary': 'POST /api/llm/summary',
                    'session': 'GET /api/llm/session/<session_id>',
                    'delete_session': 'DELETE /api/llm/session/<session_id>',
                    'sessions': 'GET /api/llm/sessions',
                    'clear_cache': 'POST /api/llm/cache/clear'
                }
            }
        }), 200
    
    app.logger.info(f'MARK Analysis Tool API initialized (environment: {config_name})')
    
    return app


def setup_logging(app):
    """Configure application logging"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    # File handler
    file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    # Add handlers
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f'Internal Server Error: {str(error)}')
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': 'The request could not be understood or was missing required parameters'
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors"""
        return jsonify({
            'success': False,
            'error': 'Method Not Allowed',
            'message': 'The HTTP method is not allowed for this endpoint'
        }), 405


def main():
    """Main entry point for running the Flask application"""
    # Get environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Get host and port from environment
    # TODO vedere se lo si vuole lasciare accessibile da altri dispositivi o no
    #host = os.environ.get('FLASK_HOST', '127.0.0.1')
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    # Run the app
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    main()
