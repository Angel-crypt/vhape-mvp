"""
Summary report generator for Vhape test results.

Generates clear, understandable summaries of test execution.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TestSummary:
    """Generates summary reports for test execution."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None
        self.features = []
        self.scenarios = []
        self.steps = []
        self.security_issues = []
        
    def add_feature(self, feature_name: str, status: str):
        """Add a feature to the summary."""
        self.features.append({
            'name': feature_name,
            'status': status,
            'timestamp': datetime.now()
        })
    
    def add_scenario(self, scenario_name: str, status: str, feature_name: str):
        """Add a scenario to the summary."""
        self.scenarios.append({
            'name': scenario_name,
            'status': status,
            'feature': feature_name,
            'timestamp': datetime.now()
        })
    
    def add_step(self, step_name: str, status: str, error: Optional[str] = None):
        """Add a step to the summary."""
        self.steps.append({
            'name': step_name,
            'status': status,
            'error': error,
            'timestamp': datetime.now()
        })
    
    def add_security_issue(self, message: str, step_name: str, severity: str = 'high'):
        """Add a security issue to the summary."""
        self.security_issues.append({
            'message': message,
            'step': step_name,
            'severity': severity,
            'timestamp': datetime.now()
        })
    
    def finalize(self):
        """Finalize the summary with end time."""
        self.end_time = datetime.now()
    
    def get_statistics(self) -> Dict:
        """Get summary statistics."""
        total_features = len(self.features)
        passed_features = len([f for f in self.features if f['status'] == 'passed'])
        failed_features = total_features - passed_features
        
        total_scenarios = len(self.scenarios)
        passed_scenarios = len([s for s in self.scenarios if s['status'] == 'passed'])
        failed_scenarios = total_scenarios - passed_scenarios
        
        total_steps = len(self.steps)
        passed_steps = len([s for s in self.steps if s['status'] == 'passed'])
        failed_steps = total_steps - passed_steps
        
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        success_rate = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
        
        return {
            'features': {
                'total': total_features,
                'passed': passed_features,
                'failed': failed_features
            },
            'scenarios': {
                'total': total_scenarios,
                'passed': passed_scenarios,
                'failed': failed_scenarios
            },
            'steps': {
                'total': total_steps,
                'passed': passed_steps,
                'failed': failed_steps
            },
            'security_issues': len(self.security_issues),
            'duration': duration,
            'success_rate': success_rate
        }
    
    def print_summary(self):
        """Print a formatted summary to console."""
        stats = self.get_statistics()
        
        print("\n" + "=" * 60)
        print("  VHAPE - Security Test Summary")
        print("=" * 60)
        
        # Features
        print(f"\n📋 Features:")
        print(f"   Total:    {stats['features']['total']}")
        print(f"   ✅ Passed: {stats['features']['passed']}")
        print(f"   ❌ Failed: {stats['features']['failed']}")
        
        # Scenarios
        print(f"\n🎯 Scenarios:")
        print(f"   Total:    {stats['scenarios']['total']}")
        print(f"   ✅ Passed: {stats['scenarios']['passed']}")
        print(f"   ❌ Failed: {stats['scenarios']['failed']}")
        
        # Steps
        print(f"\n📝 Steps:")
        print(f"   Total:    {stats['steps']['total']}")
        print(f"   ✅ Passed: {stats['steps']['passed']}")
        print(f"   ❌ Failed: {stats['steps']['failed']}")
        
        # Security Issues
        if stats['security_issues'] > 0:
            print(f"\n⚠️  Security Issues Found: {stats['security_issues']}")
            for issue in self.security_issues:
                print(f"   ❌ {issue['message']} (Step: {issue['step']})")
        else:
            print(f"\n✅ No security issues detected")
        
        # Success Rate
        print(f"\n📊 Success Rate: {stats['success_rate']:.1f}%")
        
        # Duration
        print(f"\n⏱️  Duration: {stats['duration']:.2f}s")
        
        print("\n" + "=" * 60 + "\n")
    
    def save_json(self, filepath: Optional[Path] = None):
        """Save summary to JSON file."""
        import json
        
        if filepath is None:
            filepath = Path('tests/results') / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'statistics': self.get_statistics(),
            'features': self.features,
            'scenarios': self.scenarios,
            'security_issues': self.security_issues
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath

