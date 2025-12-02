"""
Pytest Configuration and Fixtures for CR2 Backend Tests
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

import pytest

# Importa il reporter Markdown
from pytest_md_reporter import markdown_reporter

# Add web_gui to Python path
web_gui_path = Path(__file__).parent.parent.parent.parent / 'web_gui'
sys.path.insert(0, str(web_gui_path))

# Set testing environment
os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')

from services.analytics_service import AnalyticsService


@pytest.fixture(scope='session')
def temp_dir():
    """Create a temporary directory for testing"""
    temp = tempfile.mkdtemp(prefix='mark_cr2_test_')
    yield temp
    # Cleanup
    if os.path.exists(temp):
        shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture(scope='function')
def analytics_service():
    """Create AnalyticsService instance for testing"""
    return AnalyticsService()


@pytest.fixture(scope='function')
def test_csv_dir(temp_dir):
    """Create a temporary directory with test CSV files"""
    csv_dir = os.path.join(temp_dir, 'test_output')
    os.makedirs(csv_dir, exist_ok=True)
    yield csv_dir
    # Cleanup after each test
    if os.path.exists(csv_dir):
        shutil.rmtree(csv_dir, ignore_errors=True)
