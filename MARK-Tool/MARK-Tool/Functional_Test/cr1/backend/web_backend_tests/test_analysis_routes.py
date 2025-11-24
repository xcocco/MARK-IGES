"""
Test Suite for Analysis Routes
Tests all analysis-related API endpoints using category partitioning
"""
import pytest
import json
import time


class TestAnalysisRoutes:
    """Test cases for /api/analysis/* endpoints"""
    
    # ============================================================================
    # TC-A01 to TC-A04: POST /api/analysis/start
    # ============================================================================
    
    @pytest.mark.parametrize("input_path,output_path,github_csv,run_cloner,expected_status,expected_msg_key", [
        # TC-A01: Valid inputs without cloner
        ("valid", "valid", None, False, 200, "success"),
        # TC-A04: Valid inputs with cloner
        ("valid", "valid", "valid", True, 200, "success"),
    ])
    def test_start_analysis_valid(self, client, test_input_dir, test_output_dir, 
                                   sample_csv_file, input_path, output_path, 
                                   github_csv, run_cloner, expected_status, 
                                   expected_msg_key):
        """
        TC-A01, TC-A04: Test analysis start with valid inputs
        
        Category Partition:
        - input_path: valid
        - output_path: valid
        - github_csv: null or valid
        - run_cloner: true or false
        """
        # Prepare request data
        data = {
            'input_path': test_input_dir if input_path == "valid" else input_path,
            'output_path': test_output_dir if output_path == "valid" else output_path,
            'run_cloner': run_cloner
        }
        
        if github_csv == "valid":
            data['github_csv'] = sample_csv_file
        
        # Make request
        response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == expected_status
        response_data = json.loads(response.data)
        assert response_data['success'] == (expected_msg_key == "success")
        
        if expected_msg_key == "success":
            assert 'job_id' in response_data
            assert response_data['job_id'] is not None
    
    
    @pytest.mark.parametrize("missing_field,expected_msg", [
        # TC-A02: Missing input_path
        ("input_path", "input_path is required"),
        # TC-A03: Missing output_path
        ("output_path", "output_path is required"),
    ])
    def test_start_analysis_missing_fields(self, client, test_input_dir, 
                                           test_output_dir, missing_field, 
                                           expected_msg):
        """
        TC-A02, TC-A03: Test analysis start with missing required fields
        
        Category Partition:
        - Constraint: If input_path OR output_path missing → 400
        """
        # Prepare data with one missing field
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        del data[missing_field]
        
        # Make request
        response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert expected_msg in response_data['message']
    
    
    def test_start_analysis_no_data(self, client):
        """Test analysis start with no data provided"""
        response = client.post(
            '/api/analysis/start',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-A05 to TC-A06: GET /api/analysis/status/<job_id>
    # ============================================================================
    
    def test_get_job_status_existing(self, client, test_input_dir, test_output_dir):
        """
        TC-A05: Get status of existing job
        
        Expected: 200, job details returned
        """
        # First create a job
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        
        create_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        job_id = json.loads(create_response.data)['job_id']
        
        # Now get its status
        response = client.get(f'/api/analysis/status/{job_id}')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'job' in response_data
        assert response_data['job']['job_id'] == job_id
    
    
    def test_get_job_status_nonexistent(self, client):
        """
        TC-A06: Get status of non-existent job
        
        Expected: 404
        """
        fake_job_id = "nonexistent-job-id-12345"
        
        response = client.get(f'/api/analysis/status/{fake_job_id}')
        
        # Assertions
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'not found' in response_data['message'].lower()
    
    
    # ============================================================================
    # TC-A07: GET /api/analysis/jobs
    # ============================================================================
    
    def test_list_jobs(self, client, test_input_dir, test_output_dir):
        """
        TC-A07: List all analysis jobs
        
        Expected: 200, array of jobs
        """
        # Create a couple of jobs
        for i in range(2):
            data = {
                'input_path': test_input_dir,
                'output_path': test_output_dir
            }
            client.post(
                '/api/analysis/start',
                data=json.dumps(data),
                content_type='application/json'
            )
        
        # Get job list
        response = client.get('/api/analysis/jobs')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'jobs' in response_data
        assert isinstance(response_data['jobs'], list)
        assert len(response_data['jobs']) >= 2
    
    
    def test_list_jobs_empty(self, client):
        """Test listing jobs when no jobs exist"""
        response = client.get('/api/analysis/jobs')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert isinstance(response_data['jobs'], list)
    
    
    # ============================================================================
    # TC-A08: POST /api/analysis/cancel/<job_id>
    # ============================================================================
    
    def test_cancel_job(self, client, test_input_dir, test_output_dir):
        """
        TC-A08: Cancel an analysis job
        
        Expected: 200
        """
        # Create a job
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        
        create_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        job_id = json.loads(create_response.data)['job_id']
        
        # Cancel the job
        response = client.post(f'/api/analysis/cancel/{job_id}')
        
        # Assertions
        assert response.status_code in [200, 400]  # 200 if cancelled, 400 if already completed
        response_data = json.loads(response.data)
        assert 'message' in response_data
    
    
    def test_cancel_nonexistent_job(self, client):
        """Test cancelling a non-existent job"""
        fake_job_id = "nonexistent-job-id-99999"
        
        response = client.post(f'/api/analysis/cancel/{fake_job_id}')
        
        # Should return 400 or similar error
        assert response.status_code >= 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-A09: GET /api/analysis/logs/<job_id>
    # ============================================================================
    
    def test_get_job_logs(self, client, test_input_dir, test_output_dir):
        """
        TC-A09: Get logs for an analysis job
        
        Expected: 200, array of log entries
        """
        # Create a job
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        
        create_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        job_id = json.loads(create_response.data)['job_id']
        
        # Get logs
        response = client.get(f'/api/analysis/logs/{job_id}')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'logs' in response_data
        assert isinstance(response_data['logs'], list)
    
    
    def test_get_job_logs_with_limit(self, client, test_input_dir, test_output_dir):
        """Test getting job logs with custom limit parameter"""
        # Create a job
        data = {
            'input_path': test_input_dir,
            'output_path': test_output_dir
        }
        
        create_response = client.post(
            '/api/analysis/start',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        job_id = json.loads(create_response.data)['job_id']
        
        # Get logs with limit
        response = client.get(f'/api/analysis/logs/{job_id}?limit=10')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert isinstance(response_data['logs'], list)
    
    
    def test_get_logs_nonexistent_job(self, client):
        """Test getting logs for non-existent job"""
        fake_job_id = "nonexistent-job-id-logs"
        
        response = client.get(f'/api/analysis/logs/{fake_job_id}')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
