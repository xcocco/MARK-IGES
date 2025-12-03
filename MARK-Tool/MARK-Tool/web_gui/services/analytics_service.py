"""
Analytics Service - Handles data aggregation and analytics for MARK results
"""
import os
import csv
import glob
from typing import Dict, List, Tuple, Optional
from collections import Counter
from datetime import datetime


class AnalyticsService:
    """Service for analyzing and aggregating MARK analysis results"""
    
    def __init__(self):
        """Initialize the analytics service"""
        self.consumer_csv = 'consumer.csv'
        self.producer_csv = 'producer.csv'
    
    def get_summary(self, output_path: str) -> Dict:
        """
        Get a summary of the analysis results
        
        Args:
            output_path: Path to the output folder containing results
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            consumer_data = self._load_csv(output_path, self.consumer_csv)
            producer_data = self._load_csv(output_path, self.producer_csv)
            
            consumer_count = len(consumer_data)
            producer_count = len(producer_data)
            total_models = consumer_count + producer_count
            
            # Get unique projects
            consumer_projects = set(row['ProjectName'] for row in consumer_data if 'ProjectName' in row)
            producer_projects = set(row['ProjectName'] for row in producer_data if 'ProjectName' in row)
            all_projects = consumer_projects.union(producer_projects)
            
            # Get unique libraries
            consumer_libs = set(row['libraries'] for row in consumer_data if 'libraries' in row and row['libraries'])
            producer_libs = set(row['libraries'] for row in producer_data if 'libraries' in row and row['libraries'])
            all_libraries = consumer_libs.union(producer_libs)
            
            # Get last analysis timestamp (use folder modification time as proxy)
            last_analysis_id = None
            if os.path.exists(output_path):
                last_modified = os.path.getmtime(output_path)
                last_analysis_id = datetime.fromtimestamp(last_modified).isoformat()
            
            return {
                'success': True,
                'total_models': total_models,
                'consumer_count': consumer_count,
                'producer_count': producer_count,
                'total_projects': len(all_projects),
                'total_libraries': len(all_libraries),
                'last_analysis_id': last_analysis_id,
                'output_path': output_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate summary'
            }
    
    def get_consumer_producer_distribution(self, output_path: str) -> Dict:
        """
        Get the distribution of consumer and producer models
        
        Args:
            output_path: Path to the output folder containing results
            
        Returns:
            Dictionary with labels, counts, and percentages
        """
        try:
            consumer_data = self._load_csv(output_path, self.consumer_csv)
            producer_data = self._load_csv(output_path, self.producer_csv)
            
            consumer_count = len(consumer_data)
            producer_count = len(producer_data)
            total = consumer_count + producer_count
            
            if total == 0:
                return {
                    'success': True,
                    'labels': ['Consumer', 'Producer'],
                    'counts': [0, 0],
                    'percentages': [0.0, 0.0]
                }
            
            consumer_pct = (consumer_count / total) * 100
            producer_pct = (producer_count / total) * 100
            
            return {
                'success': True,
                'labels': ['Consumer', 'Producer'],
                'counts': [consumer_count, producer_count],
                'percentages': [round(consumer_pct, 2), round(producer_pct, 2)]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate distribution'
            }
    
    def get_top_keywords(self, output_path: str, limit: int = 10) -> Dict:
        """
        Get the top N keywords used in classification
        
        Args:
            output_path: Path to the output folder containing results
            limit: Maximum number of keywords to return
            
        Returns:
            Dictionary with labels and counts
        """
        try:
            consumer_data = self._load_csv(output_path, self.consumer_csv)
            producer_data = self._load_csv(output_path, self.producer_csv)
            
            # Collect all keywords
            all_keywords = []
            
            for row in consumer_data:
                if 'keywords' in row and row['keywords']:
                    # Keywords might be stored with or without leading dot
                    keyword = row['keywords'].strip()
                    if keyword:
                        all_keywords.append(keyword)
            
            for row in producer_data:
                if 'keywords' in row and row['keywords']:
                    keyword = row['keywords'].strip()
                    if keyword:
                        all_keywords.append(keyword)
            
            # Count keyword occurrences
            keyword_counter = Counter(all_keywords)
            
            # Get top N keywords
            top_keywords = keyword_counter.most_common(limit)
            
            if not top_keywords:
                return {
                    'success': True,
                    'labels': [],
                    'counts': [],
                    'total_unique_keywords': 0
                }
            
            labels = [kw[0] for kw in top_keywords]
            counts = [kw[1] for kw in top_keywords]
            
            return {
                'success': True,
                'labels': labels,
                'counts': counts,
                'total_unique_keywords': len(keyword_counter)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate keywords distribution'
            }
    
    def get_library_distribution(self, output_path: str, limit: int = 10) -> Dict:
        """
        Get the distribution of libraries used
        
        Args:
            output_path: Path to the output folder containing results
            limit: Maximum number of libraries to return
            
        Returns:
            Dictionary with labels and counts
        """
        try:
            consumer_data = self._load_csv(output_path, self.consumer_csv)
            producer_data = self._load_csv(output_path, self.producer_csv)
            
            # Collect all libraries
            all_libraries = []
            
            for row in consumer_data:
                if 'libraries' in row and row['libraries']:
                    lib = row['libraries'].strip()
                    if lib:
                        all_libraries.append(lib)
            
            for row in producer_data:
                if 'libraries' in row and row['libraries']:
                    lib = row['libraries'].strip()
                    if lib:
                        all_libraries.append(lib)
            
            # Count library occurrences
            library_counter = Counter(all_libraries)
            
            # Get top N libraries
            top_libraries = library_counter.most_common(limit)
            
            if not top_libraries:
                return {
                    'success': True,
                    'labels': [],
                    'counts': [],
                    'total_unique_libraries': 0
                }
            
            labels = [lib[0] for lib in top_libraries]
            counts = [lib[1] for lib in top_libraries]
            
            return {
                'success': True,
                'labels': labels,
                'counts': counts,
                'total_unique_libraries': len(library_counter)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate library distribution'
            }
    
    def get_filtered_results(self, output_path: str, filter_type: Optional[str] = None, 
                           keyword: Optional[str] = None, library: Optional[str] = None,
                           project: Optional[str] = None, limit: int = 100) -> Dict:
        """
        Get filtered results based on type, keyword, library, or project
        
        Args:
            output_path: Path to the output folder containing results
            filter_type: Filter by type ('consumer' or 'producer')
            keyword: Filter by specific keyword
            library: Filter by specific library
            project: Filter by specific project name
            limit: Maximum number of results to return
            
        Returns:
            Dictionary with filtered results
        """
        try:
            results = []
            
            # Determine which CSV files to load
            if filter_type == 'consumer':
                data = self._load_csv(output_path, self.consumer_csv)
                for row in data:
                    row['type'] = 'consumer'
                results.extend(data)
            elif filter_type == 'producer':
                data = self._load_csv(output_path, self.producer_csv)
                for row in data:
                    row['type'] = 'producer'
                results.extend(data)
            else:
                # Load both
                consumer_data = self._load_csv(output_path, self.consumer_csv)
                producer_data = self._load_csv(output_path, self.producer_csv)
                
                for row in consumer_data:
                    row['type'] = 'consumer'
                results.extend(consumer_data)
                
                for row in producer_data:
                    row['type'] = 'producer'
                results.extend(producer_data)
            
            # Apply filters
            if keyword:
                results = [r for r in results if 'keywords' in r and keyword in r['keywords']]
            
            if library:
                results = [r for r in results if 'libraries' in r and library in r['libraries']]
            
            if project:
                results = [r for r in results if 'ProjectName' in r and project in r['ProjectName']]
            
            # Limit results
            results = results[:limit]
            
            return {
                'success': True,
                'count': len(results),
                'results': results,
                'filters_applied': {
                    'type': filter_type,
                    'keyword': keyword,
                    'library': library,
                    'project': project
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to filter results'
            }
    
    def _load_csv(self, output_path: str, filename: str) -> List[Dict]:
        """
        Load a CSV file from the output path
        
        Args:
            output_path: Path to the output folder
            filename: Name of the CSV file (e.g., 'consumer.csv' or 'producer.csv')
            
        Returns:
            List of dictionaries (rows)
        """
        # First try direct path
        file_path = os.path.join(output_path, filename)
        
        if not os.path.exists(file_path):
            # Search for the file in subdirectories
            file_path = self._find_csv_file(output_path, filename)
            if not file_path:
                return []
        
        data = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error loading CSV {filename}: {str(e)}")
            return []
        
        return data
    
    def _find_csv_file(self, output_path: str, filename: str) -> Optional[str]:
        """
        Search for CSV file in subdirectories
        
        Args:
            output_path: Root path to search
            filename: Filename pattern to search for (e.g., 'consumer.csv')
            
        Returns:
            Full path to the file if found, None otherwise
        """
        # Determine search pattern based on filename
        if 'consumer' in filename.lower():
            # Look for consumer-related files
            search_patterns = ['consumer.csv', '*consumer*.csv', 'results_consumer.csv']
            search_dirs = ['Consumers', 'Consumers_Final', 'Consumer']
        elif 'producer' in filename.lower():
            # Look for producer-related files
            search_patterns = ['producer.csv', '*producer*.csv', 'results_producer.csv']
            search_dirs = ['Producers', 'Producers_Final', 'Producer']
        else:
            search_patterns = [filename]
            search_dirs = []
        
        # First, check common subdirectories
        for subdir in search_dirs:
            subdir_path = os.path.join(output_path, subdir)
            if os.path.exists(subdir_path):
                # Check direct match in subdirectory
                for pattern in search_patterns:
                    if '*' in pattern:
                        # Use glob for wildcard patterns
                        matches = glob.glob(os.path.join(subdir_path, pattern))
                        if matches:
                            # Return the first match (prefer exact names)
                            return matches[0]
                    else:
                        file_path = os.path.join(subdir_path, pattern)
                        if os.path.exists(file_path):
                            return file_path
                
                # Check subdirectories within this directory
                for root, dirs, files in os.walk(subdir_path):
                    for pattern in search_patterns:
                        if '*' in pattern:
                            matches = glob.glob(os.path.join(root, pattern))
                            if matches:
                                return matches[0]
                        elif pattern in files:
                            return os.path.join(root, pattern)
        
        # If not found in specific directories, do a full recursive search
        for root, dirs, files in os.walk(output_path):
            for pattern in search_patterns:
                if '*' in pattern:
                    matches = glob.glob(os.path.join(root, pattern))
                    if matches:
                        return matches[0]
                elif pattern in files:
                    return os.path.join(root, pattern)
        
        return None
    
    def validate_output_path(self, output_path: str) -> Tuple[bool, str]:
        """
        Validate that the output path exists and contains the necessary CSV files
        
        Args:
            output_path: Path to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not output_path:
            return False, "Output path is required"
        
        if not os.path.exists(output_path):
            return False, f"Output path does not exist: {output_path}"
        
        if not os.path.isdir(output_path):
            return False, f"Output path is not a directory: {output_path}"
        
        # Check for at least one CSV file (direct or in subdirectories)
        consumer_path = os.path.join(output_path, self.consumer_csv)
        producer_path = os.path.join(output_path, self.producer_csv)
        
        has_consumer = os.path.exists(consumer_path) or self._find_csv_file(output_path, self.consumer_csv) is not None
        has_producer = os.path.exists(producer_path) or self._find_csv_file(output_path, self.producer_csv) is not None
        
        if not has_consumer and not has_producer:
            return False, f"No {self.consumer_csv} or {self.producer_csv} files found in output path or its subdirectories"
        
        return True, "Output path is valid"
