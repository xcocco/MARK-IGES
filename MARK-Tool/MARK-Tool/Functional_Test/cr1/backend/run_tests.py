#!/usr/bin/env python3
"""
MARK-Tool Backend Test Runner
Comprehensive test execution script
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
    test_dir = script_dir / 'web_backend_tests'
    
    # Pulisci i risultati temporanei precedenti
    temp_results = script_dir / '.test_results_temp.json'
    if temp_results.exists():
        temp_results.unlink()
        print("🗑️  Risultati precedenti rimossi\n")
    
    # Change to test directory
    os.chdir(script_dir)
    
    print_header("MARK-Tool Backend API Test Suite")
    print("Test Planning: CR1 - Backend Testing")
    print("Total Expected Tests: 51+")
    print(f"Test Directory: {test_dir}\n")
    
    results = []
    
    # Check if pytest is installed
    try:
        subprocess.run(['pytest', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: pytest is not installed!")
        print("Please run: pip install -r requirements-test.txt")
        return 1
    
    # Test 1: Analysis Routes
    print_header("Test Suite 1/4: Analysis Routes (9 tests)")
    results.append(run_command(
        ['pytest', 'web_backend_tests/test_analysis_routes.py', '-v'],
        "Analysis Routes Tests"
    ))
    
    # Test 2: File Routes
    print_header("Test Suite 2/4: File Routes (11 tests)")
    results.append(run_command(
        ['pytest', 'web_backend_tests/test_file_routes.py', '-v'],
        "File Routes Tests"
    ))
    
    # Test 3: Results Routes
    print_header("Test Suite 3/4: Results Routes (12 tests)")
    results.append(run_command(
        ['pytest', 'web_backend_tests/test_results_routes.py', '-v'],
        "Results Routes Tests"
    ))
    
    # Test 4: Integration Tests
    print_header("Test Suite 4/4: Integration Tests (6+ tests)")
    results.append(run_command(
        ['pytest', 'web_backend_tests/test_integration.py', '-v'],
        "Integration Tests"
    ))
    
    # Summary
    print_header("Test Execution Summary")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Test Suites: {passed}/{total} passed")
    
    for i, result in enumerate(results, 1):
        status = "[OK] PASSED" if result else "[X] FAILED"
        suite_name = [
            "Analysis Routes",
            "File Routes",
            "Results Routes",
            "Integration Tests"
        ][i - 1]
        print(f"  Suite {i}: {suite_name} - {status}")
    
    print("\n" + "=" * 80)
    
    if all(results):
        print("\n All test suites PASSED! \n")
        return 0
    else:
        print("\n Some test suites FAILED \n")
        print("Run individual test suites with:")
        print("  pytest web_backend_tests/test_<module>.py -v")
        print("\nFor detailed output:")
        print("  pytest web_backend_tests/ -vv --tb=long")
        return 1


if __name__ == '__main__':
    sys.exit(main())
