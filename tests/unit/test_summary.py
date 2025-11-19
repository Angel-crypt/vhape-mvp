"""
Unit tests for Vhape TestSummary reporting system.
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from vhape.reporting.summary import TestSummary


class TestTestSummary:
    """Test cases for TestSummary class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.summary = TestSummary()
    
    def test_initialization(self):
        """Test that TestSummary initializes correctly."""
        assert self.summary.start_time is not None
        assert isinstance(self.summary.start_time, datetime)
        assert self.summary.end_time is None
        assert self.summary.features == []
        assert self.summary.scenarios == []
        assert self.summary.steps == []
        assert self.summary.security_issues == []
    
    def test_add_feature(self):
        """Test adding a feature to the summary."""
        self.summary.add_feature("Test Feature", "passed")
        
        assert len(self.summary.features) == 1
        feature = self.summary.features[0]
        assert feature['name'] == "Test Feature"
        assert feature['status'] == "passed"
        assert 'timestamp' in feature
        assert isinstance(feature['timestamp'], datetime)
    
    def test_add_feature_failed(self):
        """Test adding a failed feature."""
        self.summary.add_feature("Failed Feature", "failed")
        
        assert len(self.summary.features) == 1
        assert self.summary.features[0]['status'] == "failed"
    
    def test_add_multiple_features(self):
        """Test adding multiple features."""
        self.summary.add_feature("Feature 1", "passed")
        self.summary.add_feature("Feature 2", "passed")
        self.summary.add_feature("Feature 3", "failed")
        
        assert len(self.summary.features) == 3
        assert self.summary.features[0]['name'] == "Feature 1"
        assert self.summary.features[2]['status'] == "failed"
    
    def test_add_scenario(self):
        """Test adding a scenario to the summary."""
        self.summary.add_scenario("Test Scenario", "passed", "Test Feature")
        
        assert len(self.summary.scenarios) == 1
        scenario = self.summary.scenarios[0]
        assert scenario['name'] == "Test Scenario"
        assert scenario['status'] == "passed"
        assert scenario['feature'] == "Test Feature"
        assert 'timestamp' in scenario
    
    def test_add_scenario_failed(self):
        """Test adding a failed scenario."""
        self.summary.add_scenario("Failed Scenario", "failed", "Test Feature")
        
        assert len(self.summary.scenarios) == 1
        assert self.summary.scenarios[0]['status'] == "failed"
    
    def test_add_multiple_scenarios(self):
        """Test adding multiple scenarios."""
        self.summary.add_scenario("Scenario 1", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 2", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 3", "failed", "Feature 2")
        
        assert len(self.summary.scenarios) == 3
        assert self.summary.scenarios[2]['status'] == "failed"
    
    def test_add_step(self):
        """Test adding a step to the summary."""
        self.summary.add_step("Test Step", "passed")
        
        assert len(self.summary.steps) == 1
        step = self.summary.steps[0]
        assert step['name'] == "Test Step"
        assert step['status'] == "passed"
        assert step['error'] is None
        assert 'timestamp' in step
    
    def test_add_step_with_error(self):
        """Test adding a step with an error message."""
        error_msg = "AssertionError: Expected 200, got 401"
        self.summary.add_step("Failed Step", "failed", error_msg)
        
        assert len(self.summary.steps) == 1
        step = self.summary.steps[0]
        assert step['status'] == "failed"
        assert step['error'] == error_msg
    
    def test_add_multiple_steps(self):
        """Test adding multiple steps."""
        self.summary.add_step("Step 1", "passed")
        self.summary.add_step("Step 2", "passed")
        self.summary.add_step("Step 3", "failed", "Error message")
        
        assert len(self.summary.steps) == 3
        assert self.summary.steps[2]['status'] == "failed"
    
    def test_add_security_issue(self):
        """Test adding a security issue."""
        self.summary.add_security_issue(
            "Unauthorized access allowed",
            "validate token step",
            "high"
        )
        
        assert len(self.summary.security_issues) == 1
        issue = self.summary.security_issues[0]
        assert issue['message'] == "Unauthorized access allowed"
        assert issue['step'] == "validate token step"
        assert issue['severity'] == "high"
        assert 'timestamp' in issue
    
    def test_add_security_issue_default_severity(self):
        """Test adding a security issue with default severity."""
        self.summary.add_security_issue("Test issue", "test step")
        
        assert len(self.summary.security_issues) == 1
        assert self.summary.security_issues[0]['severity'] == "high"
    
    def test_add_multiple_security_issues(self):
        """Test adding multiple security issues."""
        self.summary.add_security_issue("Issue 1", "Step 1", "high")
        self.summary.add_security_issue("Issue 2", "Step 2", "medium")
        self.summary.add_security_issue("Issue 3", "Step 3", "low")
        
        assert len(self.summary.security_issues) == 3
        assert self.summary.security_issues[1]['severity'] == "medium"
    
    def test_finalize(self):
        """Test finalizing the summary."""
        assert self.summary.end_time is None
        self.summary.finalize()
        assert self.summary.end_time is not None
        assert isinstance(self.summary.end_time, datetime)
        assert self.summary.end_time >= self.summary.start_time
    
    def test_get_statistics_empty(self):
        """Test getting statistics with no data."""
        stats = self.summary.get_statistics()
        
        assert stats['features']['total'] == 0
        assert stats['features']['passed'] == 0
        assert stats['features']['failed'] == 0
        assert stats['scenarios']['total'] == 0
        assert stats['scenarios']['passed'] == 0
        assert stats['scenarios']['failed'] == 0
        assert stats['steps']['total'] == 0
        assert stats['steps']['passed'] == 0
        assert stats['steps']['failed'] == 0
        assert stats['security_issues'] == 0
        assert stats['duration'] == 0
        assert stats['success_rate'] == 0
    
    def test_get_statistics_with_data(self):
        """Test getting statistics with test data."""
        # Add test data
        self.summary.add_feature("Feature 1", "passed")
        self.summary.add_feature("Feature 2", "failed")
        
        self.summary.add_scenario("Scenario 1", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 2", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 3", "failed", "Feature 2")
        
        self.summary.add_step("Step 1", "passed")
        self.summary.add_step("Step 2", "passed")
        self.summary.add_step("Step 3", "failed", "Error")
        
        self.summary.add_security_issue("Issue 1", "Step 1")
        self.summary.add_security_issue("Issue 2", "Step 2")
        
        self.summary.finalize()
        
        stats = self.summary.get_statistics()
        
        assert stats['features']['total'] == 2
        assert stats['features']['passed'] == 1
        assert stats['features']['failed'] == 1
        
        assert stats['scenarios']['total'] == 3
        assert stats['scenarios']['passed'] == 2
        assert stats['scenarios']['failed'] == 1
        
        assert stats['steps']['total'] == 3
        assert stats['steps']['passed'] == 2
        assert stats['steps']['failed'] == 1
        
        assert stats['security_issues'] == 2
        assert stats['duration'] > 0
        assert stats['success_rate'] == pytest.approx(66.67, abs=0.01)
    
    def test_get_statistics_success_rate_100_percent(self):
        """Test success rate calculation for 100% success."""
        self.summary.add_scenario("Scenario 1", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 2", "passed", "Feature 1")
        self.summary.finalize()
        
        stats = self.summary.get_statistics()
        assert stats['success_rate'] == 100.0
    
    def test_get_statistics_success_rate_0_percent(self):
        """Test success rate calculation for 0% success."""
        self.summary.add_scenario("Scenario 1", "failed", "Feature 1")
        self.summary.add_scenario("Scenario 2", "failed", "Feature 1")
        self.summary.finalize()
        
        stats = self.summary.get_statistics()
        assert stats['success_rate'] == 0.0
    
    def test_save_json_default_path(self):
        """Test saving JSON report with default path."""
        # Add some test data
        self.summary.add_feature("Test Feature", "passed")
        self.summary.add_scenario("Test Scenario", "passed", "Test Feature")
        self.summary.add_step("Test Step", "passed")
        self.summary.finalize()
        
        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the default path to use temp directory
            original_path = Path('tests/results')
            filepath = Path(tmpdir) / "summary_test.json"
            
            # Save to custom path
            saved_path = self.summary.save_json(filepath)
            
            assert saved_path == filepath
            assert filepath.exists()
            
            # Verify JSON content
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'start_time' in data
            assert 'end_time' in data
            assert 'statistics' in data
            assert 'features' in data
            assert 'scenarios' in data
            assert 'security_issues' in data
            
            assert len(data['features']) == 1
            assert data['features'][0]['name'] == "Test Feature"
            assert data['statistics']['features']['total'] == 1
    
    def test_save_json_custom_path(self):
        """Test saving JSON report with custom path."""
        self.summary.add_feature("Feature 1", "passed")
        self.summary.finalize()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "custom" / "report.json"
            saved_path = self.summary.save_json(custom_path)
            
            assert saved_path == custom_path
            assert custom_path.exists()
            assert custom_path.parent.exists()  # Directory should be created
    
    def test_save_json_without_finalize(self):
        """Test saving JSON report without finalizing (end_time should be None)."""
        self.summary.add_feature("Feature 1", "passed")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "report.json"
            self.summary.save_json(filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data['end_time'] is None
    
    def test_save_json_complete_data(self):
        """Test that all data is saved correctly in JSON."""
        # Add comprehensive test data
        self.summary.add_feature("Feature 1", "passed")
        self.summary.add_feature("Feature 2", "failed")
        
        self.summary.add_scenario("Scenario 1", "passed", "Feature 1")
        self.summary.add_scenario("Scenario 2", "failed", "Feature 2")
        
        self.summary.add_step("Step 1", "passed")
        self.summary.add_step("Step 2", "failed", "Error message")
        
        self.summary.add_security_issue("Security Issue 1", "Step 1", "high")
        self.summary.add_security_issue("Security Issue 2", "Step 2", "medium")
        
        self.summary.finalize()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "complete_report.json"
            self.summary.save_json(filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Verify all data is present
            assert len(data['features']) == 2
            assert len(data['scenarios']) == 2
            assert len(data['security_issues']) == 2
            assert data['statistics']['features']['total'] == 2
            assert data['statistics']['scenarios']['total'] == 2
            assert data['statistics']['security_issues'] == 2
    
    def test_print_summary(self, capsys):
        """Test printing summary to console."""
        self.summary.add_feature("Test Feature", "passed")
        self.summary.add_scenario("Test Scenario", "passed", "Test Feature")
        self.summary.add_step("Test Step", "passed")
        self.summary.finalize()
        
        self.summary.print_summary()
        
        captured = capsys.readouterr()
        assert "VHAPE - Security Test Summary" in captured.out
        assert "Features:" in captured.out
        assert "Scenarios:" in captured.out
        assert "Steps:" in captured.out
        assert "Success Rate:" in captured.out
    
    def test_print_summary_with_security_issues(self, capsys):
        """Test printing summary with security issues."""
        self.summary.add_feature("Test Feature", "passed")
        self.summary.add_scenario("Test Scenario", "failed", "Test Feature")
        self.summary.add_security_issue("Unauthorized access", "Test Step", "high")
        self.summary.finalize()
        
        self.summary.print_summary()
        
        captured = capsys.readouterr()
        assert "Security Issues Found" in captured.out
        assert "Unauthorized access" in captured.out
    
    def test_print_summary_no_security_issues(self, capsys):
        """Test printing summary without security issues."""
        self.summary.add_feature("Test Feature", "passed")
        self.summary.finalize()
        
        self.summary.print_summary()
        
        captured = capsys.readouterr()
        assert "No security issues detected" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

