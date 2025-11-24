"""
File Service - Handles file upload, validation, and management
"""
import os
import csv
from pathlib import Path
from werkzeug.utils import secure_filename
from typing import Optional, Tuple, List, Dict


class FileService:
    """Service for handling file operations"""
    
    def __init__(self, upload_folder: str, allowed_extensions: set):
        """
        Initialize the file service
        
        Args:
            upload_folder: Path to the folder for uploaded files
            allowed_extensions: Set of allowed file extensions
        """
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
    
    def allowed_file(self, filename: str) -> bool:
        """
        Check if a file has an allowed extension
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file extension is allowed, False otherwise
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def handle_csv_upload(self, file) -> Tuple[bool, str, Optional[str]]:
        """
        Handle CSV file upload
        
        Args:
            file: File object from Flask request
            
        Returns:
            Tuple of (success, message, filepath)
        """
        if not file:
            return False, "No file provided", None
        
        if file.filename == '':
            return False, "No file selected", None
        
        if not self.allowed_file(file.filename):
            return False, f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}", None
        
        try:
            # Secure the filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_folder, filename)
            
            # Save the file
            file.save(filepath)
            
            # Validate it's a valid CSV
            is_valid, validation_msg = self.validate_csv(filepath)
            if not is_valid:
                # Remove invalid file
                os.remove(filepath)
                return False, validation_msg, None
            
            return True, f"File '{filename}' uploaded successfully", filepath
            
        except Exception as e:
            return False, f"Error uploading file: {str(e)}", None
    
    def validate_csv(self, filepath: str) -> Tuple[bool, str]:
        """
        Validate that a file is a valid CSV
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Try to read the CSV
                csv_reader = csv.reader(f)
                header = next(csv_reader, None)
                
                if header is None:
                    return False, "CSV file is empty"
                
                # Read first few rows to ensure it's valid
                row_count = 0
                for row in csv_reader:
                    row_count += 1
                    if row_count >= 5:  # Check first 5 rows
                        break
                
                return True, "Valid CSV file"
                
        except csv.Error as e:
            return False, f"Invalid CSV format: {str(e)}"
        except UnicodeDecodeError:
            return False, "Invalid file encoding. Please use UTF-8"
        except Exception as e:
            return False, f"Error validating CSV: {str(e)}"
    
    def validate_input_folder(self, folder_path: str) -> Tuple[bool, str]:
        """
        Validate the input folder path
        
        Args:
            folder_path: Path to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not folder_path:
            return False, "Input folder path is required"
        
        # Convert to absolute path
        abs_path = os.path.abspath(folder_path)
        
        # Check if path exists
        if not os.path.exists(abs_path):
            return False, f"Path does not exist: {abs_path}"
        
        # Check if it's a directory
        if not os.path.isdir(abs_path):
            return False, f"Path is not a directory: {abs_path}"
        
        # Check if readable
        if not os.access(abs_path, os.R_OK):
            return False, f"Directory is not readable: {abs_path}"
        
        return True, f"Valid input folder: {abs_path}"
    
    def validate_output_folder(self, folder_path: str) -> Tuple[bool, str]:
        """
        Validate the output folder path (creates if doesn't exist)
        
        Args:
            folder_path: Path to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not folder_path:
            return False, "Output folder path is required"
        
        # Convert to absolute path
        abs_path = os.path.abspath(folder_path)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(abs_path, exist_ok=True)
            
            # Check if writable
            if not os.access(abs_path, os.W_OK):
                return False, f"Directory is not writable: {abs_path}"
            
            return True, f"Valid output folder: {abs_path}"
            
        except Exception as e:
            return False, f"Error creating/accessing output folder: {str(e)}"
    
    def get_csv_content(self, filepath: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Read CSV file and return its content
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Tuple of (success, message, data_dict)
            data_dict contains 'headers' and 'rows'
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader, [])
                rows = list(csv_reader)
                
                data = {
                    'headers': headers,
                    'rows': rows,
                    'row_count': len(rows),
                    'column_count': len(headers)
                }
                
                return True, "CSV loaded successfully", data
                
        except Exception as e:
            return False, f"Error reading CSV: {str(e)}", None
    
    def list_csv_files(self, directory: str) -> List[Dict[str, str]]:
        """
        List all CSV files in a directory
        
        Args:
            directory: Path to search for CSV files
            
        Returns:
            List of dictionaries with file information
        """
        csv_files = []
        
        if not os.path.exists(directory):
            return csv_files
        
        try:
            for filename in os.listdir(directory):
                if filename.lower().endswith('.csv'):
                    filepath = os.path.join(directory, filename)
                    file_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'size': os.path.getsize(filepath),
                        'modified': os.path.getmtime(filepath)
                    }
                    csv_files.append(file_info)
            
            # Sort by modification time (newest first)
            csv_files.sort(key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            print(f"Error listing CSV files: {str(e)}")
        
        return csv_files
    
    def cleanup_old_uploads(self, max_age_hours: int = 24):
        """
        Clean up old uploaded files
        
        Args:
            max_age_hours: Maximum age of files to keep (in hours)
        """
        import time
        
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.upload_folder):
                filepath = os.path.join(self.upload_folder, filename)
                
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        print(f"Removed old upload: {filename}")
                        
        except Exception as e:
            print(f"Error cleaning up uploads: {str(e)}")
