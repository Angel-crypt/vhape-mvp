"""
Summary report generator for Vhape test results.

Generates clear, understandable summaries of test execution.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time


class TestSummary:
    """Generates summary reports for test execution."""
    
    @staticmethod
    def _get_local_datetime():
        """
        Get current datetime in local timezone.
        
        Returns a naive datetime object representing the current local time.
        This ensures timestamps are saved and interpreted as local time,
        not UTC or any other timezone.
        
        Uses time.localtime() to explicitly get local time, avoiding any
        timezone configuration issues that might cause datetime.now() to
        return UTC instead of local time.
        """
        # Use time.localtime() to explicitly get local time
        # This ensures we always get the correct local time, even if
        # the system is configured to use UTC or another timezone
        local_time = time.localtime()
        # Get microseconds from time.time() for precision
        current_time = time.time()
        microseconds = int((current_time - int(current_time)) * 1000000)
        
        return datetime(
            local_time.tm_year,
            local_time.tm_mon,
            local_time.tm_mday,
            local_time.tm_hour,
            local_time.tm_min,
            local_time.tm_sec,
            microseconds
        )
    
    def __init__(self):
        self.start_time = self._get_local_datetime()
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
            'timestamp': self._get_local_datetime()
        })
    
    def add_scenario(self, scenario_name: str, status: str, feature_name: str):
        """Add a scenario to the summary."""
        self.scenarios.append({
            'name': scenario_name,
            'status': status,
            'feature': feature_name,
            'timestamp': self._get_local_datetime()
        })
    
    def add_step(self, step_name: str, status: str, error: Optional[str] = None):
        """Add a step to the summary."""
        self.steps.append({
            'name': step_name,
            'status': status,
            'error': error,
            'timestamp': self._get_local_datetime()
        })
    
    def add_security_issue(self, message: str, step_name: str, severity: str = 'high'):
        """Add a security issue to the summary."""
        self.security_issues.append({
            'message': message,
            'step': step_name,
            'severity': severity,
            'timestamp': self._get_local_datetime()
        })
    
    def finalize(self):
        """Finalize the summary with end time."""
        self.end_time = self._get_local_datetime()
    
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
        print(f"\nFeatures:")
        print(f"   Total:    {stats['features']['total']}")
        print(f"   [OK] Passed: {stats['features']['passed']}")
        print(f"   [FAIL] Failed: {stats['features']['failed']}")
        
        # Scenarios
        print(f"\nScenarios:")
        print(f"   Total:    {stats['scenarios']['total']}")
        print(f"   [OK] Passed: {stats['scenarios']['passed']}")
        print(f"   [FAIL] Failed: {stats['scenarios']['failed']}")
        
        # Steps
        print(f"\nSteps:")
        print(f"   Total:    {stats['steps']['total']}")
        print(f"   [OK] Passed: {stats['steps']['passed']}")
        print(f"   [FAIL] Failed: {stats['steps']['failed']}")
        
        # Security Issues
        if stats['security_issues'] > 0:
            print(f"\n[WARN] Security Issues Found: {stats['security_issues']}")
            for issue in self.security_issues:
                print(f"   [FAIL] {issue['message']} (Step: {issue['step']})")
        else:
            print(f"\n[OK] No security issues detected")
        
        # Success Rate
        print(f"\nSuccess Rate: {stats['success_rate']:.1f}%")
        
        # Duration
        print(f"\nDuration: {stats['duration']:.2f}s")
        
        print("\n" + "=" * 60 + "\n")
    
    def save_json(self, filepath: Optional[Path] = None):
        """Save summary to JSON file."""
        import json
        
        if filepath is None:
            # Use local time for filename to match the actual execution time
            filepath = Path('tests/results') / f"summary_{self._get_local_datetime().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Helper function to serialize datetime objects
        def serialize_datetime(obj):
            """Serialize datetime objects to ISO format strings."""
            if isinstance(obj, datetime):
                # Save as ISO format (naive datetime, assumed to be local time)
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        data = {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'statistics': self.get_statistics(),
            'features': self.features,
            'scenarios': self.scenarios,
            'security_issues': self.security_issues
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=serialize_datetime)
        
        return filepath

