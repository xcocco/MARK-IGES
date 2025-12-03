"""
Unit tests for AnalyticsService
"""
import os
import sys
import unittest
import tempfile
import csv
from pathlib import Path

# Add web_gui directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'web_gui')))

from services.analytics_service import AnalyticsService


class TestAnalyticsService(unittest.TestCase):
    """Test cases for AnalyticsService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = AnalyticsService()
        
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
        # Remove temporary directory and files
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_validate_output_path_valid(self):
        """Test validate_output_path with valid path"""
        is_valid, message = self.service.validate_output_path(self.test_dir)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Output path is valid")
    
    def test_validate_output_path_invalid(self):
        """Test validate_output_path with invalid path"""
        is_valid, message = self.service.validate_output_path('/nonexistent/path')
        self.assertFalse(is_valid)
        self.assertIn('does not exist', message)
    
    def test_get_summary(self):
        """Test get_summary method"""
        summary = self.service.get_summary(self.test_dir)
        
        self.assertTrue(summary['success'])
        self.assertEqual(summary['consumer_count'], 3)
        self.assertEqual(summary['producer_count'], 2)
        self.assertEqual(summary['total_models'], 5)
        self.assertEqual(summary['total_projects'], 3)  # TestProject1, TestProject2, TestProject3
        self.assertEqual(summary['total_libraries'], 4)  # tensorflow, torch, sklearn, keras
    
    def test_get_consumer_producer_distribution(self):
        """Test get_consumer_producer_distribution method"""
        distribution = self.service.get_consumer_producer_distribution(self.test_dir)
        
        self.assertTrue(distribution['success'])
        self.assertEqual(distribution['labels'], ['Consumer', 'Producer'])
        self.assertEqual(distribution['counts'], [3, 2])
        self.assertEqual(distribution['percentages'], [60.0, 40.0])
    
    def test_get_top_keywords(self):
        """Test get_top_keywords method"""
        keywords = self.service.get_top_keywords(self.test_dir, limit=10)
        
        self.assertTrue(keywords['success'])
        self.assertGreater(len(keywords['labels']), 0)
        self.assertIn('.predict(', keywords['labels'])
        self.assertEqual(keywords['counts'][keywords['labels'].index('.predict(')], 2)
    
    def test_get_library_distribution(self):
        """Test get_library_distribution method"""
        libraries = self.service.get_library_distribution(self.test_dir, limit=10)
        
        self.assertTrue(libraries['success'])
        self.assertGreater(len(libraries['labels']), 0)
        self.assertIn('tensorflow', libraries['labels'])
    
    def test_get_filtered_results_by_type(self):
        """Test get_filtered_results by type"""
        results = self.service.get_filtered_results(
            self.test_dir,
            filter_type='consumer'
        )
        
        self.assertTrue(results['success'])
        self.assertEqual(results['count'], 3)
        self.assertEqual(results['filters_applied']['type'], 'consumer')
    
    def test_get_filtered_results_by_keyword(self):
        """Test get_filtered_results by keyword"""
        results = self.service.get_filtered_results(
            self.test_dir,
            keyword='.predict('
        )
        
        self.assertTrue(results['success'])
        self.assertEqual(results['count'], 2)
    
    def test_get_filtered_results_by_library(self):
        """Test get_filtered_results by library"""
        results = self.service.get_filtered_results(
            self.test_dir,
            library='tensorflow'
        )
        
        self.assertTrue(results['success'])
        self.assertEqual(results['count'], 2)
    
    def test_empty_csv_handling(self):
        """Test handling of empty CSV files"""
        empty_dir = tempfile.mkdtemp()
        
        # Create empty CSV files
        with open(os.path.join(empty_dir, 'consumer.csv'), 'w') as f:
            f.write('ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords\n')
        
        with open(os.path.join(empty_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        summary = self.service.get_summary(empty_dir)
        
        self.assertTrue(summary['success'])
        self.assertEqual(summary['total_models'], 0)
        self.assertEqual(summary['consumer_count'], 0)
        self.assertEqual(summary['producer_count'], 0)
        
        # Clean up
        import shutil
        shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_validate_output_path_not_directory(self):
        """TC-AS-03: Test validate_output_path with non-directory path"""
        # Create a temporary file (not directory)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        
        try:
            is_valid, message = self.service.validate_output_path(temp_file.name)
            self.assertFalse(is_valid)
            self.assertIn('not a directory', message)
        finally:
            os.unlink(temp_file.name)
    
    def test_validate_output_path_missing_csv(self):
        """TC-AS-04: Test validate_output_path with directory missing CSV files"""
        empty_dir = tempfile.mkdtemp()
        
        try:
            is_valid, message = self.service.validate_output_path(empty_dir)
            self.assertFalse(is_valid)
            self.assertIn('consumer.csv', message.lower())
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_get_summary_unique_projects(self):
        """TC-AS-06: Test get_summary counts unique projects correctly"""
        summary = self.service.get_summary(self.test_dir)
        
        # We have TestProject1 appearing in both consumer and producer
        # TestProject2 only in consumer, TestProject3 only in producer
        self.assertTrue(summary['success'])
        self.assertEqual(summary['total_projects'], 3)
    
    def test_get_summary_unique_libraries(self):
        """TC-AS-07: Test get_summary counts unique libraries correctly"""
        summary = self.service.get_summary(self.test_dir)
        
        # Libraries: tensorflow (appears twice in consumer), torch, sklearn, keras
        self.assertTrue(summary['success'])
        self.assertEqual(summary['total_libraries'], 4)
    
    def test_get_consumer_producer_distribution_empty(self):
        """TC-AS-09: Test distribution with empty dataset"""
        empty_dir = tempfile.mkdtemp()
        
        # Create empty CSV files
        with open(os.path.join(empty_dir, 'consumer.csv'), 'w') as f:
            f.write('ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords\n')
        
        with open(os.path.join(empty_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            distribution = self.service.get_consumer_producer_distribution(empty_dir)
            
            self.assertTrue(distribution['success'])
            self.assertEqual(distribution['counts'], [0, 0])
            self.assertEqual(distribution['percentages'], [0.0, 0.0])
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_get_top_keywords_limit_respected(self):
        """TC-AS-11: Test get_top_keywords respects limit parameter"""
        # Create directory with many keywords
        test_dir = tempfile.mkdtemp()
        
        keywords_data = []
        for i in range(20):
            keywords_data.append({
                'ProjectName': f'Project{i}',
                'Is ML consumer': 'Yes',
                'where': f'file{i}.py',
                'keyword': '',
                'line_number': str(i),
                'libraries': 'lib',
                'keywords': f'.method{i}('
            })
        
        with open(os.path.join(test_dir, 'consumer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keywords_data[0].keys())
            writer.writeheader()
            writer.writerows(keywords_data)
        
        with open(os.path.join(test_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            keywords = self.service.get_top_keywords(test_dir, limit=10)
            
            self.assertTrue(keywords['success'])
            self.assertLessEqual(len(keywords['labels']), 10)
        finally:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)
    
    def test_get_top_keywords_empty_dataset(self):
        """TC-AS-12: Test get_top_keywords with empty dataset"""
        empty_dir = tempfile.mkdtemp()
        
        with open(os.path.join(empty_dir, 'consumer.csv'), 'w') as f:
            f.write('ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords\n')
        
        with open(os.path.join(empty_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            keywords = self.service.get_top_keywords(empty_dir, limit=10)
            
            self.assertTrue(keywords['success'])
            self.assertEqual(keywords['labels'], [])
            self.assertEqual(keywords['counts'], [])
            self.assertEqual(keywords['total_unique_keywords'], 0)
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
    
    def test_get_library_distribution_limit_respected(self):
        """TC-AS-14: Test get_library_distribution respects limit parameter"""
        # Create directory with many libraries
        test_dir = tempfile.mkdtemp()
        
        lib_data = []
        for i in range(15):
            lib_data.append({
                'ProjectName': f'Project{i}',
                'Is ML consumer': 'Yes',
                'where': f'file{i}.py',
                'keyword': '',
                'line_number': str(i),
                'libraries': f'library{i}',
                'keywords': '.method('
            })
        
        with open(os.path.join(test_dir, 'consumer.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=lib_data[0].keys())
            writer.writeheader()
            writer.writerows(lib_data)
        
        with open(os.path.join(test_dir, 'producer.csv'), 'w') as f:
            f.write('ProjectName,Is ML producer,where,keyword,line_number,libraries,keywords\n')
        
        try:
            libraries = self.service.get_library_distribution(test_dir, limit=10)
            
            self.assertTrue(libraries['success'])
            self.assertLessEqual(len(libraries['labels']), 10)
        finally:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)
    
    def test_get_filtered_results_by_type_producer(self):
        """TC-AS-16: Test get_filtered_results filters producer type correctly"""
        results = self.service.get_filtered_results(
            self.test_dir,
            filter_type='producer'
        )
        
        self.assertTrue(results['success'])
        self.assertEqual(results['count'], 2)
        self.assertEqual(results['filters_applied']['type'], 'producer')
        
        # Verify all results are producers
        for result in results['results']:
            self.assertEqual(result.get('type'), 'producer')
    
    def test_get_filtered_results_multiple_filters(self):
        """TC-AS-19: Test get_filtered_results with multiple filters (AND logic)"""
        results = self.service.get_filtered_results(
            self.test_dir,
            filter_type='consumer',
            library='tensorflow'
        )
        
        self.assertTrue(results['success'])
        self.assertEqual(results['count'], 2)
        self.assertEqual(results['filters_applied']['type'], 'consumer')
        self.assertEqual(results['filters_applied']['library'], 'tensorflow')
        
        # Verify all results match both filters
        for result in results['results']:
            self.assertEqual(result.get('type'), 'consumer')
            # Library field might be named 'libraries' in the result
            self.assertIn('tensorflow', result.get('library', result.get('libraries', '')))
    
    def test_get_filtered_results_limit_respected(self):
        """TC-AS-20: Test get_filtered_results respects limit parameter"""
        # Create directory with many results
        test_dir = tempfile.mkdtemp()
        
        large_data = []
        for i in range(200):
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
            results = self.service.get_filtered_results(test_dir, limit=50)
            
            self.assertTrue(results['success'])
            self.assertLessEqual(len(results['results']), 50)
        finally:
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
