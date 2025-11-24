"""
Functional tests for cloner.py - GitHub Repository Cloning Tool

This test suite validates the cloner.py script, which reads a CSV file containing
GitHub repository information and clones the specified repositories to a local directory.

Test Coverage:
- CL_0: Error handling for non-existent CSV input file
- CL_1: Empty CSV file (no repositories to clone)
- CL_2: Single repository cloning
- CL_3: Multiple repositories cloning

Each test:
1. Runs cloner.py with a specific CSV input file
2. Validates successful execution (exit code 0)
3. Checks that the expected repositories were cloned to the correct directory structure
4. Verifies that no repositories exist when input is empty or missing
5. Cleans up cloned repositories after each test for isolation
"""

import unittest
import subprocess
import os
import sys
import shutil
import stat


class BaseClonerTest(unittest.TestCase):
    """
    Base test class for cloner.py functional tests.
    
    This abstract base class provides common setup, teardown, and test logic for
    validating the cloner.py script. Subclasses should define:
    - csv_input_file: Path to the CSV file containing repository information
    - temp_output_dir: Directory where repositories will be cloned
    - expected_cloned_repositories: Set or list of expected "owner/repo" strings
    
    The test validates:
    - Successful script execution
    - Correct repository cloning structure (repos2/owner/repo)
    - Handling of empty or missing CSV files
    - Cleanup of cloned repositories after test completion
    """
    # Make this an abstract base - subclasses must override these
    csv_input_file = None
    temp_output_dir = None

    @classmethod
    def setUpClass(cls):
        """
        Set up test class and validate that this is not the abstract base class.
        
        Converts relative paths to absolute paths and determines if the input CSV file exists.
        Sets up the expected repository base path (repos2).
        
        Raises:
            unittest.SkipTest: If called on the BaseClonerTest class directly
        """
        # Skip the base class - only run concrete test classes
        if cls is BaseClonerTest:
            raise unittest.SkipTest("BaseClonerTest is an abstract base class")
        
        cls.csv_input_file = os.path.abspath(cls.csv_input_file)
        cls.temp_output_dir = os.path.abspath(cls.temp_output_dir)

        cls.input_file_exists = os.path.isfile(cls.csv_input_file)

        cls.repos_base_path = os.path.join(cls.temp_output_dir, "repos2")

    @staticmethod
    def handle_remove_readonly(func, path, exc):
        """
        Handle removal of read-only files during cleanup.
        
        Git repositories often contain read-only files that require special handling
        when deleting on Windows systems.
        
        Args:
            func: The function that raised the exception (os.rmdir, os.remove, etc.)
            path: The path to the file/directory
            exc: The exception that was raised
            
        Raises:
            Exception: Re-raises the exception if it's not a PermissionError
        """
        if isinstance(exc, PermissionError) and func in (os.rmdir, os.remove, os.unlink):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise exc

    def tearDown(self):
        """
        Clean up after each test by removing all cloned repositories.
        
        Uses special handling for read-only files that may exist in Git repositories.
        This ensures test isolation and prevents disk space issues.
        """
        if os.path.exists(self.repos_base_path):
            shutil.rmtree(self.repos_base_path, onexc=self.handle_remove_readonly)

    def test_cloner_expected_files(self):
        """
        Test the cloner.py script with the configured CSV input file.
        
        This test performs the following validations:
        1. Checks if the CSV input file exists and is non-empty
        2. Executes cloner.py with the specified input and output paths
        3. Verifies successful execution (exit code 0)
        4. For empty/missing CSV files:
           - Ensures no repos2 directory is created
        5. For valid CSV files with repositories:
           - Verifies repos2 directory exists
           - Checks that all expected repositories were cloned
           - Validates correct directory structure (repos2/owner/repo)
           - Ensures no unexpected repositories were cloned
        
        The test outputs diagnostic information including stdout and stderr
        from the cloner.py execution.
        """
        # Verifica se il file esiste
        if not os.path.isfile(self.csv_input_file):
            print(f"\nFile CSV non trovato: {self.csv_input_file}")
            is_empty_csv = True  # Considera il file come "vuoto" per il test
        else:
            with open(self.csv_input_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                is_empty_csv = len(lines) <= 1

        cmd = [
            sys.executable,
            os.path.abspath(os.path.join("..", "..", "..", "cloner", "cloner.py")),
            "--input", self.csv_input_file,
            "--output", self.temp_output_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        print("\n===== STDOUT =====")
        print(result.stdout)
        print("===== STDERR =====")
        print(result.stderr)

        # Se il comando è terminato con errore, fallo fallire
        if result.returncode != 0:
            self.fail(f"Il comando cloner.py è terminato con errore, returncode={result.returncode}")

        self.repos_base_path = os.path.join(self.temp_output_dir, "repos2")

        if is_empty_csv:
            print(f"\nCSV '{self.csv_input_file}' vuoto o inesistente: verifico che nessuna repo sia stata clonata.")
            self.assertFalse(
                os.path.exists(self.repos_base_path),
                f"La cartella {self.repos_base_path} **non dovrebbe esistere** se il CSV è vuoto o mancante"
            )
            return  # Fine test per file vuoto o inesistente

        # Se arrivi qui significa che il CSV esiste ed è non vuoto
        print(f"\nContenuto di {self.repos_base_path}:")
        if os.path.exists(self.repos_base_path):
            print(os.listdir(self.repos_base_path))
        else:
            print("Cartella 'repos2' non trovata")

        self.assertTrue(os.path.isdir(self.repos_base_path), f"La cartella {self.repos_base_path} non esiste")

        if hasattr(self, "expected_cloned_repositories"):
            found = set()
            for owner in os.listdir(self.repos_base_path):
                owner_path = os.path.join(self.repos_base_path, owner)
                if os.path.isdir(owner_path):
                    for repo in os.listdir(owner_path):
                        repo_path = os.path.join(owner_path, repo)
                        if os.path.isdir(repo_path):
                            found.add(f"{owner}/{repo}")

            expected = set(self.expected_cloned_repositories)

            self.assertEqual(found, expected,
                             f"Repository clonate non corrispondono.\nAttese: {expected}\nTrovate: {found}")


# CL_0: Test with non-existent CSV file
# Verifies that the cloner handles missing input files gracefully
class TestClonerCase0(BaseClonerTest):
    """Test cloner.py behavior with a non-existent CSV input file."""
    csv_input_file = "Test_input/input/input_non_esiste.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = {

    }

# CL_1: Test with empty CSV file
# Verifies that no repositories are cloned when the CSV is empty or contains only headers
class TestClonerCase1(BaseClonerTest):
    """Test cloner.py with an empty CSV file (no repositories to clone)."""
    csv_input_file = "Test_input/input/input_1.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = {
    }

# CL_2: Test with single repository
# Verifies successful cloning of a single GitHub repository
class TestClonerCase2(BaseClonerTest):
    """Test cloner.py with a CSV containing a single repository."""
    csv_input_file = "Test_input/input/input_2.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = [
        "921kiyo/3d-dl"
    ]

# CL_3: Test with multiple repositories
# Verifies successful cloning of multiple GitHub repositories from different owners
class TestClonerCase3(BaseClonerTest):
    """Test cloner.py with a CSV containing multiple repositories from different owners."""
    csv_input_file = "Test_input/input/input_3.csv"
    temp_output_dir = "Test_input/output"
    expected_cloned_repositories = [
        "aaronlam88/cmpe295",
        "abdullahselek/koolsla",
        "abreheret/PixelAnnotationTool"
    ]



if __name__ == "__main__":
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
