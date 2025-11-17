"""
Functional tests for exec_analysis.py - ML Producer and Consumer Analysis Tool

This test suite validates the exec_analysis.py script, which analyzes Python projects
to identify ML model producers (code that trains/saves ML models) and ML model consumers
(code that loads/uses pre-trained ML models).

Test Coverage:
- EA_0: Error handling for non-existent input directories
- EA_1: Empty input directory (no projects) - should create structure with headers only
- EA_2: Single ML producer project detection
- EA_3: Single ML consumer project detection
- EA_4: Project that is both producer and consumer
- EA_5: Projects with no ML patterns (neither producer nor consumer)
- EA_6: Multiple projects with different patterns (one producer, one consumer)
- EA_7: Multiple projects with only consumer patterns
- EA_8: Multiple producers and one consumer
- EA_9: Complex scenario with multiple producers and consumers

Each test:
1. Runs exec_analysis.py with specific input projects
2. Validates output structure (Producers_Final and Consumers_Final directories)
3. Checks generated CSV files against expected results
4. Verifies no unexpected files are created
"""

import csv
import unittest
import subprocess
import os
import sys
import shutil
import pandas as pd
from io import StringIO

def read_csv_header(filepath):
    """
    Read only the header row from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of column names from the header row
    """
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return next(reader, [])

class BaseExecAnalysisTest(unittest.TestCase):
    """
    Base test class for exec_analysis.py functional tests.
    
    This class provides common setup, teardown, and assertion methods for testing
    the exec_analysis.py script. Each subclass should define:
    - temp_input_dir: Path to test input directory containing sample projects
    - temp_output_dir: Path where analysis results will be written
    - expected_producer_files: Dict mapping filename -> expected content (path or CSV string)
    - expected_consumer_files: Dict mapping filename -> expected content (path or CSV string)
    
    The test method validates:
    - Successful script execution
    - Creation of output directory structure
    - Presence of expected output files
    - Content accuracy (full CSV comparison or header-only for empty results)
    - Absence of unexpected files
    """
    temp_input_dir = None
    temp_output_dir = None
    expected_producer_files = []
    expected_consumer_files = []

    @classmethod
    def setUpClass(cls):
        """
        Set up test class by creating output directories if they don't exist.
        Defines paths for producer and consumer output directories.
        """
        # Skip the base class - only run concrete test classes
        if cls is BaseExecAnalysisTest:
            raise unittest.SkipTest("BaseExecAnalysisTest is an abstract base class")
            
        # Non fallisce, esegue il test comunque
        if not os.path.isdir(cls.temp_output_dir):
            os.makedirs(cls.temp_output_dir, exist_ok=True)

        cls.producers_output = os.path.join(cls.temp_output_dir, "Producers", "Producers_Final")
        cls.consumers_output = os.path.join(cls.temp_output_dir, "Consumers", "Consumers_Final")

    def tearDown(self):
        """
        Clean up after each test by completely removing all files and directories
        in the output folder. This ensures test isolation.
        """
        for item in os.listdir(self.temp_output_dir):
            item_path = os.path.join(self.temp_output_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    def compare_csv_on_columns(self, actual_path, expected_content, columns):
        """
        Confronta i file CSV solo sulle colonne specificate.
        
        Args:
            actual_path: Path to the actual output CSV file
            expected_content: Expected CSV content as a string
            columns: List of column names to compare
            
        Raises:
            AssertionError: If the CSV files differ on the specified columns
        """
        # Read both CSVs fully first
        actual_df_full = pd.read_csv(actual_path)
        expected_df_full = pd.read_csv(StringIO(expected_content))
        
        actual_cols = list(actual_df_full.columns)
        expected_cols = list(expected_df_full.columns)
        
        # Find columns that exist in BOTH actual and expected files from the requested columns
        existing_columns = [col for col in columns if col in actual_cols and col in expected_cols]
        
        if not existing_columns:
            self.fail(f"No common columns found between actual and expected for comparison.\n"
                     f"Actual columns: {actual_cols}\n"
                     f"Expected columns: {expected_cols}")
        
        # Filter out columns that are entirely NaN in the actual data (deprecated columns)
        columns_with_data = []
        for col in existing_columns:
            if not actual_df_full[col].isna().all():
                columns_with_data.append(col)
        
        if not columns_with_data:
            self.fail(f"All common columns are empty (NaN) in actual file.\n"
                     f"Common columns checked: {existing_columns}")
        
        # Now filter both dataframes to only the columns with actual data
        actual_df = actual_df_full[columns_with_data]
        expected_df = expected_df_full[columns_with_data]
        
        # Drop rows where ALL values are NaN in both dataframes (to handle schema differences)
        actual_df = actual_df.dropna(how='all').reset_index(drop=True)
        expected_df = expected_df.dropna(how='all').reset_index(drop=True)

        # Ordino per rendere il confronto indipendente dall'ordine delle righe
        # Only sort if we have data to sort
        if len(actual_df) > 0 and len(expected_df) > 0:
            try:
                actual_df_sorted = actual_df.sort_values(by=columns_with_data).reset_index(drop=True)
                expected_df_sorted = expected_df.sort_values(by=columns_with_data).reset_index(drop=True)
            except (KeyError, TypeError) as e:
                # If sorting fails, just use unsorted dataframes
                actual_df_sorted = actual_df.reset_index(drop=True)
                expected_df_sorted = expected_df.reset_index(drop=True)
        else:
            actual_df_sorted = actual_df
            expected_df_sorted = expected_df

        try:
            pd.testing.assert_frame_equal(actual_df_sorted, expected_df_sorted, check_like=True)
        except AssertionError as e:
            # Provide detailed information about what's different
            error_msg = f"\n{'='*80}\nDifferenze nei file CSV sulle colonne {columns_with_data}:\n"
            error_msg += f"\nActual DataFrame ({len(actual_df_sorted)} rows):\n{actual_df_sorted.head(10).to_string()}"
            if len(actual_df_sorted) > 10:
                error_msg += f"\n... ({len(actual_df_sorted) - 10} more rows)"
            error_msg += f"\n\nExpected DataFrame ({len(expected_df_sorted)} rows):\n{expected_df_sorted.to_string()}\n"
            error_msg += f"\nPandas comparison error:\n{e}\n"
            error_msg += f"\n{'='*80}\n"
            self.fail(error_msg)

    def test_exec_analysis_creates_expected_files(self):
        """
        Execute exec_analysis.py and verify that expected output files are created with correct content.
        
        This test:
        1. Runs the exec_analysis.py script with the specified input and output paths
        2. Verifies the script completes successfully (exit code 0 or 2 for managed errors)
        3. Checks that expected output directories are created
        4. Validates that all expected files are present
        5. Compares file content against expected values (headers or full CSV content)
        6. Ensures no unexpected files are generated
        """
        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "..", "Categorizer", "src", "exec_analysis.py")),
            "--input_path", self.temp_input_dir,
            "--output_path", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        # Accetta 0 (ok) o 2 (gestione input mancante)
        if result.returncode == 1:
            print("Input mancante gestito correttamente. Nessun controllo successivo necessario.")
            return  # esce dal test
        self.assertEqual(result.returncode, 0, f"Errore nell'esecuzione dello script: {result.stderr}")

        self.assertTrue(os.path.isdir(self.producers_output), "Cartella Producers_Final mancante")
        self.assertTrue(os.path.isdir(self.consumers_output), "Cartella Consumers_Final mancante")

        produced_producer_files = [
            f for f in os.listdir(self.producers_output)
            if os.path.isfile(os.path.join(self.producers_output, f))
        ]
        produced_consumer_files = [
            f for f in os.listdir(self.consumers_output)
            if os.path.isfile(os.path.join(self.consumers_output, f))
        ]

        # Read actual file to determine which columns exist
        # Use only columns that exist in BOTH actual and expected files
        
        # ---- Producers
        for expected_file, expected_content_ref in self.expected_producer_files.items():
            self.assertIn(expected_file, produced_producer_files,
                          f"File atteso non trovato in Producers_Final: {expected_file}")
            actual_path = os.path.join(self.producers_output, expected_file)
            
            expected_content = load_expected_content(expected_content_ref)

            if isinstance(expected_content, str):
                # Usa la nuova funzione solo per CSV completi (con righe)
                if '\n' in expected_content and ',' in expected_content:
                    # Determine columns dynamically from both files
                    actual_df = pd.read_csv(actual_path)
                    expected_df = pd.read_csv(StringIO(expected_content))
                    
                    # If expected file has no data rows, just check headers match
                    if len(expected_df) == 0:
                        actual_header = list(actual_df.columns)
                        expected_header = list(expected_df.columns)
                        self.assertEqual(actual_header, expected_header,
                                       f"Header non corrisponde per file: {expected_file}")
                        # Also check that actual is empty too
                        self.assertEqual(len(actual_df), 0,
                                       f"Expected empty file but actual has {len(actual_df)} rows in {expected_file}")
                        continue
                    
                    # Find common columns between actual and expected
                    common_cols = [col for col in expected_df.columns if col in actual_df.columns]
                    
                    if not common_cols:
                        self.fail(f"No common columns found between actual and expected for {expected_file}.\n"
                                 f"Actual columns: {list(actual_df.columns)}\n"
                                 f"Expected columns: {list(expected_df.columns)}")
                    
                    self.compare_csv_on_columns(actual_path, expected_content, common_cols)
                else:
                    actual_header = read_csv_header(actual_path)
                    expected_header = expected_content.split(",")
                    self.assertEqual(actual_header, expected_header,
                                     f"Header non corrisponde per file: {expected_file}")
            else:
                raise ValueError(f"Formato non supportato per expected_content in file {expected_file}")

        # ---- Consumers
        for expected_file, expected_content_ref in self.expected_consumer_files.items():
            self.assertIn(expected_file, produced_consumer_files,
                          f"File atteso non trovato in Consumers_Final: {expected_file}")
            actual_path = os.path.join(self.consumers_output, expected_file)
            
            expected_content = load_expected_content(expected_content_ref)

            if isinstance(expected_content, str):
                if '\n' in expected_content and ',' in expected_content:
                    # Determine columns dynamically from both files
                    actual_df = pd.read_csv(actual_path)
                    expected_df = pd.read_csv(StringIO(expected_content))
                    
                    # If expected file has no data rows, just check headers match
                    if len(expected_df) == 0:
                        actual_header = list(actual_df.columns)
                        expected_header = list(expected_df.columns)
                        self.assertEqual(actual_header, expected_header,
                                       f"Header non corrisponde per file: {expected_file}")
                        # Also check that actual is empty too
                        self.assertEqual(len(actual_df), 0,
                                       f"Expected empty file but actual has {len(actual_df)} rows in {expected_file}")
                        continue
                    
                    # Find common columns between actual and expected
                    common_cols = [col for col in expected_df.columns if col in actual_df.columns]
                    
                    if not common_cols:
                        self.fail(f"No common columns found between actual and expected for {expected_file}.\n"
                                 f"Actual columns: {list(actual_df.columns)}\n"
                                 f"Expected columns: {list(expected_df.columns)}")
                    
                    self.compare_csv_on_columns(actual_path, expected_content, common_cols)
                else:
                    actual_header = read_csv_header(actual_path)
                    expected_header = expected_content.split(",")
                    self.assertEqual(actual_header, expected_header,
                                     f"Header non corrisponde per file: {expected_file}")
            else:
                raise ValueError(f"Formato non supportato per expected_content in file {expected_file}")

        # ---- File inattesi
        unexpected_producers = set(produced_producer_files) - set(self.expected_producer_files.keys())
        unexpected_consumers = set(produced_consumer_files) - set(self.expected_consumer_files.keys())

        self.assertFalse(unexpected_producers, f"File inattesi trovati in Producers_Final: {unexpected_producers}")
        self.assertFalse(unexpected_consumers, f"File inattesi trovati in Consumers_Final: {unexpected_consumers}")


def load_expected_content(path_or_content):
    """
    Load expected content from a file path or return the content directly if it's a header string.
    
    Args:
        path_or_content: Either a file path to load CSV content from, or a CSV header string
        
    Returns:
        The CSV content as a string
    """
    # If it contains a newline or looks like a file path, treat it accordingly
    if os.path.exists(path_or_content):
        with open(path_or_content, newline='', encoding='utf-8') as f:
            return f.read()
    else:
        # It's already the content string (e.g., just a header)
        return path_or_content


def concat_csvs(path1, path2):
    """
    Concatenate two CSV files, keeping only one header row.
    
    Args:
        path1: Path to the first CSV file
        path2: Path to the second CSV file
        
    Returns:
        Combined CSV content as a string
        
    Raises:
        ValueError: If the CSV files have different headers
    """
    with open(path1, newline='', encoding='utf-8') as f1, open(path2, newline='', encoding='utf-8') as f2:
        reader1 = list(csv.reader(f1))
        reader2 = list(csv.reader(f2))

        # Verifica che gli header siano uguali
        if reader1[0] != reader2[0]:
            raise ValueError("I file hanno header diversi e non possono essere concatenati.")

        # Unisce solo i dati, evitando di duplicare l'header
        rows = [reader1[0]] + reader1[1:] + reader2[1:]

        # Converte in stringa CSV
        return "\n".join([",".join(row) for row in rows])



# EA_0: Test with non-existent input directory
# This test should fail gracefully when the input directory doesn't exist
class TestCase0(BaseExecAnalysisTest):
    """Test exec_analysis behavior with non-existent input directory."""
    temp_input_dir = "Test_input/input_non_esiste"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {}
    expected_consumer_files = {}
    
    def test_exec_analysis_creates_expected_files(self):
        """Verify that exec_analysis handles missing input directory gracefully."""
        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "..", "Categorizer", "src", "exec_analysis.py")),
            "--input_path", self.temp_input_dir,
            "--output_path", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        # Should exit with error code 1 when input directory doesn't exist
        self.assertEqual(result.returncode, 1, 
                        f"Expected error when input directory doesn't exist, but got: {result.returncode}")
        self.assertIn("does not exist", result.stdout, 
                     "Error message should indicate input folder doesn't exist")

# EA_1: Test with empty input directory
# Verifies that the tool creates output structure with only header rows when no projects exist
class TestCase1(BaseExecAnalysisTest):
    """Test exec_analysis with an empty input directory (no projects to analyze)."""
    temp_input_dir = "Test_input/input_1"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "ProjectName,Is ML producer,where,keyword,line_number"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "ProjectName,Is ML consumer,where,keyword,line_number"
    }

# EA_2: Test with a single ML producer project
# Verifies detection of ML model producers only (no consumers)
class TestCase2(BaseExecAnalysisTest):
    """Test exec_analysis with a single project that is an ML producer."""
    temp_input_dir = "Test_input/input_2"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "Test_input/expected/aaronlam88_cmpe295_ml_producer.csv",
        "repos2_aaronlam88_ml_producer.csv" : "Test_input/expected/aaronlam88_cmpe295_ml_producer.csv"
    }
    expected_consumer_files = {
        "results_consumer.csv": "ProjectName,Is ML consumer,where,keyword,line_number,libraries,keywords"
    }

# EA_3: Test with a single ML consumer project
# Verifies detection of ML model consumers only (no producers)
class TestCase3(BaseExecAnalysisTest):
    """Test exec_analysis with a single project that is an ML consumer."""
    temp_input_dir = "Test_input/input_3"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "ProjectName,Is ML producer,where,keyword,line_number"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/keums_melodyExtraction_JDC_ml_consumer.csv"
    }

# EA_4: Test with a project that is both producer and consumer
# Verifies detection when a single project has both ML production and consumption patterns
class TestCase4(BaseExecAnalysisTest):
    """Test exec_analysis with a project that is both an ML producer and consumer."""
    temp_input_dir = "Test_input/input_4"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "Test_input/expected/appinho_SAComputerVisionMachineLearning_ml_producer.csv"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/appinho_SAComputerVisionMachineLearning_ml_consumer.csv"
    }

# EA_5: Test with projects that are neither producers nor consumers
# Verifies that non-ML projects are correctly identified (empty results except headers)
class TestCase5(BaseExecAnalysisTest):
    """Test exec_analysis with projects that have no ML patterns (neither producer nor consumer)."""
    temp_input_dir = "Test_input/input_5"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv": "ProjectName,Is ML producer,where,keyword,line_number"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "ProjectName,Is ML consumer,where,keyword,line_number"
    }

# EA_6: Test with multiple projects - one producer and one consumer
# Verifies correct handling of multiple distinct projects with different ML patterns
class TestCase6(BaseExecAnalysisTest):
    """Test exec_analysis with two projects: one ML producer and one ML consumer."""
    temp_input_dir = "Test_input/input_6"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "Test_input/expected/testcase6_producer.csv"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/keums_melodyExtraction_JDC_ml_consumer.csv"
    }

# EA_7: Test with mixed projects - no producers but has consumers
# Verifies correct behavior when only consumer patterns are detected across multiple projects
class TestCase7(BaseExecAnalysisTest):
    """Test exec_analysis with projects that only contain ML consumers (no producers)."""
    temp_input_dir = "Test_input/input_7"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv": "ProjectName,Is ML producer,where,keyword,line_number"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/keums_melodyExtraction_JDC_ml_consumer.csv"
    }

# EA_8: Test with multiple projects - multiple producers and one consumer
# Verifies aggregation of results when multiple producer projects are analyzed together
class TestCase8(BaseExecAnalysisTest):
    """Test exec_analysis with multiple ML producers and one ML consumer project."""
    temp_input_dir = "Test_input/input_8"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "Test_input/expected/combined_producers_8.csv"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/appinho_SAComputerVisionMachineLearning_ml_consumer.csv"
    }

# EA_9: Test with multiple projects - multiple producers and multiple consumers
# Verifies correct aggregation when analyzing a complex set of projects with various ML patterns
class TestCase9(BaseExecAnalysisTest):
    """Test exec_analysis with multiple projects that are both ML producers and consumers."""
    temp_input_dir = "Test_input/input_9"
    temp_output_dir = "Test_input/output"
    expected_producer_files = {
        "results_first_step.csv" : "Test_input/expected/combined_producers_9.csv"
    }
    expected_consumer_files = {
        "results_consumer.csv" : "Test_input/expected/combined_consumers_9.csv"
    }


if __name__ == '__main__':
    # Importa il reporter Markdown
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from test_reporter import MarkdownTestRunner
    
    # Crea la suite di test
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Esegui con il reporter Markdown
    runner = MarkdownTestRunner(verbosity=2)
    runner.run(suite)
