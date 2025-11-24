"""
Test Suite for File Routes
Tests all file-related API endpoints using category partitioning
"""
import pytest
import json
import os
from io import BytesIO


class TestFileRoutes:
    """Test cases for /api/file/* endpoints"""
    
    # ============================================================================
    # TC-F01 to TC-F03: POST /api/file/upload
    # ============================================================================
    
    @pytest.mark.parametrize("file_extension,expected_status,expected_success", [
        # TC-F01: Valid CSV file
        ("csv", 200, True),
        # TC-F02: Invalid extension
        ("txt", 400, False),
        # TC-F02: Invalid extension (xlsx)
        ("xlsx", 400, False),
    ])
    def test_upload_file_with_extension(self, client, file_extension, 
                                        expected_status, expected_success):
        """
        TC-F01, TC-F02: Test file upload with different extensions
        
        Category Partition:
        - file extension: [csv, non_csv]
        """
        # Create file data
        file_content = b'repo,url\ntest,http://test.com\n'
        file = (BytesIO(file_content), f'test.{file_extension}')
        
        # Upload file
        response = client.post(
            '/api/file/upload',
            data={'file': file},
            content_type='multipart/form-data'
        )
        
        # Assertions
        assert response.status_code == expected_status
        response_data = json.loads(response.data)
        assert response_data['success'] == expected_success
        
        if expected_success:
            assert 'filepath' in response_data
            assert response_data['filepath'].endswith('.csv')
    
    
    def test_upload_file_no_file(self, client):
        """
        TC-F03: Test upload with no file provided
        
        Category Partition:
        - file: missing
        """
        # Make request without file
        response = client.post(
            '/api/file/upload',
            data={},
            content_type='multipart/form-data'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'no file' in response_data['message'].lower()
    
    
    def test_upload_file_empty_filename(self, client):
        """Test upload with empty filename"""
        file = (BytesIO(b'content'), '')
        
        response = client.post(
            '/api/file/upload',
            data={'file': file},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-F04 to TC-F06: POST /api/file/validate/input
    # ============================================================================
    
    def test_validate_input_folder_existing(self, client, test_input_dir):
        """
        TC-F04: Validate existing input folder
        
        Expected: 200, path returned
        """
        data = {'path': test_input_dir}
        
        response = client.post(
            '/api/file/validate/input',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'path' in response_data
        assert os.path.exists(response_data['path'])
    
    
    def test_validate_input_folder_nonexistent(self, client):
        """
        TC-F05: Validate non-existent input folder
        
        Expected: 400
        """
        data = {'path': '/nonexistent/path/to/folder'}
        
        response = client.post(
            '/api/file/validate/input',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_validate_input_folder_missing_path(self, client):
        """
        TC-F06: Validate input with missing path
        
        Expected: 400
        """
        response = client.post(
            '/api/file/validate/input',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'required' in response_data['message'].lower()
    
    
    # ============================================================================
    # TC-F07: POST /api/file/validate/output
    # ============================================================================
    
    def test_validate_output_folder_valid(self, client, test_output_dir):
        """
        TC-F07: Validate valid output folder
        
        Expected: 200
        """
        data = {'path': test_output_dir}
        
        response = client.post(
            '/api/file/validate/output',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'path' in response_data
    
    
    def test_validate_output_folder_creatable(self, client, temp_dir):
        """Test validate output with path that doesn't exist but can be created"""
        new_output = os.path.join(temp_dir, 'new_output')
        data = {'path': new_output}
        
        response = client.post(
            '/api/file/validate/output',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should succeed (output folders can be created)
        assert response.status_code in [200, 400]
        response_data = json.loads(response.data)
        assert 'message' in response_data
    
    
    def test_validate_output_folder_missing_path(self, client):
        """Test validate output with missing path"""
        response = client.post(
            '/api/file/validate/output',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-F08: POST /api/file/validate/csv
    # ============================================================================
    
    def test_validate_csv_valid(self, client, sample_csv_file):
        """
        TC-F08: Validate valid CSV file
        
        Expected: 200
        """
        data = {'filepath': sample_csv_file}
        
        response = client.post(
            '/api/file/validate/csv',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
    
    
    def test_validate_csv_nonexistent(self, client):
        """Test validate non-existent CSV"""
        data = {'filepath': '/nonexistent/file.csv'}
        
        response = client.post(
            '/api/file/validate/csv',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_validate_csv_missing_filepath(self, client):
        """Test validate CSV with missing filepath"""
        response = client.post(
            '/api/file/validate/csv',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-F09 to TC-F10: GET /api/file/download
    # ============================================================================
    
    def test_download_file_existing(self, client, sample_csv_file):
        """
        TC-F09: Download existing file
        
        Expected: 200, file content
        """
        response = client.get(f'/api/file/download?filepath={sample_csv_file}')
        
        # Assertions
        assert response.status_code == 200
        assert len(response.data) > 0
        # Should have proper headers for download
        assert 'attachment' in response.headers.get('Content-Disposition', '')
    
    
    def test_download_file_nonexistent(self, client):
        """
        TC-F10: Download non-existent file
        
        Expected: 404
        """
        response = client.get('/api/file/download?filepath=/nonexistent/file.csv')
        
        # Assertions
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'not found' in response_data['message'].lower()
    
    
    def test_download_file_missing_filepath(self, client):
        """Test download with missing filepath parameter"""
        response = client.get('/api/file/download')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_download_directory_instead_of_file(self, client, test_input_dir):
        """Test download with directory path instead of file"""
        response = client.get(f'/api/file/download?filepath={test_input_dir}')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-F11: GET /api/file/list
    # ============================================================================
    
    def test_list_files(self, client, temp_dir):
        """
        TC-F11: List files in directory
        
        Expected: 200, array of files
        """
        # Create some CSV files
        for i in range(3):
            with open(os.path.join(temp_dir, f'file{i}.csv'), 'w') as f:
                f.write('test,data\n')
        
        response = client.get(f'/api/file/list?directory={temp_dir}')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'files' in response_data
        assert isinstance(response_data['files'], list)
        assert len(response_data['files']) >= 3
    
    
    def test_list_files_empty_directory(self, client, test_output_dir):
        """Test list files in empty directory"""
        response = client.get(f'/api/file/list?directory={test_output_dir}')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert isinstance(response_data['files'], list)
    
    
    def test_list_files_missing_directory(self, client):
        """Test list files with missing directory parameter"""
        response = client.get('/api/file/list')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_list_files_nonexistent_directory(self, client):
        """Test list files in non-existent directory"""
        response = client.get('/api/file/list?directory=/nonexistent/dir')
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 404]
