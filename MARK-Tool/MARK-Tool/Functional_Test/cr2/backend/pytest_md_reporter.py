"""
Plugin Pytest per Report in Markdown - CR2 Analytics Dashboard
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
            
            # Mappa file -> suite per CR2
            if 'test_analytics_service' in test_file:
                suite_name = "Analytics Service Unit Tests"
                test_code = self._generate_test_code('AS', test_function)
            elif 'test_analytics_routes' in test_file or 'test_analytics_api' in test_file:
                suite_name = "Analytics API Tests"
                test_code = self._generate_test_code('API', test_function)
            elif 'test_integration' in test_file:
                suite_name = "Integration Tests"
                test_code = self._generate_test_code('INT', test_function)
            else:
                suite_name = "Other Tests"
                test_code = "TC-O??"
            
            # Genera nome leggibile dal nome della funzione
            test_name = self._humanize_test_name(test_function)
        
        return test_code, test_name, suite_name
    
    def _generate_test_code(self, prefix, test_function):
        """Genera il codice del test basato sul mapping esplicito per CR2"""
        # Mapping esplicito dei test ai loro codici per CR2
        # Based on MARK-Tool-CR2-Test-Plan.md
        test_mapping = {
            # Analytics Service Unit Tests (TC-AS-01 to TC-AS-20)
            'test_validate_output_path_valid': 'TC-AS-01',
            'test_validate_output_path_invalid': 'TC-AS-02',
            'test_validate_output_path_not_directory': 'TC-AS-03',
            'test_validate_output_path_missing_csv': 'TC-AS-04',
            'test_get_summary': 'TC-AS-05',
            'test_get_summary_unique_projects': 'TC-AS-06',
            'test_get_summary_unique_libraries': 'TC-AS-07',
            'test_get_consumer_producer_distribution': 'TC-AS-08',
            'test_get_consumer_producer_distribution_empty': 'TC-AS-09',
            'test_get_top_keywords': 'TC-AS-10',
            'test_get_top_keywords_limit_respected': 'TC-AS-11',
            'test_get_top_keywords_empty_dataset': 'TC-AS-12',
            'test_get_library_distribution': 'TC-AS-13',
            'test_get_library_distribution_limit_respected': 'TC-AS-14',
            'test_get_filtered_results_by_type': 'TC-AS-15',
            'test_get_filtered_results_by_type_producer': 'TC-AS-16',
            'test_get_filtered_results_by_keyword': 'TC-AS-17',
            'test_get_filtered_results_by_library': 'TC-AS-18',
            'test_get_filtered_results_multiple_filters': 'TC-AS-19',
            'test_get_filtered_results_limit_respected': 'TC-AS-20',
            'test_empty_csv_handling': 'TC-AS-09',  # Duplicate of TC-AS-09
            
            # Analytics API Tests (TC-ANA-01 to TC-ANA-30)
            'test_summary_valid_output_path': 'TC-ANA-01',
            'test_summary_missing_output_path': 'TC-ANA-02',
            'test_summary_nonexistent_path': 'TC-ANA-03',
            'test_summary_missing_csv_files': 'TC-ANA-04',
            'test_summary_correct_values': 'TC-ANA-05',
            'test_distribution_valid_output_path': 'TC-ANA-06',
            'test_distribution_missing_output_path': 'TC-ANA-07',
            'test_distribution_correct_percentages': 'TC-ANA-08',
            'test_distribution_empty_dataset': 'TC-ANA-09',
            'test_distribution_only_consumers': 'TC-ANA-10',
            'test_keywords_default_limit': 'TC-ANA-11',
            'test_keywords_custom_limit': 'TC-ANA-12',
            'test_keywords_boundary_limit_1': 'TC-ANA-13',
            'test_keywords_boundary_limit_100': 'TC-ANA-14',
            'test_keywords_invalid_limit_low': 'TC-ANA-15',
            'test_keywords_invalid_limit_high': 'TC-ANA-16',
            'test_libraries_default_limit': 'TC-ANA-17',
            'test_libraries_custom_limit': 'TC-ANA-18',
            'test_libraries_boundary_limit_1': 'TC-ANA-19',
            'test_libraries_boundary_limit_100': 'TC-ANA-20',
            'test_libraries_invalid_limit_low': 'TC-ANA-21',
            'test_libraries_invalid_limit_high': 'TC-ANA-22',
            'test_filter_type_consumer': 'TC-ANA-23',
            'test_filter_type_producer': 'TC-ANA-24',
            'test_filter_invalid_type': 'TC-ANA-25',
            'test_filter_by_keyword': 'TC-ANA-26',
            'test_filter_by_library': 'TC-ANA-27',
            'test_filter_multiple_filters': 'TC-ANA-28',
            'test_filter_limit_boundary': 'TC-ANA-29',
            'test_health_check': 'TC-ANA-30',
            
            # Integration Tests (TC-INT-ANA-01 to TC-INT-ANA-04)
            'test_complete_analytics_workflow': 'TC-INT-ANA-01',
            'test_filter_and_visualization_workflow': 'TC-INT-ANA-02',
            'test_empty_dataset_handling': 'TC-INT-ANA-03',
            'test_large_dataset_performance': 'TC-INT-ANA-04',
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
        report_dir = Path(__file__).parent
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
        lines.append("# Report Test CR2 - Analytics Dashboard")
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
        suite_order = ["Analytics Service Unit Tests", "Analytics API Tests", "Integration Tests", "Other Tests"]
        
        for suite_name in suite_order:
            if suite_name not in suites:
                continue
            
            tests = suites[suite_name]
            
            # Traduzione dei nomi delle suite in italiano
            italian_names = {
                "Analytics Service Unit Tests": "Test Unitari AnalyticsService",
                "Analytics API Tests": "Test API Analytics",
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
