"""
Results Routes - API endpoints for viewing analysis results
"""
from flask import Blueprint, request, jsonify, current_app
import os
from ..services.file_service import FileService


# Create blueprint
results_bp = Blueprint('results', __name__, url_prefix='/api/results')

# Service instance (will be initialized in app.py)
file_service: FileService = None


def init_file_service(service: FileService):
    """Initialize the file service"""
    global file_service
    file_service = service


@results_bp.route('/list', methods=['GET'])
def list_results():
    """
    List all result files (consumers and producers)
    
    Query parameters:
    - output_path: Path to the output folder
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "consumers": [...],
        "producers": [...]
    }
    """
    try:
        output_path = request.args.get('output_path')
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path is required'
            }), 400
        
        # Check if output path exists
        if not os.path.exists(output_path):
            return jsonify({
                'success': False,
                'message': f'Output path does not exist: {output_path}'
            }), 404
        
        # List CSV files
        consumers = file_service.list_csv_files(os.path.join(output_path, "Consumers", "Consumers_Final"))
        producers = file_service.list_csv_files(os.path.join(output_path, "Producers", "Producers_Final"))
        all_files = consumers + producers
        
        return jsonify({
            'success': True,
            'message': f'Found {len(consumers)} consumer and {len(producers)} producer files',
            'consumers': consumers,
            'producers': producers,
            'all_files': all_files
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error listing results: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error listing results: {str(e)}'
        }), 500


@results_bp.route('/view', methods=['GET'])
def view_csv():
    """
    View the contents of a CSV file
    
    Query parameters:
    - filepath: Path to the CSV file
    - limit: Maximum number of rows to return (default: 1000)
    - offset: Number of rows to skip (default: 0)
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "data": {
            "headers": [...],
            "rows": [...],
            "row_count": 123,
            "column_count": 5,
            "total_rows": 500,
            "has_more": true/false
        }
    }
    """
    try:
        filepath = request.args.get('filepath')
        limit = request.args.get('limit', 1000, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if not filepath:
            return jsonify({
                'success': False,
                'message': 'filepath is required'
            }), 400
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': f'File not found: {filepath}'
            }), 404
        
        # Get CSV content
        success, message, data = file_service.get_csv_content(filepath)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Apply pagination
        total_rows = len(data['rows'])
        paginated_rows = data['rows'][offset:offset + limit]
        has_more = (offset + limit) < total_rows
        
        response_data = {
            'success': True,
            'message': f'Retrieved {len(paginated_rows)} rows',
            'data': {
                'headers': data['headers'],
                'rows': paginated_rows,
                'row_count': len(paginated_rows),
                'column_count': data['column_count'],
                'total_rows': total_rows,
                'has_more': has_more,
                'offset': offset,
                'limit': limit
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error viewing CSV: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error viewing CSV: {str(e)}'
        }), 500


@results_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about the results
    
    Query parameters:
    - output_path: Path to the output folder
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "stats": {
            "total_files": 10,
            "consumer_files": 5,
            "producer_files": 5,
            "total_size": 12345,
            "latest_file": {...}
        }
    }
    """
    try:
        output_path = request.args.get('output_path')
        
        if not output_path:
            return jsonify({
                'success': False,
                'message': 'output_path is required'
            }), 400
        
        # Check if output path exists
        if not os.path.exists(output_path):
            return jsonify({
                'success': False,
                'message': f'Output path does not exist: {output_path}'
            }), 404
        
        # Get all CSV files
        all_files = file_service.list_csv_files(output_path)
        
        # Calculate statistics
        consumer_files = [f for f in all_files if 'consumer' in f['filename'].lower()]
        producer_files = [f for f in all_files if 'producer' in f['filename'].lower()]
        
        total_size = sum(f['size'] for f in all_files)
        latest_file = all_files[0] if all_files else None
        
        stats = {
            'total_files': len(all_files),
            'consumer_files': len(consumer_files),
            'producer_files': len(producer_files),
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'latest_file': latest_file
        }
        
        return jsonify({
            'success': True,
            'message': 'Statistics retrieved successfully',
            'stats': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting stats: {str(e)}'
        }), 500


@results_bp.route('/search', methods=['POST'])
def search_results():
    """
    Search within CSV results
    
    Request JSON:
    {
        "filepath": "/path/to/file.csv",
        "query": "search term",
        "column": "column_name" (optional)
    }
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "results": {
            "matches": [...],
            "match_count": 10
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        filepath = data.get('filepath')
        query = data.get('query')
        column = data.get('column')
        
        if not filepath:
            return jsonify({
                'success': False,
                'message': 'filepath is required'
            }), 400
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'query is required'
            }), 400
        
        # Get CSV content
        success, message, csv_data = file_service.get_csv_content(filepath)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Perform search
        matches = []
        headers = csv_data['headers']
        
        # If column specified, get its index
        column_index = None
        if column and column in headers:
            column_index = headers.index(column)
        
        # Search through rows
        for row_idx, row in enumerate(csv_data['rows']):
            # Search in specific column or all columns
            if column_index is not None:
                # Search specific column
                if column_index < len(row) and query.lower() in str(row[column_index]).lower():
                    matches.append({
                        'row_index': row_idx,
                        'row_data': row
                    })
            else:
                # Search all columns
                if any(query.lower() in str(cell).lower() for cell in row):
                    matches.append({
                        'row_index': row_idx,
                        'row_data': row
                    })
        
        return jsonify({
            'success': True,
            'message': f'Found {len(matches)} matches',
            'results': {
                'headers': headers,
                'matches': matches[:100],  # Limit to first 100 matches
                'match_count': len(matches),
                'query': query,
                'column': column
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error searching results: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error searching results: {str(e)}'
        }), 500
