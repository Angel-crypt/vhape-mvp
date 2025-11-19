"""
HTML Report Generator for Vhape Test Results

Generates a modern, interactive HTML report from JSON test results.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def generate_html_report(json_file: Path, output_file: Path = None) -> Path:
    """
    Generate a modern HTML report from a JSON test results file.
    
    Args:
        json_file: Path to the JSON test results file
        output_file: Optional output path for HTML file. If None, uses same name as JSON but with .html extension
        
    Returns:
        Path to the generated HTML file
    """
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine output file path
    if output_file is None:
        output_file = json_file.with_suffix('.html')
    
    output_file = Path(output_file)
    
    # Generate HTML
    html_content = _generate_html_content(data, json_file.name)
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file


def _generate_html_content(data: Dict[str, Any], json_filename: str) -> str:
    """Generate the complete HTML content."""
    
    stats = data.get('statistics', {})
    features = data.get('features', [])
    scenarios = data.get('scenarios', [])
    security_issues = data.get('security_issues', [])
    
    # Format timestamps
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    
    # Calculate success rate
    success_rate = stats.get('success_rate', 0)
    duration = stats.get('duration', 0)
    
    # Counts
    total_features = stats.get('features', {}).get('total', 0)
    passed_features = stats.get('features', {}).get('passed', 0)
    failed_features = stats.get('features', {}).get('failed', 0)
    
    total_scenarios = stats.get('scenarios', {}).get('total', 0)
    passed_scenarios = stats.get('scenarios', {}).get('passed', 0)
    failed_scenarios = stats.get('scenarios', {}).get('failed', 0)
    
    total_steps = stats.get('steps', {}).get('total', 0)
    passed_steps = stats.get('steps', {}).get('passed', 0)
    failed_steps = stats.get('steps', {}).get('failed', 0)
    
    num_security_issues = len(security_issues)
    
    # Determine overall status
    overall_status = 'success' if failed_scenarios == 0 and num_security_issues == 0 else 'warning' if failed_scenarios > 0 else 'danger'
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vhape Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        {_get_css()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1 class="title">
                    <span class="logo">VHAPE</span>
                    <span class="subtitle">Security Test Report</span>
                </h1>
                <div class="header-meta">
                    <div class="meta-item">
                        <span class="meta-label">Generated:</span>
                        <span class="meta-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Source:</span>
                        <span class="meta-value">{json_filename}</span>
                    </div>
                </div>
            </div>
        </header>

        <div class="overview-section">
            <div class="status-badge status-{overall_status}">
                <span class="status-icon">{'✓' if overall_status == 'success' else '⚠' if overall_status == 'warning' else '✗'}</span>
                <span class="status-text">
                    {f'All Tests Passed' if overall_status == 'success' else f'{failed_scenarios} Failed' if failed_scenarios > 0 else 'Security Issues Found'}
                </span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{success_rate:.1f}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{duration:.2f}s</div>
                    <div class="stat-label">Duration</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_features}</div>
                    <div class="stat-label">Features</div>
                    <div class="stat-detail">
                        <span class="passed">{passed_features} passed</span>
                        <span class="failed">{failed_features} failed</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_scenarios}</div>
                    <div class="stat-label">Scenarios</div>
                    <div class="stat-detail">
                        <span class="passed">{passed_scenarios} passed</span>
                        <span class="failed">{failed_scenarios} failed</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_steps}</div>
                    <div class="stat-label">Steps</div>
                    <div class="stat-detail">
                        <span class="passed">{passed_steps} passed</span>
                        <span class="failed">{failed_steps} failed</span>
                    </div>
                </div>
                <div class="stat-card stat-card-danger">
                    <div class="stat-value">{num_security_issues}</div>
                    <div class="stat-label">Security Issues</div>
                </div>
            </div>
        </div>

        {_generate_security_issues_section(security_issues) if security_issues else ''}

        <div class="content-section">
            <div class="section-header">
                <h2>Features & Scenarios</h2>
                <div class="filter-controls">
                    <input type="text" id="searchInput" placeholder="Search features or scenarios..." class="search-input">
                    <div class="filter-buttons">
                        <button class="filter-btn active" data-filter="all">All</button>
                        <button class="filter-btn" data-filter="passed">Passed</button>
                        <button class="filter-btn" data-filter="failed">Failed</button>
                    </div>
                </div>
            </div>

            <div class="features-container" id="featuresContainer">
                {_generate_features_html(features, scenarios)}
            </div>
        </div>

        <footer class="footer">
            <p>Generated by Vhape Test Framework</p>
            <p>Execution Time: {start_time} - {end_time if end_time else 'N/A'}</p>
        </footer>
    </div>

    <script>
        {_get_javascript()}
    </script>
</body>
</html>
"""
    return html


def _generate_security_issues_section(security_issues: list) -> str:
    """Generate HTML for security issues section."""
    if not security_issues:
        return ''
    
    issues_html = '<div class="security-section">'
    issues_html += '<div class="section-header">'
    issues_html += '<h2 class="security-title">Security Issues</h2>'
    issues_html += f'<span class="badge badge-danger">{len(security_issues)}</span>'
    issues_html += '</div>'
    issues_html += '<div class="security-issues-list">'
    
    for issue in security_issues:
        severity = issue.get('severity', 'high')
        message = issue.get('message', '')
        step = issue.get('step', '')
        timestamp = issue.get('timestamp', '')
        
        issues_html += f'''
        <div class="security-issue security-{severity}">
            <div class="issue-header">
                <span class="severity-badge severity-{severity}">{severity.upper()}</span>
                <span class="issue-step">{step}</span>
            </div>
            <div class="issue-message">{message}</div>
            {f'<div class="issue-timestamp">{timestamp}</div>' if timestamp else ''}
        </div>
        '''
    
    issues_html += '</div></div>'
    return issues_html


def _generate_features_html(features: list, scenarios: list) -> str:
    """Generate HTML for features and scenarios."""
    html = ''
    
    # Group scenarios by feature
    scenarios_by_feature = {}
    for scenario in scenarios:
        feature_name = scenario.get('feature', 'Unknown')
        if feature_name not in scenarios_by_feature:
            scenarios_by_feature[feature_name] = []
        scenarios_by_feature[feature_name].append(scenario)
    
    for feature in features:
        feature_name = feature.get('name', 'Unknown')
        feature_status = feature.get('status', 'unknown')
        
        feature_scenarios = scenarios_by_feature.get(feature_name, [])
        passed_count = sum(1 for s in feature_scenarios if s.get('status') == 'passed')
        failed_count = sum(1 for s in feature_scenarios if s.get('status') == 'failed')
        
        html += f'''
        <div class="feature-card" data-status="{feature_status}">
            <div class="feature-header">
                <h3 class="feature-name">{feature_name}</h3>
                <div class="feature-badges">
                    <span class="badge badge-{feature_status}">{feature_status.upper()}</span>
                    <span class="scenario-count">{len(feature_scenarios)} scenarios</span>
                </div>
            </div>
            <div class="feature-stats">
                <span class="stat-item passed">{passed_count} passed</span>
                <span class="stat-item failed">{failed_count} failed</span>
            </div>
            <div class="scenarios-list">
        '''
        
        for scenario in feature_scenarios:
            scenario_name = scenario.get('name', 'Unknown')
            scenario_status = scenario.get('status', 'unknown')
            
            html += f'''
                <div class="scenario-item scenario-{scenario_status}">
                    <span class="scenario-status-icon">{'✓' if scenario_status == 'passed' else '✗'}</span>
                    <span class="scenario-name">{scenario_name}</span>
                    <span class="scenario-badge badge-{scenario_status}">{scenario_status}</span>
                </div>
            '''
        
        html += '''
            </div>
        </div>
        '''
    
    return html


def _get_css() -> str:
    """Return the CSS styles for the HTML report."""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .title {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .logo {
            font-size: 48px;
            font-weight: 700;
            letter-spacing: 4px;
        }

        .subtitle {
            font-size: 18px;
            opacity: 0.9;
            font-weight: 300;
        }

        .header-meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            text-align: right;
        }

        .meta-item {
            display: flex;
            gap: 8px;
        }

        .meta-label {
            opacity: 0.8;
        }

        .meta-value {
            font-weight: 600;
        }

        .overview-section {
            padding: 40px;
            background: #f8f9fa;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 16px 24px;
            border-radius: 12px;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 30px;
        }

        .status-success {
            background: #d4edda;
            color: #155724;
        }

        .status-warning {
            background: #fff3cd;
            color: #856404;
        }

        .status-danger {
            background: #f8d7da;
            color: #721c24;
        }

        .status-icon {
            font-size: 24px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .stat-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }

        .stat-card-danger {
            border: 2px solid #dc3545;
        }

        .stat-value {
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 8px;
        }

        .stat-card-danger .stat-value {
            color: #dc3545;
        }

        .stat-label {
            font-size: 14px;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .stat-detail {
            display: flex;
            justify-content: center;
            gap: 12px;
            font-size: 12px;
            margin-top: 8px;
        }

        .stat-detail .passed {
            color: #28a745;
            font-weight: 600;
        }

        .stat-detail .failed {
            color: #dc3545;
            font-weight: 600;
        }

        .security-section {
            padding: 40px;
            background: #fff5f5;
            border-top: 4px solid #dc3545;
        }

        .security-title {
            color: #dc3545;
            margin-bottom: 20px;
        }

        .security-issues-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .security-issue {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .security-high {
            border-left-color: #dc3545;
        }

        .security-medium {
            border-left-color: #ffc107;
        }

        .security-low {
            border-left-color: #17a2b8;
        }

        .issue-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .severity-badge {
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .severity-high {
            background: #dc3545;
            color: white;
        }

        .severity-medium {
            background: #ffc107;
            color: #333;
        }

        .severity-low {
            background: #17a2b8;
            color: white;
        }

        .issue-step {
            color: #666;
            font-size: 14px;
        }

        .issue-message {
            color: #333;
            font-size: 16px;
            line-height: 1.6;
        }

        .issue-timestamp {
            color: #999;
            font-size: 12px;
            margin-top: 8px;
        }

        .content-section {
            padding: 40px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .section-header h2 {
            font-size: 28px;
            color: #333;
        }

        .filter-controls {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-input {
            padding: 10px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            width: 300px;
            transition: border-color 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .filter-buttons {
            display: flex;
            gap: 8px;
        }

        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }

        .filter-btn:hover {
            border-color: #667eea;
            color: #667eea;
        }

        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .features-container {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .feature-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 24px;
            border: 2px solid transparent;
            transition: all 0.2s;
        }

        .feature-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .feature-card[data-status="passed"] {
            border-left: 4px solid #28a745;
        }

        .feature-card[data-status="failed"] {
            border-left: 4px solid #dc3545;
        }

        .feature-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .feature-name {
            font-size: 22px;
            color: #333;
            font-weight: 600;
        }

        .feature-badges {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .badge {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-passed {
            background: #d4edda;
            color: #155724;
        }

        .badge-failed {
            background: #f8d7da;
            color: #721c24;
        }

        .badge-danger {
            background: #dc3545;
            color: white;
        }

        .scenario-count {
            color: #666;
            font-size: 14px;
        }

        .feature-stats {
            display: flex;
            gap: 16px;
            margin-bottom: 16px;
            font-size: 14px;
        }

        .stat-item.passed {
            color: #28a745;
            font-weight: 600;
        }

        .stat-item.failed {
            color: #dc3545;
            font-weight: 600;
        }

        .scenarios-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .scenario-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: white;
            border-radius: 8px;
            transition: all 0.2s;
        }

        .scenario-item:hover {
            background: #f8f9fa;
            transform: translateX(4px);
        }

        .scenario-passed {
            border-left: 3px solid #28a745;
        }

        .scenario-failed {
            border-left: 3px solid #dc3545;
        }

        .scenario-status-icon {
            font-size: 18px;
            font-weight: bold;
        }

        .scenario-passed .scenario-status-icon {
            color: #28a745;
        }

        .scenario-failed .scenario-status-icon {
            color: #dc3545;
        }

        .scenario-name {
            flex: 1;
            color: #333;
            font-size: 15px;
        }

        .scenario-badge {
            font-size: 11px;
        }

        .footer {
            background: #f8f9fa;
            padding: 24px 40px;
            text-align: center;
            color: #666;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }

        .footer p {
            margin: 4px 0;
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            .header-meta {
                text-align: center;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .search-input {
                width: 100%;
            }

            .section-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }

        .hidden {
            display: none !important;
        }
    """


def _get_javascript() -> str:
    """Return the JavaScript code for interactivity."""
    return """
        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        const featureCards = document.querySelectorAll('.feature-card');
        const searchInput = document.getElementById('searchInput');

        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // Filter features
                const filter = button.getAttribute('data-filter');
                filterFeatures(filter);
            });
        });

        // Search functionality
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
            
            featureCards.forEach(card => {
                const featureName = card.querySelector('.feature-name').textContent.toLowerCase();
                const scenarios = card.querySelectorAll('.scenario-name');
                let matches = featureName.includes(searchTerm);
                
                if (!matches) {
                    scenarios.forEach(scenario => {
                        if (scenario.textContent.toLowerCase().includes(searchTerm)) {
                            matches = true;
                        }
                    });
                }

                if (matches && (activeFilter === 'all' || card.getAttribute('data-status') === activeFilter)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });

        function filterFeatures(filter) {
            const searchTerm = searchInput.value.toLowerCase();
            
            featureCards.forEach(card => {
                const featureName = card.querySelector('.feature-name').textContent.toLowerCase();
                const scenarios = card.querySelectorAll('.scenario-name');
                let matches = featureName.includes(searchTerm);
                
                if (!matches) {
                    scenarios.forEach(scenario => {
                        if (scenario.textContent.toLowerCase().includes(searchTerm)) {
                            matches = true;
                        }
                    });
                }

                if (filter === 'all') {
                    card.classList.toggle('hidden', !matches);
                } else {
                    const status = card.getAttribute('data-status');
                    card.classList.toggle('hidden', status !== filter || !matches);
                }
            });
        }

        // Smooth scroll for better UX
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    """

