#!/usr/bin/env python3
"""
Script principal para ejecutar tests de Behave y generar reportes.

Este script:
1. Ejecuta los tests de Behave
2. Captura y parsea los resultados
3. Genera un reporte completo en JSON
4. Muestra un resumen en consola

Uso:
    python test/run_tests_and_generate_report.py
    # o
    ./test/run_tests_and_generate_report.py
"""

import sys
import os
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from vhape.reporting.summary import TestSummary


def parse_behave_output(output: str) -> dict:
    """Parsea la salida de Behave para extraer estadísticas."""
    stats = {
        'features': {'total': 0, 'passed': 0, 'failed': 0},
        'scenarios': {'total': 0, 'passed': 0, 'failed': 0},
        'steps': {'total': 0, 'passed': 0, 'failed': 0}
    }
    
    # Buscar línea de resumen: "X features passed, Y failed..."
    feature_match = re.search(r'(\d+)\s+features?\s+passed,\s+(\d+)\s+failed', output)
    if feature_match:
        stats['features']['passed'] = int(feature_match.group(1))
        stats['features']['failed'] = int(feature_match.group(2))
        stats['features']['total'] = stats['features']['passed'] + stats['features']['failed']
    
    scenario_match = re.search(r'(\d+)\s+scenarios?\s+passed,\s+(\d+)\s+failed', output)
    if scenario_match:
        stats['scenarios']['passed'] = int(scenario_match.group(1))
        stats['scenarios']['failed'] = int(scenario_match.group(2))
        stats['scenarios']['total'] = stats['scenarios']['passed'] + stats['scenarios']['failed']
    
    step_match = re.search(r'(\d+)\s+steps?\s+passed,\s+(\d+)\s+failed', output)
    if step_match:
        stats['steps']['passed'] = int(step_match.group(1))
        stats['steps']['failed'] = int(step_match.group(2))
        stats['steps']['total'] = stats['steps']['passed'] + stats['steps']['failed']
    
    # Buscar tiempo de ejecución
    time_match = re.search(r'Took\s+(\d+)min\s+([\d.]+)s', output)
    duration = 0.0
    if time_match:
        duration = float(time_match.group(1)) * 60 + float(time_match.group(2))
    
    stats['duration'] = duration
    
    return stats


def extract_features_and_scenarios(output: str) -> list:
    """Extrae features y scenarios del output."""
    features = []
    current_feature = None
    failed_scenarios = set()
    
    # First, identify failed scenarios from the "Failing scenarios:" section
    in_failing_section = False
    for line in output.split('\n'):
        if 'Failing scenarios:' in line:
            in_failing_section = True
            continue
        if in_failing_section:
            if line.strip().startswith('features/'):
                # Extract scenario name from line like "features/failure_scenarios.feature:7  Invalid token..."
                # Format: "features/xxx.feature:LINE  Scenario Name"
                parts = line.strip().split('  ', 1)
                if len(parts) > 1:
                    scenario_name = parts[1].strip()
                    failed_scenarios.add(scenario_name)
            elif line.strip() == '' or line.strip().startswith(('0 features', '1 features', '2 features', '3 features', '4 features', '5 features')):
                in_failing_section = False
    
    # Now extract features and scenarios, marking failed ones
    for line in output.split('\n'):
        # Detectar feature
        if 'Feature:' in line and not line.strip().startswith('#'):
            parts = line.split('Feature:')
            if len(parts) > 1:
                feature_name = parts[1].strip().split('#')[0].strip()
                if current_feature:
                    features.append(current_feature)
                current_feature = {
                    'name': feature_name,
                    'scenarios': [],
                    'status': 'passed'
                }
        # Detectar scenario (con o sin indentación)
        elif 'Scenario:' in line and not line.strip().startswith('#'):
            if current_feature:
                parts = line.split('Scenario:')
                if len(parts) > 1:
                    scenario_name = parts[1].strip().split('#')[0].strip()
                    # Check if this scenario failed
                    scenario_status = 'failed' if scenario_name in failed_scenarios else 'passed'
                    current_feature['scenarios'].append({
                        'name': scenario_name,
                        'status': scenario_status
                    })
    
    if current_feature:
        features.append(current_feature)
    
    return features


def main():
    """Ejecuta tests y genera reporte."""
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("  VHAPE - Ejecutando Tests y Generando Reportes")
    print("=" * 60)
    print()
    
    # Ejecutar behave y capturar output
    print("🔍 Ejecutando tests de Behave...")
    print()
    
    # Behave searches for behave.ini in current directory and parent directories
    # Since behave.ini is in vhape/, we need to copy it to project root temporarily
    import shutil
    behave_ini_source = project_root / 'vhape' / 'behave.ini'
    behave_ini_temp = project_root / 'behave.ini'
    
    # Copy behave.ini to project root temporarily
    if behave_ini_source.exists():
        shutil.copy2(behave_ini_source, behave_ini_temp)
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'behave', 'features/', '--no-capture'],
            cwd=project_root,
            capture_output=True,
            text=True
        )
    finally:
        # Remove temporary behave.ini from project root
        if behave_ini_temp.exists():
            behave_ini_temp.unlink()
    
    output = result.stdout + result.stderr
    
    # Mostrar output
    print(output)
    
    # Parsear resultados
    stats = parse_behave_output(output)
    features = extract_features_and_scenarios(output)
    
    # Try to use the global test_summary instance directly (it has the security issues)
    # Import it after behave has run so it has the updated data
    try:
        from features.steps.environment import test_summary as global_summary
        # Check if it has data (was used by Behave)
        if len(global_summary.features) > 0 or len(global_summary.security_issues) > 0:
            summary = global_summary
            # Ensure it's finalized
            if not summary.end_time:
                summary.finalize()
            use_global = True
        else:
            use_global = False
    except Exception as e:
        use_global = False
    
    # Fallback: Try to read the summary JSON file generated by Behave's after_all hook
    summary_json_file = None
    if not use_global:
        results_dir = Path('tests/results')
        if results_dir.exists():
            # Find the most recent summary JSON file
            json_files = sorted(results_dir.glob('summary_*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
            if json_files:
                summary_json_file = json_files[0]
    
    # Si encontramos un archivo JSON reciente (generado por Behave), usarlo
    # De lo contrario, crear uno nuevo desde el parsing
    if use_global:
        # Use the global summary instance (already has security issues)
        pass  # summary already set above
    elif summary_json_file and summary_json_file.stat().st_mtime > (datetime.now().timestamp() - 10):
        # Leer el JSON generado por Behave (tiene los security issues)
        with open(summary_json_file, 'r') as f:
            json_data = json.load(f)
        
        # Crear summary desde el JSON
        summary = TestSummary()
        summary.start_time = datetime.fromisoformat(json_data['start_time'])
        summary.end_time = datetime.fromisoformat(json_data['end_time']) if json_data.get('end_time') else None
        
        # Cargar features, scenarios, steps y security issues desde JSON
        summary.features = json_data.get('features', [])
        summary.scenarios = json_data.get('scenarios', [])
        summary.steps = json_data.get('steps', [])
        summary.security_issues = json_data.get('security_issues', [])
        
        # Asegurar que está finalizado
        if not summary.end_time:
            summary.finalize()
    else:
        # Crear summary desde el parsing (fallback)
        summary = TestSummary()
        # Ajustar start_time para reflejar la duración real
        if stats['duration'] > 0:
            from datetime import timedelta
            summary.start_time = datetime.now() - timedelta(seconds=stats['duration'])
        
        # Agregar features
        for feature in features:
            # Determine feature status based on its scenarios
            feature_status = 'passed'
            for scenario in feature['scenarios']:
                if scenario['status'] == 'failed':
                    feature_status = 'failed'
                    break
            summary.add_feature(feature['name'], feature_status)
            
            # Agregar scenarios
            for scenario in feature['scenarios']:
                summary.add_scenario(scenario['name'], scenario['status'], feature['name'])
        
        # Agregar steps (estimado basado en statistics)
        # Normalmente hay 3 steps por scenario (Given, When, Then)
        for i in range(stats['steps']['total']):
            status = 'passed' if i < stats['steps']['passed'] else 'failed'
            summary.add_step(f'Step {i+1}', status)
        
        # Extract security issues from output (they're in the error messages)
        # Look for security-related error messages in the output
        seen_issues = set()  # Avoid duplicates
        for line in output.split('\n'):
            if '❌' in line and ('insecure' in line.lower() or 'validation failed' in line.lower()):
                # Extract security issue from error message
                if 'Token validation failed' in line and 'Token validation failed' not in seen_issues:
                    summary.add_security_issue('Token validation failed when it should have passed', 'Failed step', 'high')
                    seen_issues.add('Token validation failed')
                elif 'Unauthorized access allowed' in line and 'Unauthorized access allowed' not in seen_issues:
                    summary.add_security_issue('Unauthorized access allowed when it should be denied', 'Failed step', 'high')
                    seen_issues.add('Unauthorized access allowed')
                elif 'Access denied when it should be allowed' in line and 'Access denied when it should be allowed' not in seen_issues:
                    summary.add_security_issue('Access denied when it should have been allowed', 'Failed step', 'medium')
                    seen_issues.add('Access denied when it should be allowed')
        
        # Ajustar duración en el summary
        summary.end_time = datetime.now()
        if stats['duration'] > 0:
            summary.start_time = summary.end_time - timedelta(seconds=stats['duration'])
        
        summary.finalize()
    
    # Mostrar resumen
    print()
    summary.print_summary()
    
    # Si ya había un JSON generado por Behave y lo usamos, no sobrescribirlo
    # Solo guardar un nuevo JSON si creamos el summary desde el parsing
    if summary_json_file and summary_json_file.stat().st_mtime > (datetime.now().timestamp() - 10):
        # Ya tenemos el JSON con los security issues, solo informar
        print(f"💾 JSON Report (with security issues): {summary_json_file}")
        print()
    else:
        # Guardar JSON desde el parsing (fallback)
        results_dir = Path('tests/results')
        results_dir.mkdir(parents=True, exist_ok=True)
        json_file = summary.save_json(results_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        print(f"💾 JSON Report saved to: {json_file}")
        print()
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())

