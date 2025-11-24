"""
Test Reporter per i test unittest originali
Cattura i risultati dei test e li scrive in formato Markdown
"""
import unittest
import json
from datetime import datetime
from pathlib import Path


class MarkdownTestResult(unittest.TextTestResult):
    """Estensione di TextTestResult che cattura i risultati per il report"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []
        self.start_time = datetime.now()
    
    def startTest(self, test):
        """Chiamato quando inizia un test"""
        super().startTest(test)
        self.current_test_start = datetime.now()
    
    def addSuccess(self, test):
        """Chiamato quando un test passa"""
        super().addSuccess(test)
        self._record_result(test, '✅ PASS', None)
    
    def addError(self, test, err):
        """Chiamato quando un test ha un errore"""
        super().addError(test, err)
        error_msg = self._format_error(err)
        self._record_result(test, '❌ FAIL', error_msg)
    
    def addFailure(self, test, err):
        """Chiamato quando un test fallisce"""
        super().addFailure(test, err)
        error_msg = self._format_error(err)
        self._record_result(test, '❌ FAIL', error_msg)
    
    def addSkip(self, test, reason):
        """Chiamato quando un test viene saltato"""
        super().addSkip(test, reason)
        self._record_result(test, '⏭️ SKIP', reason)
    
    def _format_error(self, err):
        """Formatta l'errore per il report"""
        import traceback
        exc_type, exc_value, exc_tb = err
        error_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        return ''.join(error_lines[:10])  # Prime 10 righe
    
    def _record_result(self, test, result, error):
        """Registra il risultato del test"""
        # Calcola durata se possibile
        if hasattr(self, 'current_test_start'):
            duration = (datetime.now() - self.current_test_start).total_seconds()
        else:
            duration = 0.0
        
        # Estrae informazioni dal test
        test_method = test._testMethodName if hasattr(test, '_testMethodName') else 'unknown'
        test_class = test.__class__.__name__ if hasattr(test, '__class__') else 'unknown'
        
        # Determina codice e descrizione
        code, description, suite = self._parse_test_info(test_class, test_method)
        
        self.test_results.append({
            'suite': suite,
            'code': code,
            'name': description,
            'result': result,
            'duration': duration,
            'error': error or '',
            'class': test_class,
            'method': test_method
        })
    
    def _parse_test_info(self, test_class, test_method):
        """Estrae codice, descrizione e suite dal nome del test"""
        suite_name = ""
        test_code = ""
        description = ""
        
        # Test di Exec Analysis
        if 'TestCase' in test_class and 'ExecAnalysis' not in test_class:
            suite_name = "Exec Analysis Tests"
            # Estrae il numero (es. TestCase0 -> 0)
            num = ''.join(filter(str.isdigit, test_class))
            test_code = f"EA_{num}" if num else "EA_XX"
            description = self._get_ea_description(num)
        
        # Test di Cloner
        elif 'Cloner' in test_class:
            suite_name = "Cloner Tests"
            # Estrae il numero (es. TestClonerCase0 -> 0)
            if 'Case' in test_class:
                num = ''.join(filter(str.isdigit, test_class.split('Case')[-1]))
                test_code = f"CL_{num}" if num else "CL_XX"
                description = self._get_cl_description(num)
            else:
                test_code = "CL_XX"
                description = "Cloner test"
        else:
            suite_name = "Altri Test"
            test_code = "OT_XX"
            description = test_method.replace('test_', '').replace('_', ' ').capitalize()
        
        return test_code, description, suite_name
    
    def _get_ea_description(self, num):
        """Restituisce la descrizione del test EA"""
        descriptions = {
            '0': "Directory input non esistente",
            '1': "Directory input vuota",
            '2': "Singolo progetto ML producer",
            '3': "Singolo progetto ML consumer",
            '4': "Progetto producer e consumer",
            '5': "Progetti senza pattern ML",
            '6': "Un producer e un consumer",
            '7': "Solo consumer (multipli)",
            '8': "Multipli producer, un consumer",
            '9': "Multipli producer e consumer"
        }
        return descriptions.get(num, f"Test case {num}")
    
    def _get_cl_description(self, num):
        """Restituisce la descrizione del test CL"""
        descriptions = {
            '0': "File CSV non esistente",
            '1': "File CSV vuoto",
            '2': "Singola repository",
            '3': "Multiple repository"
        }
        return descriptions.get(num, f"Test case {num}")


class MarkdownTestRunner(unittest.TextTestRunner):
    """Test runner che usa MarkdownTestResult e genera il report"""
    
    resultclass = MarkdownTestResult
    
    def __init__(self, output_file=None, **kwargs):
        super().__init__(**kwargs)
        self.output_file = output_file or "ORIGINAL_TEST_RESULTS.md"
    
    def run(self, test):
        """Esegue i test e genera il report"""
        result = super().run(test)
        
        if hasattr(result, 'test_results'):
            self._write_markdown_report(result)
        
        return result
    
    def _write_markdown_report(self, result):
        """Scrive il report in Markdown"""
        # Determina il percorso del file
        if Path.cwd().name in ['exec_analysis_test', 'cloner_test']:
            # Siamo in una sottodirectory, risali
            report_dir = Path.cwd().parent
        else:
            report_dir = Path.cwd()
        
        report_file = report_dir / self.output_file
        temp_file = report_dir / ".original_test_results_temp.json"
        
        # Carica risultati precedenti
        all_results = []
        if temp_file.exists():
            try:
                with open(temp_file, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
            except:
                pass
        
        # Aggiungi nuovi risultati
        all_results.extend(result.test_results)
        
        # Salva risultati accumulati
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        # Raggruppa per suite
        suites = {}
        for test in all_results:
            suite = test['suite']
            if suite not in suites:
                suites[suite] = []
            suites[suite].append(test)
        
        # Genera contenuto
        content = self._generate_markdown_content(suites, all_results, result.start_time)
        
        # Scrivi file
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\nReport Markdown generato: {report_file}")
    
    def _generate_markdown_content(self, suites, all_results, start_time):
        """Genera il contenuto Markdown"""
        lines = []
        
        # Intestazione
        lines.append("# Report Test Funzionali MARK-Tool (Originali)")
        lines.append("")
        lines.append(f"**Data Esecuzione:** {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
        lines.append("")
        
        # Sommario
        total_tests = len(all_results)
        passed = sum(1 for t in all_results if '✅' in t['result'])
        failed = sum(1 for t in all_results if '❌' in t['result'])
        skipped = sum(1 for t in all_results if '⏭️' in t['result'])
        
        lines.append("## Sommario")
        lines.append("")
        lines.append(f"- **Test Totali:** {total_tests}")
        lines.append(f"- **Passati:** {passed} ✅")
        lines.append(f"- **Falliti:** {failed} ❌")
        lines.append(f"- **Saltati:** {skipped} ⏭️")
        
        if total_tests > 0:
            success_rate = (passed / total_tests) * 100
            lines.append(f"- **Tasso di Successo:** {success_rate:.1f}%")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Tabelle per suite
        for suite_name in ["Exec Analysis Tests", "Cloner Tests", "Altri Test"]:
            if suite_name not in suites:
                continue
            
            tests = suites[suite_name]
            
            lines.append(f"## {suite_name}")
            lines.append("")
            
            # Intestazione tabella
            lines.append("| Codice Test | Descrizione | Risultato | Durata |")
            lines.append("|-------------|-------------|-----------|---------|")
            
            # Ordina per codice
            tests.sort(key=lambda x: x['code'])
            
            # Righe tabella
            for test in tests:
                code = test['code']
                name = test['name']
                result = test['result']
                duration = f"{test['duration']:.3f}s"
                
                lines.append(f"| {code} | {name} | {result} | {duration} |")
            
            lines.append("")
            
            # Errori
            failed_tests = [t for t in tests if '❌' in t['result']]
            if failed_tests:
                lines.append(f"### ❌ Errori in {suite_name}")
                lines.append("")
                
                for test in failed_tests:
                    lines.append(f"**{test['code']} - {test['name']}**")
                    if test['error']:
                        lines.append("```")
                        lines.append(test['error'][:500])  # Limita lunghezza
                        lines.append("```")
                    lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Footer
        lines.append("## Note")
        lines.append("")
        lines.append("- ✅ PASS: Test superato con successo")
        lines.append("- ❌ FAIL: Test fallito")
        lines.append("- ⏭️ SKIP: Test saltato")
        lines.append("")
        lines.append("## Descrizione Test")
        lines.append("")
        lines.append("### Exec Analysis Tests (EA_X)")
        lines.append("Test funzionali per `exec_analysis.py` - analisi di progetti ML per identificare producer e consumer.")
        lines.append("")
        lines.append("### Cloner Tests (CL_X)")
        lines.append("Test funzionali per `cloner.py` - clonazione di repository GitHub da file CSV.")
        lines.append("")
        lines.append(f"*Report generato automaticamente il {datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')}*")
        
        return '\n'.join(lines)
