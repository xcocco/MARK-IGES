"""
Test Suite for Results Routes
Tests all results-related API endpoints using category partitioning
"""
import pytest
import json
import os


class TestResultsRoutes:
    """Test cases for /api/results/* endpoints"""
    
    # ============================================================================
    # TC-R01 to TC-R03: GET /api/results/list
    # ============================================================================
    
    def test_list_results_valid_path(self, client, sample_results_csv):
        """
        TC-R01: List results with valid output path
        
        Expected: 200, consumers/producers arrays
        """
        output_path = os.path.dirname(os.path.dirname(sample_results_csv['consumer']))
        # Go up two more levels to get the output root
        output_path = os.path.dirname(output_path)
        
        response = client.get(f'/api/results/list?output_path={output_path}')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'consumers' in response_data
        assert 'producers' in response_data
        assert isinstance(response_data['consumers'], list)
        assert isinstance(response_data['producers'], list)
    
    
    def test_list_results_missing_path(self, client):
        """
        TC-R02: List results with missing path
        
        Expected: 400
        """
        response = client.get('/api/results/list')
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'required' in response_data['message'].lower()
    
    
    def test_list_results_nonexistent_path(self, client):
        """
        TC-R03: List results with non-existent path
        
        Expected: 404
        """
        response = client.get('/api/results/list?output_path=/nonexistent/path')
        
        # Assertions
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'not exist' in response_data['message'].lower()
    
    
    # ============================================================================
    # TC-R04 to TC-R07: GET /api/results/view
    # ============================================================================
    
    def test_view_csv_valid(self, client, sample_results_csv):
        """
        TC-R04: View CSV with valid filepath
        
        Expected: 200, headers/rows returned
        """
        response = client.get(
            f'/api/results/view?filepath={sample_results_csv["consumer"]}'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'data' in response_data
        assert 'headers' in response_data['data']
        assert 'rows' in response_data['data']
        assert 'row_count' in response_data['data']
        assert 'column_count' in response_data['data']
        
        # Verify data content
        data = response_data['data']
        assert len(data['headers']) > 0
        assert data['column_count'] == len(data['headers'])
    
    
    @pytest.mark.parametrize("limit,offset,expected_max_rows", [
        # TC-R05: With pagination - limit 1
        (1, 0, 1),
        # Different pagination settings
        (10, 0, 10),
        (5, 1, 5),
    ])
    def test_view_csv_with_pagination(self, client, sample_results_csv, 
                                      limit, offset, expected_max_rows):
        """
        TC-R05: View CSV with pagination
        
        Expected: 200, paginated data
        """
        response = client.get(
            f'/api/results/view?filepath={sample_results_csv["consumer"]}'
            f'&limit={limit}&offset={offset}'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        
        data = response_data['data']
        assert 'rows' in data
        assert len(data['rows']) <= expected_max_rows
        assert data['limit'] == limit
        assert data['offset'] == offset
        assert 'has_more' in data
        assert 'total_rows' in data
    
    
    def test_view_csv_missing_filepath(self, client):
        """
        TC-R06: View CSV with missing filepath
        
        Expected: 400
        """
        response = client.get('/api/results/view')
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'required' in response_data['message'].lower()
    
    
    def test_view_csv_nonexistent_file(self, client):
        """
        TC-R07: View non-existent CSV file
        
        Expected: 404
        """
        response = client.get('/api/results/view?filepath=/nonexistent/file.csv')
        
        # Assertions
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'not found' in response_data['message'].lower()
    
    
    # ============================================================================
    # TC-R08: GET /api/results/stats
    # ============================================================================
    
    def test_get_results_statistics(self, client, sample_results_csv):
        """
        TC-R08: Get statistics about results
        
        Expected: 200, statistics object
        """
        output_path = os.path.dirname(os.path.dirname(sample_results_csv['consumer']))
        output_path = os.path.dirname(output_path)
        
        response = client.get(f'/api/results/stats?output_path={output_path}')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'stats' in response_data
        
        stats = response_data['stats']
        assert 'total_files' in stats
        assert 'consumer_files' in stats
        assert 'producer_files' in stats
        assert 'total_size' in stats
        assert isinstance(stats['total_files'], int)
    
    
    def test_get_stats_missing_path(self, client):
        """Test get stats with missing output_path"""
        response = client.get('/api/results/stats')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_get_stats_nonexistent_path(self, client):
        """Test get stats with non-existent path"""
        response = client.get('/api/results/stats?output_path=/nonexistent')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    # ============================================================================
    # TC-R09 to TC-R12: POST /api/results/search
    # ============================================================================
    
    def test_search_results_valid_query(self, client, sample_results_csv):
        """
        TC-R09: Search with valid query
        
        Expected: 200, search results
        """
        data = {
            'filepath': sample_results_csv['consumer'],
            'query': 'sklearn'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'results' in response_data
        
        results = response_data['results']
        assert 'matches' in results
        assert 'match_count' in results
        assert 'headers' in results
        assert isinstance(results['matches'], list)
    
    
    def test_search_results_with_column_filter(self, client, sample_results_csv):
        """
        TC-R10: Search with column filter
        
        Expected: 200, filtered results
        """
        data = {
            'filepath': sample_results_csv['consumer'],
            'query': 'test',
            'column': 'Repo'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert 'results' in response_data
        assert response_data['results']['column'] == 'Repo'
    
    
    def test_search_results_no_matches(self, client, sample_results_csv):
        """Test search with query that has no matches"""
        data = {
            'filepath': sample_results_csv['consumer'],
            'query': 'nonexistent_search_term_xyz123'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
        assert response_data['results']['match_count'] == 0
    
    
    def test_search_results_missing_filepath(self, client):
        """
        TC-R11: Search with missing filepath
        
        Expected: 400
        """
        data = {
            'query': 'test'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'required' in response_data['message'].lower()
    
    
    def test_search_results_missing_query(self, client, sample_results_csv):
        """
        TC-R12: Search with missing query
        
        Expected: 400
        """
        data = {
            'filepath': sample_results_csv['consumer']
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Assertions
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
        assert 'required' in response_data['message'].lower()
    
    
    def test_search_results_invalid_filepath(self, client):
        """Test search with invalid filepath"""
        data = {
            'filepath': '/nonexistent/file.csv',
            'query': 'test'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] is False
    
    
    def test_search_results_invalid_column(self, client, sample_results_csv):
        """Test search with invalid column name"""
        data = {
            'filepath': sample_results_csv['consumer'],
            'query': 'test',
            'column': 'NonExistentColumn'
        }
        
        response = client.post(
            '/api/results/search',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should still return 200 but search all columns
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['success'] is True
