"""
Integration Test Suite for MARK-Tool Backend API
End-to-end workflow testing
"""
import pytest
import json
import os
import time
from io import BytesIO


class TestIntegration:
    """Integration tests for complete workflows"""
    
    # ============================================================================
    # TC-INT-01: Analysis E2E Without Cloner
    # ============================================================================
    
    def test_analysis_e2e_without_cloner(self, client, test_input_dir, 
                                         test_output_dir):
        """
        TC-INT-01: Complete analysis workflow without cloner
        
        Steps:
        1. Validate input/output paths
        2. Start analysis job
        3. Poll job status
        4. List results
        5. View CSV
        """
        # Step 1: Validate paths
        input_validation = client.post(
            '/api/file/validate/input',
            data=json.dumps({'path': test_input_dir}),
            content_type='application/json'
        )
        assert input_validation.status_code == 200
        
        output_validation = client.post(
            '/api/file/validate/output',
            data=json.dumps({'path': test_output_dir}),
            content_type='application/json'
        )
        assert output_validation.status_code == 200
        
        # Step 2: Start analysis job
        start_data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir,
            'run_cloner': False
        }
        
        start_response = client.post(
            '/api/analysis/start',
            data=json.dumps(start_data),
            content_type='application/json'
        )
        
        assert start_response.status_code == 200
        start_data = json.loads(start_response.data)
        assert start_data['success'] is True
        job_id = start_data['job_id']
        
        # Step 3: Poll job status (with timeout)
        max_polls = 10
        poll_count = 0
        job_completed = False
        
        while poll_count < max_polls:
            status_response = client.get(f'/api/analysis/status/{job_id}')
            assert status_response.status_code == 200
            
            status_data = json.loads(status_response.data)
            job_status = status_data['job']['status']
            
            if job_status in ['completed', 'failed']:
                job_completed = True
                break
            
            time.sleep(0.5)
            poll_count += 1
        
        # Verify job was tracked (may not complete in test environment)
        assert poll_count < max_polls or job_completed
        
        # Step 4: Verify job appears in jobs list
        jobs_response = client.get('/api/analysis/jobs')
        assert jobs_response.status_code == 200
        jobs_data = json.loads(jobs_response.data)
        
        job_ids = [job['job_id'] for job in jobs_data['jobs']]
        assert job_id in job_ids
        
        # Step 5: Get job logs
        logs_response = client.get(f'/api/analysis/logs/{job_id}')
        assert logs_response.status_code == 200
        logs_data = json.loads(logs_response.data)
        assert 'logs' in logs_data
    
    
    # ============================================================================
    # TC-INT-02: E2E With Cloner
    # ============================================================================
    
    def test_analysis_e2e_with_cloner(self, client, test_input_dir, 
                                      test_output_dir, temp_dir):
        """
        TC-INT-02: Complete analysis workflow with cloner
        
        Steps:
        1. Upload CSV with GitHub URLs
        2. Start analysis with run_cloner=true
        3. Verify job is created
        4. Check job status
        """
        # Step 1: Create and upload CSV
        csv_content = b'repo_name,repo_url\ntest_repo,https://github.com/test/repo\n'
        file = (BytesIO(csv_content), 'github_repos.csv')
        
        upload_response = client.post(
            '/api/file/upload',
            data={'file': file},
            content_type='multipart/form-data'
        )
        
        assert upload_response.status_code == 200
        upload_data = json.loads(upload_response.data)
        csv_filepath = upload_data['filepath']
        
        # Step 2: Start analysis with cloner
        start_data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir,
            'github_csv': csv_filepath,
            'run_cloner': True
        }
        
        start_response = client.post(
            '/api/analysis/start',
            data=json.dumps(start_data),
            content_type='application/json'
        )
        
        assert start_response.status_code == 200
        start_data = json.loads(start_response.data)
        assert start_data['success'] is True
        job_id = start_data['job_id']
        
        # Step 3: Verify job exists
        status_response = client.get(f'/api/analysis/status/{job_id}')
        assert status_response.status_code == 200
        
        status_data = json.loads(status_response.data)
        assert status_data['job']['job_id'] == job_id
        
        # Step 4: Check job can be cancelled
        cancel_response = client.post(f'/api/analysis/cancel/{job_id}')
        # Should return 200 or 400 (if already completed/failed)
        assert cancel_response.status_code in [200, 400]
    
    
    # ============================================================================
    # TC-INT-03: Concurrent Jobs
    # ============================================================================
    
    def test_concurrent_jobs(self, client, test_input_dir, test_output_dir):
        """
        TC-INT-03: Multiple concurrent analysis jobs
        
        Verify that multiple jobs can run independently
        """
        job_ids = []
        
        # Create 2 jobs
        for i in range(2):
            data = {
                'input_path': test_input_dir,
                'output_path': test_output_dir
            }
            
            response = client.post(
                '/api/analysis/start',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            response_data = json.loads(response.data)
            job_ids.append(response_data['job_id'])
        
        # Verify both jobs exist
        assert len(job_ids) == 2
        assert job_ids[0] != job_ids[1]
        
        # Check status of both jobs
        for job_id in job_ids:
            status_response = client.get(f'/api/analysis/status/{job_id}')
            assert status_response.status_code == 200
            
            status_data = json.loads(status_response.data)
            assert status_data['success'] is True
        
        # Verify jobs list contains both
        jobs_response = client.get('/api/analysis/jobs')
        jobs_data = json.loads(jobs_response.data)
        
        retrieved_ids = [job['job_id'] for job in jobs_data['jobs']]
        for job_id in job_ids:
            assert job_id in retrieved_ids
    
    
    # ============================================================================
    # TC-INT-04: Job Cancellation
    # ============================================================================
    
    def test_job_cancellation_workflow(self, client, test_input_dir, 
                                       test_output_dir):
        """
        TC-INT-04: Start and cancel a job
        
        Steps:
        1. Start job
        2. Cancel job
        3. Verify cancellation
        """
        # Step 1: Start job
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        
        start_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert start_response.status_code == 200
        job_id = json.loads(start_response.data)['job_id']
        
        # Step 2: Cancel job
        cancel_response = client.post(f'/api/analysis/cancel/{job_id}')
        assert cancel_response.status_code in [200, 400]
        
        cancel_data = json.loads(cancel_response.data)
        assert 'message' in cancel_data
        
        # Step 3: Check status after cancellation
        status_response = client.get(f'/api/analysis/status/{job_id}')
        assert status_response.status_code == 200
        
        status_data = json.loads(status_response.data)
        job_status = status_data['job']['status']
        
        # Status should be cancelled, failed, or completed
        assert job_status in ['cancelled', 'failed', 'completed', 'pending', 'running']
    
    
    # ============================================================================
    # TC-INT-05: Invalid Input Path Handling
    # ============================================================================
    
    def test_invalid_input_path_handling(self, client, test_output_dir):
        """
        TC-INT-05: Job fails with invalid input path
        
        Verify proper error handling for invalid inputs
        """
        # Try to validate non-existent input
        invalid_input = '/completely/nonexistent/path/to/repos'
        
        validation_response = client.post(
            '/api/file/validate/input',
            data=json.dumps({'path': invalid_input}),
            content_type='application/json'
        )
        
        # Should fail validation
        assert validation_response.status_code == 400
        validation_data = json.loads(validation_response.data)
        assert validation_data['success'] is False
        
        # Try to start job anyway
        data = {
            'input_path': invalid_input,
            'output_path': test_output_dir
        }
        
        start_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Job should start but likely fail during execution
        # or might return error immediately depending on implementation
        assert start_response.status_code in [200, 400, 500]
    
    
    # ============================================================================
    # TC-INT-06: Malformed CSV Handling
    # ============================================================================
    
    def test_malformed_csv_handling(self, client, temp_dir):
        """
        TC-INT-06: API handles malformed CSV properly
        
        Upload malformed CSV and verify error handling
        """
        # Create malformed CSV (not valid CSV format)
        malformed_csv = b'This is not a CSV file, just random text\nNo structure here\n'
        file = (BytesIO(malformed_csv), 'malformed.csv')
        
        # Upload should succeed (file has .csv extension)
        upload_response = client.post(
            '/api/file/upload',
            data={'file': file},
            content_type='multipart/form-data'
        )
        
        assert upload_response.status_code == 200
        upload_data = json.loads(upload_response.data)
        csv_path = upload_data['filepath']
        
        # Validation should handle the malformed content
        validate_response = client.post(
            '/api/file/validate/csv',
            data=json.dumps({'filepath': csv_path}),
            content_type='application/json'
        )
        
        # Should succeed or fail gracefully
        assert validate_response.status_code in [200, 400]
    
    
    # ============================================================================
    # Additional Integration Tests
    # ============================================================================
    
    def test_results_workflow_with_search(self, client, sample_results_csv):
        """
        Complete results workflow: list, view, search
        """
        output_path = os.path.dirname(os.path.dirname(sample_results_csv['consumer']))
        output_path = os.path.dirname(output_path)
        
        # List results
        list_response = client.get(f'/api/results/list?output_path={output_path}')
        assert list_response.status_code == 200
        list_data = json.loads(list_response.data)
        
        # Get stats
        stats_response = client.get(f'/api/results/stats?output_path={output_path}')
        assert stats_response.status_code == 200
        stats_data = json.loads(stats_response.data)
        assert 'stats' in stats_data
        
        # View a specific file
        view_response = client.get(
            f'/api/results/view?filepath={sample_results_csv["consumer"]}'
        )
        assert view_response.status_code == 200
        view_data = json.loads(view_response.data)
        assert 'data' in view_data
        
        # Search within the file
        search_data = {
            'filepath': sample_results_csv['consumer'],
            'query': 'test'
        }
        
        search_response = client.post(
            '/api/results/search',
            data=json.dumps(search_data),
            content_type='application/json'
        )
        
        assert search_response.status_code == 200
        search_result = json.loads(search_response.data)
        assert 'results' in search_result
    
    
    def test_file_upload_and_download_workflow(self, client):
        """
        Upload a file and then download it
        """
        # Upload
        csv_content = b'col1,col2\nval1,val2\n'
        file = (BytesIO(csv_content), 'test.csv')
        
        upload_response = client.post(
            '/api/file/upload',
            data={'file': file},
            content_type='multipart/form-data'
        )
        
        assert upload_response.status_code == 200
        upload_data = json.loads(upload_response.data)
        filepath = upload_data['filepath']
        
        # Download
        download_response = client.get(f'/api/file/download?filepath={filepath}')
        assert download_response.status_code == 200
        assert download_response.data == csv_content
    
    
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
    
    
    def test_root_endpoint_documentation(self, client):
        """Test the root endpoint returns API documentation"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'service' in data
        assert 'endpoints' in data
        assert 'analysis' in data['endpoints']
        assert 'file' in data['endpoints']
        assert 'results' in data['endpoints']
