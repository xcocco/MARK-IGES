"""
Test script to verify context builder is extracting correct project names
"""
import sys
sys.path.insert(0, r'c:\Users\turco\Desktop\IGES\MARK-IGES\MARK-Tool\MARK-Tool\web_gui')

from services.context_builder_service import ContextBuilderService

# Test with actual output path
output_path = r"C:\Users\turco\Desktop\IGES\output"
input_path = r"C:\Users\turco\Desktop\IGES\input"

print("=" * 80)
print("Testing build_all_projects_context")
print("=" * 80)

all_projects = ContextBuilderService.build_all_projects_context(output_path, input_path)

print(f"\nTotal projects found: {all_projects['total_count']}")
print(f"Producer count: {all_projects['producer_count']}")
print(f"Consumer count: {all_projects['consumer_count']}")
print("\n" + "=" * 80)
print("PROJECTS LIST:")
print("=" * 80)

for idx, project in enumerate(all_projects['projects'][:10], 1):  # Show first 10
    print(f"\n{idx}. {project['project_name']}")
    print(f"   Classification: {project['classification']}")
    print(f"   Libraries: {', '.join(project['libraries'][:3])}")
    print(f"   Detections: {project['total_detections']}")

print("\n" + "=" * 80)
print("FORMATTED OUTPUT FOR LLM (first 2000 chars):")
print("=" * 80)

formatted = ContextBuilderService.format_all_projects_for_llm(all_projects)
print(formatted[:2000])
print("\n[... truncated ...]")
