"""
Plugin Pytest per Report in Markdown
Genera un report in formato Markdown con i risultati dei test
"""
import pytest
import json
import os
from datetime import datetime
from pathlib import Path


class MarkdownReporter:
    """Reporter che cattura e scrive i risultati dei test in formato Markdown"""
    
    def __init__(self):
        self.test_results = []
        self.test_suite_name = ""
        self.start_time = None
        self.end_time = None
    
    def pytest_sessionstart(self, session):
        """Chiamato all'inizio della sessione di test"""
        self.start_time = datetime.now()
        self.test_results = []
    
    def pytest_runtest_logreport(self, report):
        """Chiamato per ogni fase del test (setup, call, teardown)"""
        if report.when == 'call' or (report.when == 'setup' and report.outcome == 'skipped'):
            # Solo la fase principale del test o setup skippati
            # Estrai informazioni dal test
            test_info = self._extract_test_info(report)
            self.test_results.append(test_info)
    
    def _extract_test_info(self, report):
        """Estrae le informazioni dal report del test"""
        # Ottieni il nome del modulo e del test
        nodeid = report.nodeid
        
        # Estrai il file di test e il nome della funzione
        parts = nodeid.split("::")
        test_file = Path(parts[0]).stem if parts else "unknown"
        
        # Determina il codice del test e la categoria
        test_code, test_name, suite_name = self._parse_test_name(parts, test_file)
        
        # Estrai i parametri se presenti
        parameters = self._extract_parameters(report)
        
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
        
        # Aggiungi dettagli dell'errore se presente
        error_details = ""
        if report.failed and hasattr(report, 'longrepr'):
            error_details = str(report.longrepr)[:200]  # Primi 200 caratteri
        
        return {
            'suite': suite_name,
            'code': test_code,
            'name': test_name,
            'parameters': parameters,
            'result': result,
            'duration': report.duration,
            'error': error_details,
            'nodeid': nodeid
        }
    
    def _parse_test_name(self, parts, test_file):
        """Determina il codice del test, nome e suite basandosi sul file"""
        suite_name = ""
        test_code = ""
        test_name = ""
        
        if len(parts) >= 2:
            full_name = parts[-1]
            
            # Rimuovi i parametri se presenti
            if '[' in full_name:
                test_function = full_name[:full_name.index('[')]
            else:
                test_function = full_name
            
            # Mappa file -> suite
            if 'test_analysis_routes' in test_file:
                suite_name = "Analysis Routes"
                test_code = self._generate_test_code('A', test_function)
            elif 'test_file_routes' in test_file:
                suite_name = "File Routes"
                test_code = self._generate_test_code('F', test_function)
            elif 'test_results_routes' in test_file:
                suite_name = "Results Routes"
                test_code = self._generate_test_code('R', test_function)
            elif 'test_integration' in test_file:
                suite_name = "Integration Tests"
                test_code = self._generate_test_code('I', test_function)
            else:
                suite_name = "Other Tests"
                test_code = "TC-O??"
            
            # Genera nome leggibile dal nome della funzione
            test_name = self._humanize_test_name(test_function)
        
        return test_code, test_name, suite_name
    
    def _generate_test_code(self, prefix, test_function):
        """Genera il codice del test (es. TC-A01) basato sul mapping esplicito"""
        # Mapping esplicito dei test ai loro codici
        test_mapping = {
            # Analysis Routes (TC-A01 to TC-A09)
            'test_start_analysis_valid': 'TC-A01',  # TC-A01 e TC-A04
            'test_start_analysis_missing_fields': 'TC-A02',  # TC-A02 e TC-A03
            'test_start_analysis_no_data': 'TC-A02',
            'test_get_job_status_existing': 'TC-A05',
            'test_get_job_status_nonexistent': 'TC-A06',
            'test_list_jobs': 'TC-A07',
            'test_list_jobs_empty': 'TC-A07',
            'test_cancel_job': 'TC-A08',
            'test_cancel_nonexistent_job': 'TC-A08',
            'test_get_job_logs': 'TC-A09',
            'test_get_job_logs_with_limit': 'TC-A09',
            'test_get_logs_nonexistent_job': 'TC-A09',
            
            # File Routes (TC-F01 to TC-F11)
            'test_upload_file_with_extension': 'TC-F01',  # TC-F01 e TC-F02
            'test_upload_file_no_file': 'TC-F03',
            'test_upload_file_empty_filename': 'TC-F03',
            'test_validate_input_folder_existing': 'TC-F04',
            'test_validate_input_folder_nonexistent': 'TC-F05',
            'test_validate_input_folder_missing_path': 'TC-F06',
            'test_validate_output_folder_valid': 'TC-F07',
            'test_validate_output_folder_creatable': 'TC-F07',
            'test_validate_output_folder_missing_path': 'TC-F07',
            'test_validate_csv_valid': 'TC-F08',
            'test_validate_csv_nonexistent': 'TC-F08',
            'test_validate_csv_missing_filepath': 'TC-F08',
            'test_download_file_existing': 'TC-F09',
            'test_download_file_nonexistent': 'TC-F10',
            'test_download_file_missing_filepath': 'TC-F10',
            'test_download_directory_instead_of_file': 'TC-F10',
            'test_list_files': 'TC-F11',
            'test_list_files_empty_directory': 'TC-F11',
            'test_list_files_missing_directory': 'TC-F11',
            'test_list_files_nonexistent_directory': 'TC-F11',
            
            # Results Routes (TC-R01 to TC-R12)
            'test_list_results_valid_path': 'TC-R01',
            'test_list_results_missing_path': 'TC-R02',
            'test_list_results_nonexistent_path': 'TC-R03',
            'test_view_csv_valid': 'TC-R04',
            'test_view_csv_with_pagination': 'TC-R05',
            'test_view_csv_missing_filepath': 'TC-R06',
            'test_view_csv_nonexistent_file': 'TC-R07',
            'test_get_results_statistics': 'TC-R08',
            'test_get_stats_missing_path': 'TC-R08',
            'test_get_stats_nonexistent_path': 'TC-R08',
            'test_search_results_valid_query': 'TC-R09',
            'test_search_results_with_column_filter': 'TC-R10',
            'test_search_results_no_matches': 'TC-R10',
            'test_search_results_missing_filepath': 'TC-R11',
            'test_search_results_missing_query': 'TC-R12',
            'test_search_results_invalid_filepath': 'TC-R12',
            'test_search_results_invalid_column': 'TC-R12',
            
            # Integration Tests (TC-INT-01 to TC-INT-06)
            'test_analysis_e2e_without_cloner': 'TC-INT-01',
            'test_analysis_e2e_with_cloner': 'TC-INT-02',
            'test_concurrent_jobs': 'TC-INT-03',
            'test_job_cancellation_workflow': 'TC-INT-04',
            'test_invalid_input_path_handling': 'TC-INT-05',
            'test_malformed_csv_handling': 'TC-INT-06',
            'test_results_workflow_with_search': 'TC-INT-07',
            'test_file_upload_and_download_workflow': 'TC-INT-08',
            'test_health_check_endpoint': 'TC-INT-09',
            'test_root_endpoint_documentation': 'TC-INT-10',
        }
        
        # Cerca nel mapping
        if test_function in test_mapping:
            return test_mapping[test_function]
        
        # Fallback: usa il prefisso con numero generico
        import re
        numbers = re.findall(r'\d+', test_function)
        if numbers:
            num = numbers[0].zfill(2)
            return f"TC-{prefix}{num}"
        
        # Ultimo fallback
        return f"TC-{prefix}XX"
    
    def _humanize_test_name(self, test_function):
        """Converte il nome della funzione in un nome leggibile"""
        # Rimuovi "test_" dal prefisso
        name = test_function.replace('test_', '')
        
        # Sostituisci underscore con spazi
        name = name.replace('_', ' ')
        
        # Capitalizza
        name = name.capitalize()
        
        return name
    
    def _extract_parameters(self, report):
        """Estrae i parametri dal test parametrizzato"""
        # Cerca parametri nel nodeid
        nodeid = report.nodeid
        
        if '[' in nodeid and ']' in nodeid:
            param_str = nodeid[nodeid.index('[') + 1:nodeid.index(']')]
            # Limita la lunghezza dei parametri
            if len(param_str) > 50:
                param_str = param_str[:47] + "..."
            return param_str
        
        return "N/A"
    
    def pytest_sessionfinish(self, session):
        """Chiamato alla fine della sessione di test"""
        self.end_time = datetime.now()
        self._write_markdown_report()
    
    def _write_markdown_report(self):
        """Scrive il report in formato Markdown"""
        # Determina il percorso del file
        report_dir = Path(__file__).parent.parent
        report_file = report_dir / "TEST_RESULTS.md"
        temp_file = report_dir / ".test_results_temp.json"
        
        # Carica i risultati precedenti se esistono
        all_results = []
        if temp_file.exists():
            try:
                with open(temp_file, 'r', encoding='utf-8') as f:
                    import json
                    all_results = json.load(f)
            except:
                pass
        
        # Aggiungi i nuovi risultati
        all_results.extend(self.test_results)
        
        # Salva i risultati accumulati
        with open(temp_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        # Raggruppa i test per suite
        suites = {}
        for test in all_results:
            suite = test['suite']
            if suite not in suites:
                suites[suite] = []
            suites[suite].append(test)
        
        # Genera il contenuto Markdown
        content = self._generate_markdown_content(suites, all_results)
        
        # Scrivi il file
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n📝 Report Markdown generato: {report_file}")
    
    def _generate_markdown_content(self, suites, all_results=None):
        """Genera il contenuto del file Markdown"""
        if all_results is None:
            all_results = self.test_results
            
        lines = []
        
        # Intestazione
        lines.append("# Report Test Backend MARK-Tool")
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
        
        # Tabelle per ogni suite
        suite_order = ["Analysis Routes", "File Routes", "Results Routes", "Integration Tests", "Other Tests"]
        
        for suite_name in suite_order:
            if suite_name not in suites:
                continue
            
            tests = suites[suite_name]
            
            # Traduzione dei nomi delle suite in italiano
            italian_names = {
                "Analysis Routes": "Route di Analisi",
                "File Routes": "Route dei File",
                "Results Routes": "Route dei Risultati",
                "Integration Tests": "Test di Integrazione",
                "Other Tests": "Altri Test"
            }
            
            lines.append(f"## {italian_names.get(suite_name, suite_name)}")
            lines.append("")
            
            # Intestazione tabella
            lines.append("| Codice Test | Nome Test | Parametri | Risultato | Durata |")
            lines.append("|-------------|-----------|-----------|-----------|---------|")
            
            # Ordina i test per codice
            tests.sort(key=lambda x: x['code'])
            
            # Righe della tabella
            for test in tests:
                code = test['code']
                name = test['name']
                params = test['parameters']
                result = test['result']
                duration = f"{test['duration']:.3f}s"
                
                # Limita la lunghezza del nome
                if len(name) > 60:
                    name = name[:57] + "..."
                
                lines.append(f"| {code} | {name} | {params} | {result} | {duration} |")
            
            lines.append("")
            
            # Dettagli degli errori per questa suite
            failed_tests = [t for t in tests if '❌' in t['result']]
            if failed_tests:
                lines.append(f"### ❌ Errori in {italian_names.get(suite_name, suite_name)}")
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
        lines.append(f"*Report generato automaticamente il {datetime.now().strftime('%d/%m/%Y alle %H:%M:%S')}*")
        
        return '\n'.join(lines)


@pytest.fixture(scope='session', autouse=True)
def markdown_reporter(request):
    """Fixture che registra il reporter Markdown"""
    reporter = MarkdownReporter()
    
    # Registra gli hook
    request.config.pluginmanager.register(reporter)
    
    yield reporter
    
    # Il reporter viene automaticamente deregistrato da pytest
