import sys
import os
import subprocess
import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta


# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from vhape.reporting.summary import TestSummary
from tests.e2e.html_report_generator import generate_html_report


def get_available_features(project_root: Path) -> list:
    """Get list of available feature files."""
    features_dir = project_root / 'features'
    feature_files = sorted(features_dir.glob('*.feature'))
    return [f.name for f in feature_files]


def select_features_interactive(project_root: Path) -> list:
    """
    Interactive menu to select which features to run.
    
    Returns:
        List of feature file paths to execute, or None for all features
    """
    available_features = get_available_features(project_root)
    
    if not available_features:
        print("[WARN] No feature files found in features/ directory")
        return None
    
    print("\n" + "=" * 60)
    print("  Select Features to Run")
    print("=" * 60)
    print()
    print("Available features:")
    print()
    
    # Display features with numbers
    for idx, feature in enumerate(available_features, 1):
        print(f"  [{idx}] {feature}")
    
    print()
    print("Options:")
    print("  [0]  Run ALL features")
    print(f"  [1-{len(available_features)}] Select specific feature(s) (comma-separated, e.g., 1,3,5)")
    print("  [q]  Quit")
    print()
    print("Examples:")
    print("  - Enter '0' to run all features")
    print("  - Enter '1' to run only the first feature")
    print("  - Enter '1,3,5' to run features 1, 3, and 5")
    print()
    
    while True:
        try:
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q' or choice == 'quit':
                print("[INFO] Exiting...")
                sys.exit(0)
            
            if choice == '0' or choice == 'all':
                print("\n[INFO] Selected: ALL features")
                return None  # None means run all
            
            # Parse comma-separated numbers
            selected_indices = []
            invalid_selections = []
            
            for part in choice.split(','):
                part = part.strip()
                if part:
                    try:
                        idx = int(part)
                        if 1 <= idx <= len(available_features):
                            # Avoid duplicates
                            idx_0_based = idx - 1
                            if idx_0_based not in selected_indices:
                                selected_indices.append(idx_0_based)
                        else:
                            invalid_selections.append(part)
                    except ValueError:
                        invalid_selections.append(part)
            
            # Check for invalid selections
            if invalid_selections:
                print(f"[ERROR] Invalid selection(s): {', '.join(invalid_selections)}")
                print(f"[INFO] Please choose numbers between 1-{len(available_features)}")
                continue
            
            # All indices were valid
            if selected_indices:
                # Sort indices to maintain order
                selected_indices.sort()
                selected_features = [available_features[i] for i in selected_indices]
                print(f"\n[INFO] Selected {len(selected_features)} feature(s):")
                for feature in selected_features:
                    print(f"  - {feature}")
                return selected_features
            else:
                print("[ERROR] No valid features selected. Please try again.")
        
        except ValueError:
            print("[ERROR] Invalid input. Please enter numbers separated by commas, '0' for all, or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n\n[INFO] Interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}. Please try again.")


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
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Vhape E2E Test Runner - Execute BDD tests and generate reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_e2e_tests.py                    # Interactive mode
  python run_e2e_tests.py --all              # Run all features
  python run_e2e_tests.py --features auth    # Run auth.feature
  python run_e2e_tests.py --features auth,api_security  # Run multiple features
        """
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all features (skip interactive menu)'
    )
    parser.add_argument(
        '--features', '-f',
        type=str,
        help='Comma-separated list of feature names to run (e.g., auth,api_security)'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Force interactive mode (default if no other options)'
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("  VHAPE - Ejecutando Tests y Generando Reportes")
    print("=" * 60)
    
    # Determine which features to run
    selected_features = None
    
    if args.all:
        # Run all features
        print("\n[INFO] Selected: ALL features (--all flag)")
        selected_features = None
    elif args.features:
        # Parse feature names from command line
        feature_names = [f.strip() for f in args.features.split(',')]
        available_features = get_available_features(project_root)
        
        # Validate feature names
        valid_features = []
        for name in feature_names:
            # Try exact match first
            if name in available_features:
                valid_features.append(name)
            # Try with .feature extension
            elif f"{name}.feature" in available_features:
                valid_features.append(f"{name}.feature")
            else:
                print(f"[WARN] Feature '{name}' not found. Available features: {', '.join(available_features)}")
        
        if valid_features:
            selected_features = valid_features
            print(f"\n[INFO] Selected {len(selected_features)} feature(s) from command line:")
            for feature in selected_features:
                print(f"  - {feature}")
        else:
            print("[ERROR] No valid features specified. Exiting...")
            sys.exit(1)
    else:
        # Interactive mode (default)
        selected_features = select_features_interactive(project_root)
    
    print()
    print("=" * 60)
    print("  VHAPE - Ejecutando Tests y Generando Reportes")
    print("=" * 60)
    print()
    
    # Build behave command
    if selected_features is None:
        # Run all features
        behave_args = ['features/']
        print("[INFO] Ejecutando tests de Behave (todas las features)...")
    else:
        # Run selected features
        feature_paths = [f'features/{f}' for f in selected_features]
        behave_args = feature_paths
        print(f"[INFO] Ejecutando tests de Behave ({len(selected_features)} feature(s) seleccionada(s))...")
    
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
        # Execute selected features
        # --no-capture: Show output in real-time
        # stop=False is already set in behave.ini, so it won't stop on first failure
        cmd = [sys.executable, '-m', 'behave', '--no-capture'] + behave_args
        result = subprocess.run(
            cmd,
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
            if '[FAIL]' in line and ('insecure' in line.lower() or 'validation failed' in line.lower()):
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
    
    # Determine the JSON file path
    json_file_path = None
    if summary_json_file and summary_json_file.stat().st_mtime > (datetime.now().timestamp() - 10):
        # Ya tenemos el JSON con los security issues
        json_file_path = summary_json_file
        print(f"[SAVE] JSON Report (with security issues): {json_file_path}")
    else:
        # Guardar JSON desde el parsing (fallback)
        results_dir = Path('tests/results')
        results_dir.mkdir(parents=True, exist_ok=True)
        json_file_path = summary.save_json(results_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        print(f"[SAVE] JSON Report saved to: {json_file_path}")
    
    # Generate HTML report from JSON
    print()
    print("[INFO] Generating HTML report...")
    try:
        html_file = generate_html_report(json_file_path)
        html_absolute = html_file.absolute()
        print(f"[SAVE] HTML Report generated: {html_file}")
        
        # Try to open the report in the default browser
        try:
            import webbrowser
            file_url = f'file:///{html_absolute.as_posix()}'
            webbrowser.open(file_url)
            print(f"[INFO] HTML report opened in your default browser")
        except Exception as browser_error:
            # If browser opening fails, just show the path
            if sys.platform == 'win32':
                print(f"[INFO] Open the report manually: {html_absolute}")
            else:
                print(f"[INFO] Open the report manually: file://{html_absolute}")
    except Exception as e:
        print(f"[FAIL] Error generating HTML report: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())

