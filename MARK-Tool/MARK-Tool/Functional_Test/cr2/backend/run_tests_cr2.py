#!/usr/bin/env python3
"""
MARK-Tool CR2 Backend Test Runner
Comprehensive test execution script for Analytics Dashboard
"""
import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_command(cmd, description):
    """Run a command and return the result"""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"✓ {description} - PASSED\n")
        return True
    else:
        print(f"✗ {description} - FAILED\n")
        return False


def main():
    """Main test runner"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Pulisci i risultati temporanei precedenti
    temp_results = script_dir / '.test_results_temp.json'
    if temp_results.exists():
        temp_results.unlink()
        print("🗑️  Risultati precedenti rimossi\n")
    
    # Rimuovi anche il vecchio report markdown se esiste
    old_report = script_dir / 'TEST_RESULTS.md'
    if old_report.exists():
        old_report.unlink()
        print("🗑️  Vecchio report TEST_RESULTS.md rimosso\n")
    
    # Change to test directory
    os.chdir(script_dir)
    
    print_header("MARK-Tool CR2 Analytics Dashboard Test Suite")
    print("Test Planning: CR2 - Analytics Backend Testing")
    print("Total Expected Tests: 50+ (20 unit + 30 API + integration)")
    print(f"Test Directory: {script_dir}\n")
    
    results = []
    
    # Check if pytest is installed
    try:
        subprocess.run([sys.executable, '-m', 'pytest', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: pytest is not installed!")
        print("Please run: pip install -r requirements-test.txt")
        return 1
    
    # Test 1: AnalyticsService Unit Tests
    print_header("Test Suite 1/3: AnalyticsService Unit Tests (20 tests)")
    results.append(run_command(
        [sys.executable, '-m', 'pytest', 'test_analytics_service.py', '-v'],
        "AnalyticsService Unit Tests"
    ))
    
    # Test 2: Analytics API Tests
    print_header("Test Suite 2/3: Analytics API Tests (30 tests)")
    results.append(run_command(
        [sys.executable, '-m', 'pytest', 'test_analytics_api.py', '-v'],
        "Analytics API Tests"
    ))
    
    # Test 3: Integration Tests
    print_header("Test Suite 3/3: Integration Tests (4 tests)")
    results.append(run_command(
        [sys.executable, '-m', 'pytest', 'test_integration.py', '-v'],
        "Integration Tests"
    ))
    
    # Summary
    print_header("Test Execution Summary")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Test Suites: {passed}/{total} passed")
    
    suite_names = [
        "AnalyticsService Unit Tests",
        "Analytics API Tests",
        "Integration Tests"
    ]
    
    for i, result in enumerate(results, 1):
        status = "[OK] PASSED" if result else "[X] FAILED"
        suite_name = suite_names[i - 1] if i <= len(suite_names) else f"Suite {i}"
        print(f"  Suite {i}: {suite_name} - {status}")
    
    print("\n" + "=" * 80)
    
    # Verifica se il report markdown è stato generato
    report_file = script_dir / 'TEST_RESULTS.md'
    if report_file.exists():
        print("\n📝 Report dettagliato generato: TEST_RESULTS.md\n")
    
    if all(results):
        print("\n All test suites PASSED! \n")
        return 0
    else:
        print("\n Some test suites FAILED \n")
        print("Run individual test suites with:")
        print("  pytest test_analytics_service.py -v")
        print("  pytest test_analytics_api.py -v")
        print("  pytest test_integration.py -v")
        print("\nFor detailed output:")
        print("  pytest -vv --tb=long")
        return 1


if __name__ == '__main__':
    sys.exit(main())
