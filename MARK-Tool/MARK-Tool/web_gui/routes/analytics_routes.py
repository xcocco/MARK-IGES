"""
Analytics Routes - API endpoints for analytics and dashboard data
"""
from flask import Blueprint, request, jsonify, current_app
from ..services.analytics_service import AnalyticsService


# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# Service instance (will be initialized in app.py)
analytics_service: AnalyticsService = None


def init_analytics_service(service: AnalyticsService):
    """Initialize the analytics service"""
    global analytics_service
    analytics_service = service


@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get summary statistics for the analysis results
    
    Query parameters:
    - output_path: Path to the output folder containing results (required)
    
    Response JSON:
    {
        "success": true/false,
        "total_models": 120,
        "consumer_count": 70,
        "producer_count": 50,
        "total_projects": 25,
        "total_libraries": 8,
        "last_analysis_id": "2025-11-24T10:32:01",
        "output_path": "..."
    }
    """
    try:
        output_path = request.args.get('output_path')
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path parameter is required'
            }), 400
        
        # Validate output path
        is_valid, message = analytics_service.validate_output_path(output_path)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Get summary
        summary = analytics_service.get_summary(output_path)
        
        if not summary.get('success'):
            return jsonify(summary), 500
        
        return jsonify(summary), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting summary: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get summary'
        }), 500


@analytics_bp.route('/consumer-producer-distribution', methods=['GET'])
def get_consumer_producer_distribution():
    """
    Get the distribution of consumer and producer models
    
    Query parameters:
    - output_path: Path to the output folder containing results (required)
    
    Response JSON:
    {
        "success": true/false,
        "labels": ["Consumer", "Producer"],
        "counts": [70, 50],
        "percentages": [58.33, 41.67]
    }
    """
    try:
        output_path = request.args.get('output_path')
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path parameter is required'
            }), 400
        
        # Validate output path
        is_valid, message = analytics_service.validate_output_path(output_path)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Get distribution
        distribution = analytics_service.get_consumer_producer_distribution(output_path)
        
        if not distribution.get('success'):
            return jsonify(distribution), 500
        
        return jsonify(distribution), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting distribution: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get distribution'
        }), 500


@analytics_bp.route('/keywords', methods=['GET'])
def get_keywords():
    """
    Get the top keywords used in classification
    
    Query parameters:
    - output_path: Path to the output folder containing results (required)
    - limit: Maximum number of keywords to return (default: 10)
    
    Response JSON:
    {
        "success": true/false,
        "labels": ["train", "predict", "fit", "inference"],
        "counts": [30, 25, 18, 12],
        "total_unique_keywords": 45
    }
    """
    try:
        output_path = request.args.get('output_path')
        limit = request.args.get('limit', default=10, type=int)
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path parameter is required'
            }), 400
        
        # Validate limit
        if limit < 1 or limit > 100:
            return jsonify({
                'success': False,
                'message': 'limit must be between 1 and 100'
            }), 400
        
        # Validate output path
        is_valid, message = analytics_service.validate_output_path(output_path)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Get keywords
        keywords = analytics_service.get_top_keywords(output_path, limit)
        
        if not keywords.get('success'):
            return jsonify(keywords), 500
        
        return jsonify(keywords), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting keywords: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get keywords'
        }), 500


@analytics_bp.route('/libraries', methods=['GET'])
def get_libraries():
    """
    Get the distribution of libraries used
    
    Query parameters:
    - output_path: Path to the output folder containing results (required)
    - limit: Maximum number of libraries to return (default: 10)
    
    Response JSON:
    {
        "success": true/false,
        "labels": ["tensorflow", "torch", "keras", "sklearn"],
        "counts": [45, 38, 25, 12],
        "total_unique_libraries": 15
    }
    """
    try:
        output_path = request.args.get('output_path')
        limit = request.args.get('limit', default=10, type=int)
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path parameter is required'
            }), 400
        
        # Validate limit
        if limit < 1 or limit > 100:
            return jsonify({
                'success': False,
                'message': 'limit must be between 1 and 100'
            }), 400
        
        # Validate output path
        is_valid, message = analytics_service.validate_output_path(output_path)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Get libraries
        libraries = analytics_service.get_library_distribution(output_path, limit)
        
        if not libraries.get('success'):
            return jsonify(libraries), 500
        
        return jsonify(libraries), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting libraries: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get libraries'
        }), 500


@analytics_bp.route('/filter', methods=['GET'])
def filter_results():
    """
    Get filtered results based on various criteria
    
    Query parameters:
    - output_path: Path to the output folder containing results (required)
    - type: Filter by type ('consumer' or 'producer')
    - keyword: Filter by specific keyword
    - library: Filter by specific library
    - project: Filter by project name (partial match)
    - limit: Maximum number of results to return (default: 100)
    
    Response JSON:
    {
        "success": true/false,
        "count": 15,
        "results": [...],
        "filters_applied": {
            "type": "consumer",
            "keyword": ".predict(",
            "library": "tensorflow",
            "project": null
        }
    }
    """
    try:
        output_path = request.args.get('output_path')
        filter_type = request.args.get('type')
        keyword = request.args.get('keyword')
        library = request.args.get('library')
        project = request.args.get('project')
        limit = request.args.get('limit', default=100, type=int)
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path parameter is required'
            }), 400
        
        # Validate filter_type if provided
        if filter_type and filter_type not in ['consumer', 'producer']:
            return jsonify({
                'success': False,
                'message': 'type must be either "consumer" or "producer"'
            }), 400
        
        # Validate limit
        if limit < 1 or limit > 1000:
            return jsonify({
                'success': False,
                'message': 'limit must be between 1 and 1000'
            }), 400
        
        # Validate output path
        is_valid, message = analytics_service.validate_output_path(output_path)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Get filtered results
        results = analytics_service.get_filtered_results(
            output_path=output_path,
            filter_type=filter_type,
            keyword=keyword,
            library=library,
            project=project,
            limit=limit
        )
        
        if not results.get('success'):
            return jsonify(results), 500
        
        return jsonify(results), 200
        
    except Exception as e:
        current_app.logger.error(f'Error filtering results: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to filter results'
        }), 500


@analytics_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for analytics service
    
    Response JSON:
    {
        "status": "healthy",
        "service": "Analytics API"
    }
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Analytics API'
    }), 200
