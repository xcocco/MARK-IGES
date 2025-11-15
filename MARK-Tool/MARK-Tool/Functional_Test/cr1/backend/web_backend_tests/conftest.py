"""
Pytest Configuration and Fixtures for Web Backend Tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Ensure testing environment and a SECRET_KEY are set before importing
# the application modules. The config module defines a ProductionConfig
# that raises if SECRET_KEY is missing at import time, so set defaults
# here to avoid import-time failures when running tests.
os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')

from web_gui.app import create_app
from web_gui.services.file_service import FileService
from web_gui.services.analysis_service import AnalysisService


@pytest.fixture(scope='session')
def temp_dir():
    """Create a temporary directory for testing"""
    temp = tempfile.mkdtemp(prefix='mark_test_')
    yield temp
    # Cleanup
    if os.path.exists(temp):
        shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture(scope='function')
def test_upload_dir(temp_dir):
    """Create a temporary upload directory for each test"""
    upload_dir = os.path.join(temp_dir, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    yield upload_dir
    # Cleanup after each test
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir, ignore_errors=True)


@pytest.fixture(scope='function')
def test_input_dir(temp_dir):
    """Create a temporary input directory with sample repos"""
    input_dir = os.path.join(temp_dir, 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    # Create a sample repo structure
    repo_path = os.path.join(input_dir, 'sample_repo')
    os.makedirs(repo_path, exist_ok=True)
    
    # Create a sample Python file
    with open(os.path.join(repo_path, 'sample.py'), 'w') as f:
        f.write('import pandas as pd\ndf = pd.DataFrame()\n')
    
    yield input_dir
    # Cleanup
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir, ignore_errors=True)


@pytest.fixture(scope='function')
def test_output_dir(temp_dir):
    """Create a temporary output directory"""
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    yield output_dir
    # Cleanup
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)


@pytest.fixture(scope='function')
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing"""
    csv_path = os.path.join(temp_dir, 'sample.csv')
    with open(csv_path, 'w') as f:
        f.write('repo_name,repo_url\n')
        f.write('test_repo,https://github.com/test/repo\n')
    yield csv_path
    # Cleanup
    if os.path.exists(csv_path):
        os.remove(csv_path)


@pytest.fixture(scope='function')
def sample_results_csv(test_output_dir):
    """Create sample result CSV files"""
    # Create directory structure
    consumers_dir = os.path.join(test_output_dir, 'Consumers', 'Consumers_Final')
    producers_dir = os.path.join(test_output_dir, 'Producers', 'Producers_Final')
    os.makedirs(consumers_dir, exist_ok=True)
    os.makedirs(producers_dir, exist_ok=True)
    
    # Create consumer CSV
    consumer_csv = os.path.join(consumers_dir, 'consumer_0.csv')
    with open(consumer_csv, 'w') as f:
        f.write('Repo,File,Method,Library\n')
        f.write('test_repo,test.py,load_model,sklearn\n')
        f.write('test_repo,test.py,predict,tensorflow\n')
    
    # Create producer CSV
    producer_csv = os.path.join(producers_dir, 'producer_0.csv')
    with open(producer_csv, 'w') as f:
        f.write('Repo,File,Method,Library\n')
        f.write('test_repo,train.py,fit,sklearn\n')
    
    yield {
        'consumer': consumer_csv,
        'producer': producer_csv,
        'consumers_dir': consumers_dir,
        'producers_dir': producers_dir
    }


@pytest.fixture(scope='function')
def app(test_upload_dir, monkeypatch):
    """Create and configure a Flask app instance for testing"""
    # Set environment to testing
    monkeypatch.setenv('FLASK_ENV', 'testing')
    
    # Create app with testing config
    app = create_app('testing')
    
    # Override upload folder
    app.config['UPLOAD_FOLDER'] = test_upload_dir
    app.config['TESTING'] = True
    
    yield app


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner for the Flask app"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def file_service(test_upload_dir):
    """Create a FileService instance for testing"""
    return FileService(
        upload_folder=test_upload_dir,
        allowed_extensions={'csv'}
    )


@pytest.fixture(scope='function')
def analysis_service():
    """Create an AnalysisService instance for testing"""
    # Use dummy paths for testing
    return AnalysisService(
        exec_analysis_path='dummy_exec_analysis.py',
        cloner_path='dummy_cloner.py'
    )
