"""
Configurazione pytest per i test originali
Genera report in Markdown per i test unittest
"""
import pytest
import os
import json
from pathlib import Path
from datetime import datetime


class MarkdownReporterOriginal:
    """Reporter che cattura i risultati dei test unittest e li scrive in Markdown"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def pytest_sessionstart(self, session):
        """Chiamato all'inizio della sessione"""
        self.start_time = datetime.now()
        self.test_results = []
    
    def pytest_runtest_logreport(self, report):
        """Cattura i risultati dei test"""
        if report.when == 'call' or (report.when == 'setup' and report.outcome == 'skipped'):
            test_info = self._extract_test_info(report)
            self.test_results.append(test_info)
    
    def _extract_test_info(self, report):
        """Estrae le informazioni dal report"""
        nodeid = report.nodeid
        parts = nodeid.split("::")
        
        # Determina il tipo di test e il codice
        test_code, test_name, suite_name = self._parse_test_name(parts)
        
        # Determina il risultato
        outcome = getattr(report, 'outcome', None)
        if outcome == 'passed' or report.passed:
            result = "✅ PASS"
        elif outcome == 'failed' or report.failed:
            result = "❌ FAIL"
        elif outcome == 'skipped' or report.skipped:
            result = "⏭️ SKIP"
        else:
            result = "❓ UNKNOWN"
        
        # Errore se presente
        error_details = ""
        if report.failed and hasattr(report, 'longrepr'):
            error_details = str(report.longrepr)[:300]
        
        return {
            'suite': suite_name,
            'code': test_code,
            'name': test_name,
            'result': result,
            'duration': report.duration,
            'error': error_details,
            'nodeid': nodeid
        }
    
    def _parse_test_name(self, parts):
        """Determina codice, nome e suite del test"""
        suite_name = ""
        test_code = ""
        test_name = ""
        
        if len(parts) >= 2:
            class_name = parts[1] if len(parts) > 1 else ""
            
            # Determina la suite basandosi sul nome della classe
            if 'TestCase' in class_name or 'ExecAnalysis' in str(parts):
                suite_name = "Exec Analysis Tests"
                # Estrae il numero del test case (es. TestCase0 -> EA_0)
                if 'TestCase' in class_name:
                    num = ''.join(filter(str.isdigit, class_name))
                    test_code = f"EA_{num}" if num else "EA_XX"
                    test_name = self._get_ea_test_description(num)
                else:
                    test_code = "EA_XX"
                    test_name = "Exec analysis test"
            
            elif 'TestCloner' in class_name or 'Cloner' in str(parts):
                suite_name = "Cloner Tests"
                # Estrae il numero del test case (es. TestClonerCase0 -> CL_0)
                if 'Case' in class_name:
                    num = ''.join(filter(str.isdigit, class_name))
                    test_code = f"CL_{num}" if num else "CL_XX"
                    test_name = self._get_cl_test_description(num)
                else:
                    test_code = "CL_XX"
                    test_name = "Cloner test"
            else:
                suite_name = "Altri Test"
                test_code = "OT_XX"
                test_name = "Test generico"
        
        return test_code, test_name, suite_name
    
    def _get_ea_test_description(self, num):
        """Restituisce la descrizione del test EA basata sul numero"""
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
    
    def _get_cl_test_description(self, num):
        """Restituisce la descrizione del test CL basata sul numero"""
        descriptions = {
            '0': "File CSV non esistente",
            '1': "File CSV vuoto",
            '2': "Singola repository",
            '3': "Multiple repository"
        }
        return descriptions.get(num, f"Test case {num}")
    
    def pytest_sessionfinish(self, session):
        """Chiamato alla fine della sessione"""
        self.end_time = datetime.now()
        self._write_markdown_report()
    
    def _write_markdown_report(self):
        """Scrive il report in Markdown"""
        report_dir = Path(__file__).parent
        report_file = report_dir / "ORIGINAL_TEST_RESULTS.md"
        temp_file = report_dir / ".original_test_results_temp.json"
        
        # Carica risultati precedenti se esistono
        all_results = []
        if temp_file.exists():
            try:
                with open(temp_file, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
            except:
                pass
        
        # Aggiungi nuovi risultati
        all_results.extend(self.test_results)
        
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
        content = self._generate_markdown_content(suites, all_results)
        
        # Scrivi file
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n📝 Report Markdown generato: {report_file}")
    
    def _generate_markdown_content(self, suites, all_results):
        """Genera il contenuto Markdown"""
        lines = []
        
        # Intestazione
        lines.append("# Report Test Funzionali MARK-Tool (Originali)")
        lines.append("")
        
        if self.start_time:
            lines.append(f"**Data Esecuzione:** {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            lines.append(f"**Data Esecuzione:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            lines.append(f"**Durata Totale:** {duration:.2f}s")
        
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
                        lines.append(test['error'])
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


@pytest.fixture(scope='session', autouse=True)
def markdown_reporter_original(request):
    """Fixture che registra il reporter Markdown"""
    reporter = MarkdownReporterOriginal()
    request.config.pluginmanager.register(reporter)
    yield reporter
