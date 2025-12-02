"""
Integration tests for Analytics functionality
Tests end-to-end workflows combining multiple components
"""
import os
import sys
import unittest
import tempfile
import csv
import time
from pathlib import Path

# Add web_gui directory to path
web_gui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'web_gui'))
sys.path.insert(0, web_gui_path)
sys.path.insert(0, os.path.dirname(web_gui_path))

import web_gui.app as web_app
app = web_app.create_app('testing')


class TestAnalyticsIntegration(unittest.TestCase):
    """Integration test cases for Analytics workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Create realistic sample data
        self.consumer_data = [
            {
                'ProjectName': 'MLProject1',
                'Is ML consumer': 'Yes',
                'where': 'src/inference.py',
                'keyword': '',
                'line_number': '15',
                'libraries': 'tensorflow',
                'keywords': '.predict('
            },
            {
                'ProjectName': 'MLProject1',
                'Is ML consumer': 'Yes',
                'where': 'src/evaluate.py',
                'keyword': '',
                'line_number': '25',
                'libraries': 'tensorflow',
                'keywords': '.evaluate('
            },
            {
                'ProjectName': 'MLProject2',
                'Is ML consumer': 'Yes',
                'where': 'inference/model.py',
                'keyword': '',
                'line_number': '42',
                'libraries': 'torch',
                'keywords': '.no_grad('
            },
        ]
        
        self.producer_data = [
            {
                'ProjectName': 'MLProject1',
                'Is ML producer': 'Yes',
                'where': 'src/training.py',
                'keyword': '',
                'line_number': '100',
                'libraries': 'tensorflow',
                'keywords': '.fit('
            },
            {
                'ProjectName': 'MLProject3',
                'Is ML producer': 'Yes',
                'where': 'train/main.py',
                'keyword': '',
                'line_number': '50',
                'libraries': 'sklearn',
                'keywords': '.fit('
            },
        ]
        
        # Write CSV files
        consumer_path = os.path.join(self.test_dir, 'consumer.csv')
        with open(consumer_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.consumer_data[0].keys())
            writer.writeheader()
            writer.writerows(self.consumer_data)
        
        producer_path = os.path.join(self.test_dir, 'producer.csv')
        with open(producer_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.producer_data[0].keys())
            writer.writeheader()
            writer.writerows(self.producer_data)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_complete_analytics_workflow(self):
        """TC-INT-ANA-01: Complete analytics workflow end-to-end"""
        # Step 1: Get summary
        response = self.client.get(f'/api/analytics/summary?output_path={self.test_dir}')
        self.assertEqual(response.status_code, 200)
        summary = response.get_json()
        
        # Verify summary data is coherent
        self.assertEqual(summary['total_models'], 5)
        self.assertEqual(summary['consumer_count'], 3)
        self.assertEqual(summary['producer_count'], 2)
        self.assertIn('last_analysis_id', summary)
        
        # Step 2: Get distribution
        response = self.client.get(
            f'/api/analytics/consumer-producer-distribution?output_path={self.test_dir}'
        )
        self.assertEqual(response.status_code, 200)
        distribution = response.get_json()
        
        # Verify distribution percentages sum to 100
        percentages = distribution['percentages']
        self.assertAlmostEqual(sum(percentages), 100.0, places=1)
        
        # Verify counts match summary
        self.assertEqual(distribution['counts'][0], summary['consumer_count'])
        self.assertEqual(distribution['counts'][1], summary['producer_count'])
        
        # Step 3: Verify data consistency
        self.assertEqual(
            distribution['counts'][0] + distribution['counts'][1],
            summary['total_models']
        )
    
    def test_filter_and_visualization_workflow(self):
        """TC-INT-ANA-02: Filter and visualization workflow"""
        # Step 1: Get top keywords
        response = self.client.get(
            f'/api/analytics/keywords?output_path={self.test_dir}&limit=10'
        )
        self.assertEqual(response.status_code, 200)
        keywords_data = response.get_json()
        
        self.assertTrue(keywords_data['success'])
        self.assertGreater(len(keywords_data['labels']), 0)
        
        # Step 2: Use first keyword to filter results
        first_keyword = keywords_data['labels'][0]
        response = self.client.get(
            f'/api/analytics/filter?output_path={self.test_dir}&keyword={first_keyword}'
        )
        self.assertEqual(response.status_code, 200)
        filtered_data = response.get_json()
        
        self.assertTrue(filtered_data['success'])
        
        # Step 3: Verify all results contain the keyword
        for result in filtered_data['results']:
            self.assertIn(first_keyword, result.get('keywords', ''))
        
        # Step 4: Verify count consistency
        keyword_count = keywords_data['counts'][keywords_data['labels'].index(first_keyword)]
        self.assertEqual(filtered_data['count'], keyword_count)
    
    def test_empty_dataset_handling(self):
        """TC-INT-ANA-03: End-to-end handling of empty dataset"""
        # Create empty dataset
        empty_dir = tempfile.mkdtemp()
        
        with open(os.path.join(empty_dir, 'consumer.csv'), 'w') as f:
            f.write('ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords\n')
        
        with open(os.path.join(empty_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            # Test all analytics endpoints with empty data
            
            # 1. Summary
            response = self.client.get(f'/api/analytics/summary?output_path={empty_dir}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['total_models'], 0)
            
            # 2. Distribution
            response = self.client.get(
                f'/api/analytics/consumer-producer-distribution?output_path={empty_dir}'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['counts'], [0, 0])
            
            # 3. Keywords
            response = self.client.get(
                f'/api/analytics/keywords?output_path={empty_dir}'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['labels'], [])
            
            # 4. Libraries
            response = self.client.get(
                f'/api/analytics/libraries?output_path={empty_dir}'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['labels'], [])
            
            # 5. Filter
            response = self.client.get(
                f'/api/analytics/filter?output_path={empty_dir}'
            )
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['count'], 0)
            
            # Verify no 500 errors occurred
            self.assertNotEqual(response.status_code, 500)
            
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_large_dataset_performance(self):
        """TC-INT-ANA-04: Performance test with large dataset"""
        # Create large dataset
        large_dir = tempfile.mkdtemp()
        
        # Generate 1000+ consumer entries
        large_consumer_data = []
        for i in range(1000):
            large_consumer_data.append({
                'ProjectName': f'Project{i % 50}',  # 50 unique projects
                'Is ML consumer': 'Yes',
                'where': f'src/file{i}.py',
                'keyword': '',
                'line_number': str(i * 10),
                'libraries': f'lib{i % 20}',  # 20 unique libraries
                'keywords': f'.method{i % 100}('  # 100 unique keywords
            })
        
        # Generate 200 producer entries
        large_producer_data = []
        for i in range(200):
            large_producer_data.append({
                'ProjectName': f'Project{i % 50}',
                'Is ML producer': 'Yes',
                'where': f'train/file{i}.py',
                'keyword': '',
                'line_number': str(i * 10),
                'libraries': f'lib{i % 20}',
                'keywords': f'.train{i % 50}('
            })
        
        # Write large CSV files
        with open(os.path.join(large_dir, 'consumer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=large_consumer_data[0].keys())
            writer.writeheader()
            writer.writerows(large_consumer_data)
        
        with open(os.path.join(large_dir, 'producer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=large_producer_data[0].keys())
            writer.writeheader()
            writer.writerows(large_producer_data)
        
        try:
            # Test performance of each endpoint
            endpoints = [
                f'/api/analytics/summary?output_path={large_dir}',
                f'/api/analytics/consumer-producer-distribution?output_path={large_dir}',
                f'/api/analytics/keywords?output_path={large_dir}&limit=50',
                f'/api/analytics/libraries?output_path={large_dir}&limit=50',
                f'/api/analytics/filter?output_path={large_dir}&limit=100',
            ]
            
            for endpoint in endpoints:
                start_time = time.time()
                response = self.client.get(endpoint)
                elapsed_time = time.time() - start_time
                
                # Verify response is successful
                self.assertEqual(response.status_code, 200)
                
                # Verify response time < 2 seconds
                self.assertLess(elapsed_time, 2.0, 
                    f"Endpoint {endpoint} took {elapsed_time:.2f}s, expected < 2s")
            
        finally:
            import shutil
            shutil.rmtree(large_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
