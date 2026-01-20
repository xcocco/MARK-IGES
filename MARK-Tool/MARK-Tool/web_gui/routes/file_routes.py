"""
File Routes - API endpoints for file operations
"""
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
import os
from services.file_service import FileService


# Create blueprint
file_bp = Blueprint('file', __name__, url_prefix='/api/file')

# Service instance (will be initialized in app.py)
file_service: FileService = None


def init_file_service(service: FileService):
    """Initialize the file service"""
    global file_service
    file_service = service


@file_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload a CSV file
    
    Form data:
    - file: The CSV file to upload
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "filepath": "/path/to/file"
    }
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file part in request'
            }), 400
        
        file = request.files['file']
        
        # Handle upload
        success, message, filepath = file_service.handle_csv_upload(file)
        
        status_code = 200 if success else 400
        
        response_data = {
            'success': success,
            'message': message
        }
        
        if filepath:
            response_data['filepath'] = filepath
        
        return jsonify(response_data), status_code
        
    except Exception as e:
        current_app.logger.error(f"Error uploading file: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error uploading file: {str(e)}'
        }), 500


@file_bp.route('/validate/input', methods=['POST'])
def validate_input_folder():
    """
    Validate an input folder path
    
    Request JSON:
    {
        "path": "/path/to/folder"
    }
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "path": "/absolute/path"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'path' not in data:
            return jsonify({
                'success': False,
                'message': 'Path is required'
            }), 400
        
        path = data['path']
        
        # Validate path
        is_valid, message = file_service.validate_input_folder(path)
        
        status_code = 200 if is_valid else 400
        
        response_data = {
            'success': is_valid,
            'message': message
        }
        
        if is_valid:
            response_data['path'] = os.path.abspath(path)
        
        return jsonify(response_data), status_code
        
    except Exception as e:
        current_app.logger.error(f"Error validating input folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error validating input folder: {str(e)}'
        }), 500


@file_bp.route('/validate/output', methods=['POST'])
def validate_output_folder():
    """
    Validate an output folder path
    
    Request JSON:
    {
        "path": "/path/to/folder"
    }
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "path": "/absolute/path"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'path' not in data:
            return jsonify({
                'success': False,
                'message': 'Path is required'
            }), 400
        
        path = data['path']
        
        # Validate path
        is_valid, message = file_service.validate_output_folder(path)
        
        status_code = 200 if is_valid else 400
        
        response_data = {
            'success': is_valid,
            'message': message
        }
        
        if is_valid:
            response_data['path'] = os.path.abspath(path)
        
        return jsonify(response_data), status_code
        
    except Exception as e:
        current_app.logger.error(f"Error validating output folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error validating output folder: {str(e)}'
        }), 500


@file_bp.route('/validate/csv', methods=['POST'])
def validate_csv():
    """
    Validate a CSV file
    
    Request JSON:
    {
        "filepath": "/path/to/file.csv"
    }
    
    Response JSON:
    {
        "success": true/false,
        "message": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'filepath' not in data:
            return jsonify({
                'success': False,
                'message': 'Filepath is required'
            }), 400
        
        filepath = data['filepath']
        
        # Validate CSV
        is_valid, message = file_service.validate_csv(filepath)
        
        status_code = 200 if is_valid else 400
        
        return jsonify({
            'success': is_valid,
            'message': message
        }), status_code
        
    except Exception as e:
        current_app.logger.error(f"Error validating CSV: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error validating CSV: {str(e)}'
        }), 500


@file_bp.route('/download', methods=['GET'])
def download_file():
    """
    Download a file
    
    Query parameters:
    - filepath: Path to the file to download
    
    Returns:
    File download
    """
    try:
        filepath = request.args.get('filepath')
        
        if not filepath:
            return jsonify({
                'success': False,
                'message': 'Filepath is required'
            }), 400
        
        # Security check - ensure file exists and is accessible
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'File not found'
            }), 404
        
        if not os.path.isfile(filepath):
            return jsonify({
                'success': False,
                'message': 'Path is not a file'
            }), 400
        
        # Send file
        return send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath)
        )
        
    except Exception as e:
        current_app.logger.error(f"Error downloading file: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error downloading file: {str(e)}'
        }), 500


@file_bp.route('/list', methods=['GET'])
def list_files():
    """
    List files in a directory
    
    Query parameters:
    - directory: Path to the directory
    
    Response JSON:
    {
        "success": true/false,
        "message": "...",
        "files": [...]
    }
    """
    try:
        directory = request.args.get('directory')
        
        if not directory:
            return jsonify({
                'success': False,
                'message': 'Directory is required'
            }), 400
        
        # List CSV files
        files = file_service.list_csv_files(directory)
        
        return jsonify({
            'success': True,
            'message': f'Found {len(files)} CSV files',
            'files': files
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error listing files: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error listing files: {str(e)}'
        }), 500
