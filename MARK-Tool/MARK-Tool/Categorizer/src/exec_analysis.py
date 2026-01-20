import os
import argparse
from consumer_classifier_by_dict import MLConsumerAnalyzer
from producer_classifier_by_dict import MLProducerAnalyzer
from components.notebook_converter import NotebookConverter


class ExecAnalyzer:
    def __init__(self, input_path=None, output_path=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_dir = script_dir
        self.input_path = input_path or os.path.join(script_dir, "..", "..", "repos")
        self.output_path = output_path or script_dir

    def run(self):
        import time
        import shutil
        start_time = time.time()
        
        # Check input and output paths
        if not os.path.exists(self.input_path):
            print(f"Error: The input folder '{self.input_path}' does not exist.")
            exit(1)
        
        # Clean up old CSV files in output directory before analysis
        self._cleanup_old_csvs(self.output_path)
        
        print(f"\n{'='*60}")
        print(f"Starting Analysis Process")
        print(f"Input path: {self.input_path}")
        print(f"Output path: {self.output_path}")
        print(f"{'='*60}\n")

        # --- ML-Model Producers ---
        output_base_folder = os.path.join(self.output_path, "Producers")
        output_folder_producers = os.path.join(output_base_folder, "Producers_Final")
        producer_dict_path = os.path.join(self.script_dir, "library_dictionary", "library_dict_producers_2.csv")

        os.makedirs(output_folder_producers, exist_ok=True)

        if not os.path.exists(producer_dict_path):
            print(f"Error Producer: The library dictionary '{producer_dict_path}' does not exist.")
            exit(1)

        print(f"Analyzing Producers with dictionary: {producer_dict_path}")
        print(f"Results will be written to: {output_folder_producers}")
        analyzer = MLProducerAnalyzer(output_folder=output_folder_producers)
        analyzer.analyze_projects_set_for_producers(self.input_path, producer_dict_path)

        # --- ML-Model Consumers ---
        output_base_folder = os.path.join(self.output_path, "Consumers")
        output_folder_consumers = os.path.join(output_base_folder, "Consumers_Final")
        consumer_dict_path = os.path.join(self.script_dir, "library_dictionary", "library_dict_consumers_2.csv")

        os.makedirs(output_folder_consumers, exist_ok=True)

        if not os.path.exists(consumer_dict_path):
            print(f"Error Consumer: The library dictionary '{consumer_dict_path}' does not exist.")
            exit(1)

        print(f"Analyzing Consumers with dictionary: {consumer_dict_path}")
        print(f"Results will be written to: {output_folder_consumers}")
        print("Rules_3 is set to: True")
        print("Rules_4 is set to: True")

        analyzer = MLConsumerAnalyzer(output_folder=output_folder_consumers)
        analyzer.analyze_projects_set_for_consumers(
            self.input_path,
            consumer_dict_path,
            producer_dict_path,
            rules_3=True,
            rules_4=True
        )
        
        # Copy final results to root of output_path for easy access
        self._copy_final_results(output_folder_producers, output_folder_consumers, self.output_path)
        
        end_time = time.time()
        print(f"\n{'='*60}")
        print(f"Analysis Complete!")
        print(f"Total time: {end_time - start_time:.2f} seconds")
        print(f"Results saved to: {self.output_path}")
        print(f"{'='*60}\n")
    def _cleanup_old_csvs(self, output_path):
        """Clean up old CSV files in the output directory before running new analysis"""
        import glob
        import shutil
        
        print(f"\n{'='*60}")
        print("Cleaning up old analysis results...")
        print(f"{'='*60}")
        
        # Patterns to match old CSV files
        patterns = [
            os.path.join(output_path, "*.csv"),
            os.path.join(output_path, "Producers", "**", "*.csv"),
            os.path.join(output_path, "Consumers", "**", "*.csv"),
            os.path.join(output_path, "*_producer.csv"),
            os.path.join(output_path, "*_consumer.csv")
        ]
        
        removed_count = 0
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    os.remove(file_path)
                    print(f"Removed old file: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"Warning: Could not remove {file_path}: {e}")
        
        # Also clean up old directories
        for dir_name in ["Producers", "Consumers"]:
            dir_path = os.path.join(output_path, dir_name)
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed old directory: {dir_path}")
                except Exception as e:
                    print(f"Warning: Could not remove directory {dir_path}: {e}")
        
        print(f"Cleanup complete: Removed {removed_count} old CSV files\n")
    
    def _copy_final_results(self, producer_folder, consumer_folder, output_path):
        """Copy final CSV results to the root of output_path for easy access"""
        import shutil
        import glob
        
        print(f"\n{'='*60}")
        print("Copying final results to output directory...")
        print(f"{'='*60}")
        
        # Find and copy producer CSV
        producer_csvs = glob.glob(os.path.join(producer_folder, "*.csv"))
        for csv_file in producer_csvs:
            dest = os.path.join(output_path, "producer.csv")
            shutil.copy2(csv_file, dest)
            print(f"Copied: {os.path.basename(csv_file)} -> {dest}")
        
        # Find and copy consumer CSV
        consumer_csvs = glob.glob(os.path.join(consumer_folder, "*.csv"))
        for csv_file in consumer_csvs:
            dest = os.path.join(output_path, "consumer.csv")
            shutil.copy2(csv_file, dest)
            print(f"Copied: {os.path.basename(csv_file)} -> {dest}")
        
        print(f"Results copied successfully\n")
    
    # Metodo per API web
    def run_async(self):
        """Esegue l’analisi in un thread in background"""
        import threading
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        return thread


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Run ablation analysis for ML model producers and consumers.")
    parser.add_argument("--input_path", type=str, default=os.path.join(script_dir, "..", "..", "repos"),
                        help="Path to the input directory containing project repositories.")
    parser.add_argument("--output_path", type=str, default=script_dir,
                        help="Path to the output directory to store analysis results.")

    args = parser.parse_args()
    print(f"Starting ablation analysis with input path: {args.input_path} and output path: {args.output_path}")

    # Aggiunta esecuzione processo di conversione dei file . in .py
    import time
    print(f"\n{'='*60}")
    print("Step 1: Converting Jupyter Notebooks to Python files")
    print(f"{'='*60}")
    conv_start = time.time()
    converter = NotebookConverter()
    converter.run()
    conv_end = time.time()
    print(f"\n[TIMING] Notebook conversion took: {conv_end - conv_start:.2f} seconds")
    
    print(f"\n{'='*60}")
    print("Step 2: Starting Project Analysis")
    print(f"{'='*60}\n")
    analyzer = ExecAnalyzer(input_path=args.input_path, output_path=args.output_path)
    analysis_start = time.time()
    analyzer.run()
    analysis_end = time.time()
    print(f"\n[TIMING] Total analysis took: {analysis_end - analysis_start:.2f} seconds")
