"""
API tests for Analytics endpoints
Tests all 30 API test cases from CR2 Test Plan
"""
import os
import sys
import unittest
import tempfile
import csv
from pathlib import Path

# Add web_gui directory to path
web_gui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'web_gui'))
sys.path.insert(0, web_gui_path)
sys.path.insert(0, os.path.dirname(web_gui_path))

import web_gui.app as web_app
app = web_app.create_app('testing')


class TestAnalyticsAPI(unittest.TestCase):
    """Test cases for Analytics API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Create sample consumer CSV
        self.consumer_data = [
            {
                'ProjectName': 'TestProject1',
                'Is ML consumer': 'Yes',
                'where': 'test/path/file.py',
                'keyword': '',
                'line_number': '10',
                'libraries': 'tensorflow',
                'keywords': '.predict('
            },
            {
                'ProjectName': 'TestProject2',
                'Is ML consumer': 'Yes',
                'where': 'test/path/file2.py',
                'keyword': '',
                'line_number': '20',
                'libraries': 'torch',
                'keywords': '.no_grad('
            },
            {
                'ProjectName': 'TestProject1',
                'Is ML consumer': 'Yes',
                'where': 'test/path/file3.py',
                'keyword': '',
                'line_number': '30',
                'libraries': 'tensorflow',
                'keywords': '.predict('
            }
        ]
        
        # Create sample producer CSV
        self.producer_data = [
            {
                'ProjectName': 'TestProject1',
                'Is ML producer': 'Yes',
                'where': 'test/path/train.py',
                'keyword': '',
                'line_number': '50',
                'libraries': 'sklearn',
                'keywords': '.fit('
            },
            {
                'ProjectName': 'TestProject3',
                'Is ML producer': 'Yes',
                'where': 'test/path/train2.py',
                'keyword': '',
                'line_number': '60',
                'libraries': 'keras',
                'keywords': '.fit_generator'
            }
        ]
        
        # Write consumer CSV
        consumer_path = os.path.join(self.test_dir, 'consumer.csv')
        with open(consumer_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.consumer_data[0].keys())
            writer.writeheader()
            writer.writerows(self.consumer_data)
        
        # Write producer CSV
        producer_path = os.path.join(self.test_dir, 'producer.csv')
        with open(producer_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.producer_data[0].keys())
            writer.writeheader()
            writer.writerows(self.producer_data)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    # TC-ANA-01 to TC-ANA-05: GET /api/analytics/summary
    
    def test_summary_valid_output_path(self):
        """TC-ANA-01: Summary with valid output path"""
        response = self.client.get(f'/api/analytics/summary?output_path={self.test_dir}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('total_models', data)
        self.assertIn('consumer_count', data)
        self.assertIn('producer_count', data)
    
    def test_summary_missing_output_path(self):
        """TC-ANA-02: Summary without output_path parameter"""
        response = self.client.get('/api/analytics/summary')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('output_path', data.get('message', data.get('error', '')).lower())
    
    def test_summary_nonexistent_path(self):
        """TC-ANA-03: Summary with non-existent path"""
        response = self.client.get('/api/analytics/summary?output_path=/nonexistent/path')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('does not exist', data.get('message', data.get('error', '')).lower())
    
    def test_summary_missing_csv_files(self):
        """TC-ANA-04: Summary with directory missing CSV files"""
        empty_dir = tempfile.mkdtemp()
        
        try:
            response = self.client.get(f'/api/analytics/summary?output_path={empty_dir}')
            
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn('csv', data.get('message', data.get('error', '')).lower())
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_summary_correct_values(self):
        """TC-ANA-05: Summary returns correct values"""
        response = self.client.get(f'/api/analytics/summary?output_path={self.test_dir}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total_models'], 5)
        self.assertEqual(data['consumer_count'], 3)
        self.assertEqual(data['producer_count'], 2)
        self.assertIn('last_analysis_id', data)
    
    # TC-ANA-06 to TC-ANA-10: GET /api/analytics/consumer-producer-distribution
    
    def test_distribution_valid_output_path(self):
        """TC-ANA-06: Distribution with valid output path"""
        response = self.client.get(
            f'/api/analytics/consumer-producer-distribution?output_path={self.test_dir}'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['labels'], ['Consumer', 'Producer'])
        self.assertIn('counts', data)
        self.assertIn('percentages', data)
    
    def test_distribution_missing_output_path(self):
        """TC-ANA-07: Distribution without output_path parameter"""
        response = self.client.get('/api/analytics/consumer-producer-distribution')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('output_path', data.get('message', data.get('error', '')).lower())
    
    def test_distribution_correct_percentages(self):
        """TC-ANA-08: Distribution returns correct percentages"""
        response = self.client.get(
            f'/api/analytics/consumer-producer-distribution?output_path={self.test_dir}'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['counts'], [3, 2])
        self.assertEqual(data['percentages'], [60.0, 40.0])
    
    def test_distribution_empty_dataset(self):
        """TC-ANA-09: Distribution with empty dataset"""
        empty_dir = tempfile.mkdtemp()
        
        with open(os.path.join(empty_dir, 'consumer.csv'), 'w') as f:
            f.write('ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords\n')
        
        with open(os.path.join(empty_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            response = self.client.get(
                f'/api/analytics/consumer-producer-distribution?output_path={empty_dir}'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['counts'], [0, 0])
            self.assertEqual(data['percentages'], [0.0, 0.0])
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_distribution_only_consumers(self):
        """TC-ANA-10: Distribution with only consumers"""
        test_dir = tempfile.mkdtemp()
        
        with open(os.path.join(test_dir, 'consumer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.consumer_data[0].keys())
            writer.writeheader()
            writer.writerows(self.consumer_data)
        
        with open(os.path.join(test_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            response = self.client.get(
                f'/api/analytics/consumer-producer-distribution?output_path={test_dir}'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['counts'][0], 3)
            self.assertEqual(data['counts'][1], 0)
            self.assertEqual(data['percentages'], [100.0, 0.0])
        finally:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)
    
    # TC-ANA-11 to TC-ANA-16: GET /api/analytics/keywords
    
    def test_keywords_default_limit(self):
        """TC-ANA-11: Keywords with default limit"""
        response = self.client.get(f'/api/analytics/keywords?output_path={self.test_dir}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertLessEqual(len(data['labels']), 10)
    
    def test_keywords_custom_limit(self):
        """TC-ANA-12: Keywords with custom limit"""
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=5'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 5)
    
    def test_keywords_boundary_limit_1(self):
        """TC-ANA-13: Keywords with boundary limit=1"""
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=1'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 1)
    
    def test_keywords_boundary_limit_100(self):
        """TC-ANA-14: Keywords with boundary limit=100"""
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=100'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 100)
    
    def test_keywords_invalid_limit_low(self):
        """TC-ANA-15: Keywords with invalid limit (<1)"""
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=0'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('limit', data.get('message', data.get('error', '')).lower())
    
    def test_keywords_invalid_limit_high(self):
        """TC-ANA-16: Keywords with invalid limit (>100)"""
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=101'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('limit', data.get('message', data.get('error', '')).lower())
    
    # TC-ANA-17 to TC-ANA-22: GET /api/analytics/libraries
    
    def test_libraries_default_limit(self):
        """TC-ANA-17: Libraries with default limit"""
        response = self.client.get(f'/api/analytics/libraries?output_path={self.test_dir}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertLessEqual(len(data['labels']), 10)
    
    def test_libraries_custom_limit(self):
        """TC-ANA-18: Libraries with custom limit"""
        response = self.client.get(
            f'/api/analytics/libraries?output_path={self.test_dir}&limit=5'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 5)
    
    def test_libraries_boundary_limit_1(self):
        """TC-ANA-19: Libraries with boundary limit=1"""
        response = self.client.get(
            f'/api/analytics/libraries?output_path={self.test_dir}&limit=1'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 1)
    
    def test_libraries_boundary_limit_100(self):
        """TC-ANA-20: Libraries with boundary limit=100"""
        response = self.client.get(
            f'/api/analytics/libraries?output_path={self.test_dir}&limit=100'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertLessEqual(len(data['labels']), 100)
    
    def test_libraries_invalid_limit_low(self):
        """TC-ANA-21: Libraries with invalid limit (<1)"""
        response = self.client.get(
            f'/api/analytics/libraries?output_path={self.test_dir}&limit=0'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('limit', data.get('message', data.get('error', '')).lower())
    
    def test_libraries_invalid_limit_high(self):
        """TC-ANA-22: Libraries with invalid limit (>100)"""
        response = self.client.get(
            f'/api/analytics/libraries?output_path={self.test_dir}&limit=101'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('limit', data.get('message', data.get('error', '')).lower())
    
    # TC-ANA-23 to TC-ANA-29: GET /api/analytics/filter
    
    def test_filter_type_consumer(self):
        """TC-ANA-23: Filter by type=consumer"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&type=consumer'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 3)
        
        # Verify all results are consumers
        for result in data['results']:
            self.assertEqual(result['type'], 'consumer')
    
    def test_filter_type_producer(self):
        """TC-ANA-24: Filter by type=producer"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&type=producer'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        
        # Verify all results are producers
        for result in data['results']:
            self.assertEqual(result['type'], 'producer')
    
    def test_filter_invalid_type(self):
        """TC-ANA-25: Filter with invalid type"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&type=invalid'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('type', data.get('message', data.get('error', '')).lower())
    
    def test_filter_by_keyword(self):
        """TC-ANA-26: Filter by keyword"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&keyword=.predict('
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
    
    def test_filter_by_library(self):
        """TC-ANA-27: Filter by library"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&library=tensorflow'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
    
    def test_filter_multiple_filters(self):
        """TC-ANA-28: Filter with multiple criteria (AND logic)"""
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&type=consumer&library=tensorflow'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        
        # Verify all results match both filters
        for result in data['results']:
            self.assertEqual(result['type'], 'consumer')
            # Handle both 'library' and 'libraries' field names
            library_value = result.get('library', result.get('libraries', ''))
            self.assertIn('tensorflow', library_value)
    
    def test_filter_limit_boundary(self):
        """TC-ANA-29: Filter with limit boundary"""
        # Create large dataset
        test_dir = tempfile.mkdtemp()
        
        large_data = []
        for i in range(1500):
            large_data.append({
                'ProjectName': f'Project{i}',
                'Is ML consumer': 'Yes',
                'where': f'file{i}.py',
                'keyword': '',
                'line_number': str(i),
                'libraries': 'tensorflow',
                'keywords': '.predict('
            })
        
        with open(os.path.join(test_dir, 'consumer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=large_data[0].keys())
            writer.writeheader()
            writer.writerows(large_data)
        
        with open(os.path.join(test_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            response = self.client.get(
                f'/api/analytics/filter?output_path={test_dir}&limit=1000'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertLessEqual(len(data['results']), 1000)
        finally:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)
    
    # TC-ANA-30: GET /api/analytics/health
    
    def test_health_check(self):
        """TC-ANA-30: Health check endpoint"""
        response = self.client.get('/api/analytics/health')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('Analytics API', data['service'])


if __name__ == '__main__':
    unittest.main()
