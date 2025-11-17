#!/usr/bin/env python3
"""
Script per eseguire i test funzionali originali di MARK-Tool
Genera un report in formato Markdown
"""
import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """Stampa intestazione formattata"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_command(cmd, description):
    """Esegue un comando e restituisce il risultato"""
    print(f"Esecuzione: {description}")
    print(f"Comando: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Mostra output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        print(f"[OK] {description} - PASSATO\n")
        return True
    else:
        print(f"[X] {description} - FALLITO\n")
        return False


def main():
    """Esegue i test funzionali originali"""
    # Directory dello script
    script_dir = Path(__file__).parent
    
    # Pulisci risultati temporanei precedenti
    temp_results = script_dir / '.original_test_results_temp.json'
    if temp_results.exists():
        temp_results.unlink()
        print("[OK] Risultati precedenti rimossi\n")
    
    # Cambia directory
    os.chdir(script_dir)
    
    print_header("Test Funzionali MARK-Tool - Suite Originale")
    print("Test di Exec Analysis e Cloner")
    print(f"Directory: {script_dir}\n")
    
    results = []
    
    # Test 1: Exec Analysis
    print_header("Suite 1/2: Exec Analysis Tests (10 test)")
    os.chdir(script_dir / 'exec_analysis_test')
    results.append(run_command(
        [sys.executable, 'exec_analysis_test.py'],
        "Test Exec Analysis"
    ))
    os.chdir(script_dir)
    
    # Test 2: Cloner
    print_header("Suite 2/2: Cloner Tests (4 test)")
    os.chdir(script_dir / 'cloner_test')
    results.append(run_command(
        [sys.executable, 'cloner_test.py'],
        "Test Cloner"
    ))
    os.chdir(script_dir)
    
    # Sommario
    print_header("Riepilogo Esecuzione Test")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Suite Test: {passed}/{total} passate")
    
    suite_names = [
        "Exec Analysis Tests",
        "Cloner Tests"
    ]
    
    for i, result in enumerate(results):
        status = "✅ PASSATO" if result else "❌ FALLITO"
        print(f"  Suite {i + 1}: {suite_names[i]} - {status}")
    
    print("\n" + "=" * 80)
    
    if all(results):
        print("\n[OK] Tutte le suite di test sono PASSATE!\n")
        return 0
    else:
        print("\n[X] Alcune suite di test sono FALLITE\n")
        print("Esegui le suite individualmente con:")
        print("  pytest <directory>/test_file.py -v")
        print("\nPer output dettagliato:")
        print("  pytest <directory>/test_file.py -vv --tb=long")
        return 1


if __name__ == '__main__':
    sys.exit(main())
