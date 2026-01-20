"""
Context Builder Service - Builds context from analysis results for LLM

Extracts and aggregates information from analyzed projects to create
rich context for LLM interactions.

As specified in CR3 LLM-Integration-Impact-Analysis.md
"""

import os
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)


class ContextBuilderService:
    """
    Service for building context from MARK analysis results.
    
    Extracts project metadata, analysis results, and code snippets to provide
    comprehensive context for LLM-based explanations and Q&A.
    """
    
    @staticmethod
    def extract_readme(project_path: str) -> Optional[str]:
        """
        Extract README content from project.
        
        Args:
            project_path: Path to analyzed project
            
        Returns:
            README content or None if not found
        """
        if not os.path.exists(project_path):
            return None
        
        # Try common README variations
        readme_names = ['README.md', 'README.MD', 'README.txt', 'README', 'readme.md']
        
        for readme_name in readme_names:
            readme_path = os.path.join(project_path, readme_name)
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Limit README size
                        if len(content) > 5000:
                            content = content[:5000] + "\n\n[... truncated ...]"
                        return content
                except Exception as e:
                    logger.error(f"Error reading README from {readme_path}: {e}")
                    return None
        
        return None
    
    @staticmethod
    def extract_dependencies(project_path: str) -> Dict[str, List[str]]:
        """
        Extract project dependencies from requirements files.
        
        Args:
            project_path: Path to analyzed project
            
        Returns:
            Dictionary with dependency lists
        """
        dependencies = {
            'requirements': [],
            'source': None
        }
        
        if not os.path.exists(project_path):
            return dependencies
        
        # Try requirements.txt
        req_path = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(req_path):
            try:
                with open(req_path, 'r', encoding='utf-8', errors='ignore') as f:
                    deps = [
                        line.strip() 
                        for line in f.readlines() 
                        if line.strip() and not line.startswith('#')
                    ]
                    dependencies['requirements'] = deps[:50]  # Limit to 50
                    dependencies['source'] = 'requirements.txt'
                    return dependencies
            except Exception as e:
                logger.error(f"Error reading requirements.txt: {e}")
        
        # Try setup.py
        setup_path = os.path.join(project_path, 'setup.py')
        if os.path.exists(setup_path):
            try:
                with open(setup_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Basic parsing - look for install_requires
                    if 'install_requires' in content:
                        dependencies['source'] = 'setup.py'
            except Exception as e:
                logger.error(f"Error reading setup.py: {e}")
        
        return dependencies
    
    @staticmethod
    def aggregate_analysis_results(producer_csv: str, consumer_csv: str) -> Dict:
        """
        Aggregate analysis results from Producer and Consumer CSVs.
        
        Args:
            producer_csv: Path to Producer CSV file
            consumer_csv: Path to Consumer CSV file
            
        Returns:
            Dictionary with aggregated statistics
        """
        results = {
            'producer': {
                'detected': False,
                'count': 0,
                'libraries': set(),
                'keywords': set(),
                'files': set()
            },
            'consumer': {
                'detected': False,
                'count': 0,
                'libraries': set(),
                'keywords': set(),
                'files': set()
            },
            'classification': 'Unknown'
        }
        
        # Parse Producer CSV
        if os.path.exists(producer_csv):
            try:
                with open(producer_csv, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results['producer']['count'] += 1
                        if 'libraries' in row and row['libraries']:
                            results['producer']['libraries'].add(row['libraries'])
                        if 'keywords' in row and row['keywords']:
                            results['producer']['keywords'].add(row['keywords'])
                        if 'where' in row and row['where']:
                            results['producer']['files'].add(row['where'])
                
                results['producer']['detected'] = results['producer']['count'] > 0
            except Exception as e:
                logger.error(f"Error parsing Producer CSV: {e}")
        
        # Parse Consumer CSV
        if os.path.exists(consumer_csv):
            try:
                with open(consumer_csv, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results['consumer']['count'] += 1
                        if 'libraries' in row and row['libraries']:
                            results['consumer']['libraries'].add(row['libraries'])
                        if 'keywords' in row and row['keywords']:
                            results['consumer']['keywords'].add(row['keywords'])
                        if 'where' in row and row['where']:
                            results['consumer']['files'].add(row['where'])
                
                results['consumer']['detected'] = results['consumer']['count'] > 0
            except Exception as e:
                logger.error(f"Error parsing Consumer CSV: {e}")
        
        # Determine classification
        if results['producer']['detected'] and results['consumer']['detected']:
            results['classification'] = 'Hybrid (Producer & Consumer)'
        elif results['producer']['detected']:
            results['classification'] = 'Producer'
        elif results['consumer']['detected']:
            results['classification'] = 'Consumer'
        
        # Convert sets to lists
        results['producer']['libraries'] = list(results['producer']['libraries'])
        results['producer']['keywords'] = list(results['producer']['keywords'])
        results['producer']['files'] = list(results['producer']['files'])
        results['consumer']['libraries'] = list(results['consumer']['libraries'])
        results['consumer']['keywords'] = list(results['consumer']['keywords'])
        results['consumer']['files'] = list(results['consumer']['files'])
        
        return results
    
    @staticmethod
    def extract_code_snippets(files: List[str], max_snippets: int = 3) -> List[Dict]:
        """
        Extract code snippets from files.
        
        Args:
            files: List of file paths
            max_snippets: Maximum number of snippets to extract
            
        Returns:
            List of snippet dictionaries
        """
        snippets = []
        
        for file_path in files[:max_snippets]:
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    # Extract first 10 lines
                    snippet_lines = lines[:10]
                    snippet = {
                        'file': file_path,
                        'lines': ''.join(snippet_lines),
                        'line_count': len(lines)
                    }
                    snippets.append(snippet)
            except Exception as e:
                logger.error(f"Error extracting snippet from {file_path}: {e}")
        
        return snippets
    
    @staticmethod
    def build_full_context(output_path: str, input_path: str) -> Dict:
        """
        Build complete analysis context for ALL analyzed projects.
        
        Args:
            output_path: Path to analysis results directory
            input_path: Path to input projects directory
            
        Returns:
            Dictionary with complete context for all projects
        """
        # Load analysis results from CSV files - USE ACTUAL PATHS FROM ANALYSIS TOOL
        producer_csv = os.path.join(output_path, 'Producers', 'Producers_Final', 'results_first_step.csv')
        consumer_csv = os.path.join(output_path, 'Consumers', 'Consumers_Final', 'results_consumer.csv')
        
        # Parse CSV files
        producer_detections = []
        consumer_detections = []
        
        if os.path.exists(producer_csv):
            try:
                with open(producer_csv, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    producer_detections = list(reader)
                    if producer_detections:
                        logger.info(f"Producer CSV columns: {list(producer_detections[0].keys())}")
            except Exception as e:
                logger.error(f"Error reading Producer CSV: {e}")
        
        if os.path.exists(consumer_csv):
            try:
                with open(consumer_csv, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    consumer_detections = list(reader)
                    if consumer_detections:
                        logger.info(f"Consumer CSV columns: {list(consumer_detections[0].keys())}")
            except Exception as e:
                logger.error(f"Error reading Consumer CSV: {e}")
        
        # Extract unique project names
        project_names = set()
        for detection in producer_detections + consumer_detections:
            if 'ProjectName' in detection and detection['ProjectName']:
                project_names.add(detection['ProjectName'])
        
        logger.info(f"Found {len(project_names)} unique projects")
        logger.info(f"Producer detections: {len(producer_detections)}")
        logger.info(f"Consumer detections: {len(consumer_detections)}")
        
        # Issue 2: Validate that we have actual data before proceeding
        if len(project_names) == 0:
            error_msg = f"No projects found in analysis results. Checked paths:\n" \
                       f"  Producer CSV: {producer_csv} (exists: {os.path.exists(producer_csv)})\n" \
                       f"  Consumer CSV: {consumer_csv} (exists: {os.path.exists(consumer_csv)})"
            logger.error(error_msg)
            raise ValueError("No analysis results found. Please run the analysis first before using LLM features.")
        
        # Build context for all projects
        projects = []
        for project_name in sorted(project_names):
            # Filter detections for this project
            proj_producer = [d for d in producer_detections if d.get('ProjectName') == project_name]
            proj_consumer = [d for d in consumer_detections if d.get('ProjectName') == project_name]
            
            # Count detections for this project
            prod_count = len(proj_producer)
            cons_count = len(proj_consumer)
            
            # Determine classification
            if prod_count > 0 and cons_count > 0:
                classification = 'Hybrid (Producer & Consumer)'
            elif prod_count > 0:
                classification = 'Producer'
            elif cons_count > 0:
                classification = 'Consumer'
            else:
                classification = 'Unknown'
            
            # Get libraries and keywords
            libraries = set()
            keywords = set()
            for d in proj_producer + proj_consumer:
                if d.get('libraries'):
                    libraries.add(d['libraries'])
                if d.get('keywords'):
                    keywords.add(d['keywords'])
            
            projects.append({
                'project_name': project_name,
                'classification': classification,
                'producer_count': prod_count,
                'consumer_count': cons_count,
                'total_detections': prod_count + cons_count,
                'libraries': sorted(list(libraries)),
                'keywords': sorted(list(keywords))[:20]  # Limit
            })
        
        # Build overall context
        context = {
            'total_projects': len(projects),
            'output_path': output_path,
            'input_path': input_path,
            'projects': projects,
            'producer_count': len([p for p in projects if 'Producer' in p['classification']]),
            'consumer_count': len([p for p in projects if 'Consumer' in p['classification']]),
            'hybrid_count': len([p for p in projects if 'Hybrid' in p['classification']])
        }
        
        logger.info(f"Built context for {len(projects)} projects")
        
        return context
    
    @staticmethod
    def format_context_for_llm(context: Dict) -> str:
        """
        Format context dictionary into readable text for LLM.
        
        Args:
            context: Context dictionary from build_full_context
            
        Returns:
            Formatted text context
        """
        lines = []
        
        lines.append("=" * 80)
        lines.append("MARK ANALYSIS RESULTS - MULTIPLE PROJECTS")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Total projects analyzed: {context['total_projects']}")
        lines.append(f"Producers: {context['producer_count']}")
        lines.append(f"Consumers: {context['consumer_count']}")
        lines.append(f"Hybrid: {context['hybrid_count']}")
        lines.append("")
        lines.append("PROJECTS LIST:")
        lines.append("-" * 80)
        
        for idx, project in enumerate(context['projects'], 1):
            lines.append(f"\n{idx}. {project['project_name']}")
            lines.append(f"   Classification: {project['classification']}")
            lines.append(f"   Libraries: {', '.join(project['libraries'][:5])}")
            lines.append(f"   Total detections: {project['total_detections']}")
            if project['producer_count'] > 0:
                lines.append(f"   Producer detections: {project['producer_count']}")
            if project['consumer_count'] > 0:
                lines.append(f"   Consumer detections: {project['consumer_count']}")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("You can ask questions about any of these projects.")
        lines.append("=" * 80)
        
        return '\n'.join(lines)
