"""
Context Builder Service - Extracts project context for LLM analysis

This service extracts relevant information from analyzed projects to provide
context to the LLM, including README files, dependencies, and analysis results.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import csv
import re


logger = logging.getLogger(__name__)


class ContextBuilderService:
    """
    Service for building context from analyzed projects for LLM consumption.
    
    Extracts:
    - README content
    - Dependencies (requirements.txt, pyproject.toml, setup.py)
    - Analysis results (Producer/Consumer CSV)
    - Code snippets with detected keywords
    """
    
    @staticmethod
    def extract_readme(project_path: str) -> str:
        """
        Extract README content from project.
        
        Args:
            project_path: Absolute path to project root
            
        Returns:
            README content or empty string if not found
        """
        readme_patterns = [
            'README.md', 'README.MD', 'readme.md',
            'README.txt', 'README.rst', 'README'
        ]
        
        try:
            for pattern in readme_patterns:
                readme_path = os.path.join(project_path, pattern)
                if os.path.isfile(readme_path):
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        logger.info(f"README found: {readme_path}")
                        return content[:5000]  # Limit to 5000 chars
            
            logger.warning(f"No README found in {project_path}")
            return ""
            
        except Exception as e:
            logger.error(f"Error reading README: {e}")
            return ""
    
    @staticmethod
    def extract_dependencies(project_path: str) -> Dict[str, List[str]]:
        """
        Extract project dependencies from various files.
        
        Args:
            project_path: Absolute path to project root
            
        Returns:
            Dictionary with dependency sources and their contents
        """
        dependencies = {}
        
        # Check requirements.txt
        req_path = os.path.join(project_path, 'requirements.txt')
        if os.path.isfile(req_path):
            try:
                with open(req_path, 'r', encoding='utf-8', errors='ignore') as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    dependencies['requirements.txt'] = deps
                    logger.info(f"Found {len(deps)} dependencies in requirements.txt")
            except Exception as e:
                logger.error(f"Error reading requirements.txt: {e}")
        
        # Check setup.py
        setup_path = os.path.join(project_path, 'setup.py')
        if os.path.isfile(setup_path):
            try:
                with open(setup_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Simple regex to extract install_requires
                    match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                    if match:
                        deps_str = match.group(1)
                        deps = [d.strip().strip('"\'') for d in deps_str.split(',') if d.strip()]
                        dependencies['setup.py'] = deps
                        logger.info(f"Found {len(deps)} dependencies in setup.py")
            except Exception as e:
                logger.error(f"Error reading setup.py: {e}")
        
        # Check pyproject.toml
        pyproject_path = os.path.join(project_path, 'pyproject.toml')
        if os.path.isfile(pyproject_path):
            try:
                with open(pyproject_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Simple extraction of dependencies section
                    match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                    if match:
                        deps_str = match.group(1)
                        deps = [d.strip().strip('"\'') for d in deps_str.split(',') if d.strip()]
                        dependencies['pyproject.toml'] = deps
                        logger.info(f"Found {len(deps)} dependencies in pyproject.toml")
            except Exception as e:
                logger.error(f"Error reading pyproject.toml: {e}")
        
        return dependencies
    
    @staticmethod
    def aggregate_analysis_results(producer_csv: str, consumer_csv: str) -> Dict:
        """
        Aggregate analysis results from Producer and Consumer CSV files.
        
        Args:
            producer_csv: Path to producer results CSV
            consumer_csv: Path to consumer results CSV
            
        Returns:
            Dictionary with aggregated statistics and details
        """
        result = {
            'is_producer': False,
            'is_consumer': False,
            'producer_files': [],
            'consumer_files': [],
            'producer_keywords': [],
            'consumer_keywords': [],
            'libraries': set(),
            'total_detections': 0
        }
        
        # Read Producer CSV
        if os.path.isfile(producer_csv):
            try:
                with open(producer_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Is ML producer', '').lower() == 'yes':
                            result['is_producer'] = True
                            result['producer_files'].append({
                                'file': row.get('where', ''),
                                'keyword': row.get('keywords', ''),
                                'line': row.get('line_number', ''),
                                'library': row.get('libraries', '')
                            })
                            result['producer_keywords'].append(row.get('keywords', ''))
                            if row.get('libraries'):
                                result['libraries'].add(row.get('libraries'))
                            result['total_detections'] += 1
                
                logger.info(f"Producer results: {len(result['producer_files'])} detections")
            except Exception as e:
                logger.error(f"Error reading producer CSV: {e}")
        
        # Read Consumer CSV
        if os.path.isfile(consumer_csv):
            try:
                with open(consumer_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Is ML consumer', '').lower() == 'yes':
                            result['is_consumer'] = True
                            result['consumer_files'].append({
                                'file': row.get('where', ''),
                                'keyword': row.get('keywords', ''),
                                'line': row.get('line_number', ''),
                                'library': row.get('libraries', '')
                            })
                            result['consumer_keywords'].append(row.get('keywords', ''))
                            if row.get('libraries'):
                                result['libraries'].add(row.get('libraries'))
                            result['total_detections'] += 1
                
                logger.info(f"Consumer results: {len(result['consumer_files'])} detections")
            except Exception as e:
                logger.error(f"Error reading consumer CSV: {e}")
        
        # Convert set to list for JSON serialization
        result['libraries'] = list(result['libraries'])
        
        # Determine classification
        if result['is_producer'] and result['is_consumer']:
            result['classification'] = 'Hybrid'
        elif result['is_producer']:
            result['classification'] = 'Producer'
        elif result['is_consumer']:
            result['classification'] = 'Consumer'
        else:
            result['classification'] = 'Unknown'
        
        return result
    
    @staticmethod
    def extract_code_snippets(files_info: List[Dict], max_snippets: int = 3) -> List[Dict]:
        """
        Extract code snippets from files with detected keywords.
        
        Args:
            files_info: List of file info dicts with 'file', 'line', 'keyword'
            max_snippets: Maximum number of snippets to extract
            
        Returns:
            List of snippet dictionaries with file, line, and code content
        """
        snippets = []
        
        for file_info in files_info[:max_snippets]:
            try:
                file_path = file_info.get('file', '')
                line_num = int(file_info.get('line', 0))
                keyword = file_info.get('keyword', '')
                
                if not os.path.isfile(file_path) or line_num <= 0:
                    continue
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # Extract context: 2 lines before, target line, 2 lines after
                    start = max(0, line_num - 3)
                    end = min(len(lines), line_num + 2)
                    snippet_lines = lines[start:end]
                    
                    snippets.append({
                        'file': os.path.basename(file_path),
                        'line': line_num,
                        'keyword': keyword,
                        'code': ''.join(snippet_lines)
                    })
            
            except Exception as e:
                logger.error(f"Error extracting snippet from {file_info.get('file')}: {e}")
                continue
        
        return snippets
    
    @staticmethod
    def build_full_context(
        input_path: str, 
        output_path: str,
        project_name: Optional[str] = None
    ) -> Dict:
        """
        Build complete context for LLM from analysis results.
        
        Args:
            input_path: Path to analyzed project
            output_path: Path to analysis output folder
            project_name: Optional project name (extracted from input_path if None)
            
        Returns:
            Dictionary with complete project context
        """
        if project_name is None:
            project_name = os.path.basename(input_path.rstrip('/\\'))
        
        context = {
            'project_name': project_name,
            'input_path': input_path,
            'output_path': output_path
        }
        
        # Extract README
        context['readme'] = ContextBuilderService.extract_readme(input_path)
        
        # Extract dependencies
        context['dependencies'] = ContextBuilderService.extract_dependencies(input_path)
        
        # Find and parse result CSVs
        producer_csv = os.path.join(output_path, f'{project_name}_producer.csv')
        consumer_csv = os.path.join(output_path, f'{project_name}_consumer.csv')
        
        if not os.path.isfile(producer_csv) and not os.path.isfile(consumer_csv):
            # Try alternative naming
            csv_files = [f for f in os.listdir(output_path) if f.endswith('.csv')]
            producer_files = [f for f in csv_files if 'producer' in f.lower()]
            consumer_files = [f for f in csv_files if 'consumer' in f.lower()]
            
            if producer_files:
                producer_csv = os.path.join(output_path, producer_files[0])
            if consumer_files:
                consumer_csv = os.path.join(output_path, consumer_files[0])
        
        # Aggregate results
        analysis_results = ContextBuilderService.aggregate_analysis_results(
            producer_csv, consumer_csv
        )
        context['analysis_results'] = analysis_results
        
        # Extract code snippets
        all_files = analysis_results['producer_files'] + analysis_results['consumer_files']
        context['code_snippets'] = ContextBuilderService.extract_code_snippets(all_files)
        
        logger.info(f"Built context for {project_name}: {analysis_results['classification']}")
        
        return context
    
    @staticmethod
    def format_context_for_llm(context: Dict) -> str:
        """
        Format context dictionary into a readable string for LLM prompt.
        
        Args:
            context: Context dictionary from build_full_context
            
        Returns:
            Formatted string for LLM consumption
        """
        parts = []
        
        parts.append(f"# Progetto: {context['project_name']}")
        parts.append("")
        
        # Classification
        analysis = context.get('analysis_results', {})
        parts.append(f"## Classificazione: {analysis.get('classification', 'Unknown')}")
        parts.append("")
        
        # Libraries
        if analysis.get('libraries'):
            parts.append("## Librerie ML Rilevate:")
            for lib in analysis['libraries']:
                parts.append(f"- {lib}")
            parts.append("")
        
        # Producer detections
        if analysis.get('producer_files'):
            parts.append(f"## Rilevamenti Producer ({len(analysis['producer_files'])}):")
            for detection in analysis['producer_files'][:5]:  # Max 5
                parts.append(f"- File: {os.path.basename(detection['file'])}")
                parts.append(f"  Keyword: {detection['keyword']}, Linea: {detection['line']}")
            parts.append("")
        
        # Consumer detections
        if analysis.get('consumer_files'):
            parts.append(f"## Rilevamenti Consumer ({len(analysis['consumer_files'])}):")
            for detection in analysis['consumer_files'][:5]:  # Max 5
                parts.append(f"- File: {os.path.basename(detection['file'])}")
                parts.append(f"  Keyword: {detection['keyword']}, Linea: {detection['line']}")
            parts.append("")
        
        # Dependencies
        deps = context.get('dependencies', {})
        if deps:
            parts.append("## Dipendenze:")
            for source, dep_list in deps.items():
                parts.append(f"### {source}:")
                for dep in dep_list[:10]:  # Max 10 per source
                    parts.append(f"- {dep}")
            parts.append("")
        
        # README excerpt
        readme = context.get('readme', '')
        if readme:
            parts.append("## README (estratto):")
            parts.append(readme[:1000])  # First 1000 chars
            parts.append("")
        
        # Code snippets
        snippets = context.get('code_snippets', [])
        if snippets:
            parts.append("## Snippet Codice:")
            for snippet in snippets:
                parts.append(f"### {snippet['file']} (linea {snippet['line']}):")
                parts.append("```python")
                parts.append(snippet['code'])
                parts.append("```")
                parts.append("")
        
        return "\n".join(parts)
