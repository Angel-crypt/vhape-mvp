#!/bin/bash
# End-to-End (E2E) Testing Script for Vhape MVP
# This script runs comprehensive E2E tests to verify the complete system

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Vhape MVP - E2E Testing${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Check if virtual environment is activated
echo -e "${YELLOW}[1/6] Checking virtual environment...${NC}"
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    elif [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    else
        echo -e "${RED}✗ Virtual environment not found. Please create one first.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓ Virtual environment active${NC}"
echo ""

# Step 2: Check dependencies
echo -e "${YELLOW}[2/6] Checking dependencies...${NC}"
if ! python -c "import behave" 2>/dev/null; then
    echo -e "${RED}✗ 'behave' not installed. Installing dependencies...${NC}"
    pip install -q -r requirements.txt
fi
if ! python -c "import requests" 2>/dev/null; then
    echo -e "${RED}✗ 'requests' not installed. Installing dependencies...${NC}"
    pip install -q -r requirements.txt
fi
if ! python -c "import lark" 2>/dev/null; then
    echo -e "${RED}✗ 'lark' not installed. Installing dependencies...${NC}"
    pip install -q -r requirements.txt
fi
echo -e "${GREEN}✓ All dependencies installed${NC}"
echo ""

# Step 3: Run parser unit tests
echo -e "${YELLOW}[3/6] Running parser unit tests...${NC}"
if [ -f "test/test_parser.py" ]; then
    if python -m pytest test/test_parser.py -v 2>/dev/null || python test/test_parser.py 2>/dev/null; then
        echo -e "${GREEN}✓ Parser unit tests passed${NC}"
    else
        echo -e "${RED}✗ Parser unit tests failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ Parser tests not found, skipping...${NC}"
fi
echo ""

# Step 4: Check if API server is running
echo -e "${YELLOW}[4/6] Checking API server status...${NC}"
API_URL="${VHAPE_API_URL:-http://localhost:8000}"
if curl -s -f "${API_URL}/api/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API server is running at ${API_URL}${NC}"
else
    echo -e "${YELLOW}⚠ API server is not running at ${API_URL}${NC}"
    echo -e "${YELLOW}  Starting API server in background...${NC}"
    
    # Try to start the API server
    if [ -f "api_dummy/run.sh" ]; then
        bash api_dummy/run.sh > /tmp/vhape_api.log 2>&1 &
        API_PID=$!
        echo "API server started with PID: $API_PID"
        
        # Wait for server to be ready
        echo "Waiting for API server to be ready..."
        for i in {1..10}; do
            if curl -s -f "${API_URL}/api/health" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ API server is ready${NC}"
                SERVER_STARTED=true
                break
            fi
            sleep 1
        done
        
        if [ -z "$SERVER_STARTED" ]; then
            echo -e "${RED}✗ API server failed to start. Check /tmp/vhape_api.log${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ Cannot start API server. Please start it manually: ./api_dummy/run.sh${NC}"
        exit 1
    fi
fi
echo ""

# Step 5: Run Behave E2E tests
echo -e "${YELLOW}[5/6] Running Behave E2E tests...${NC}"
echo ""

# Run all features
if behave features/ --no-capture; then
    echo ""
    echo -e "${GREEN}✓ All E2E tests passed${NC}"
else
    echo ""
    echo -e "${RED}✗ Some E2E tests failed${NC}"
    
    # Clean up if we started the server
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
    fi
    
    exit 1
fi
echo ""

# Step 6: Generate summary
echo -e "${YELLOW}[6/6] Generating E2E test summary...${NC}"
echo ""

# Count features and scenarios
FEATURE_COUNT=$(find features -name "*.feature" | wc -l)
SCENARIO_COUNT=$(grep -h "^  Scenario" features/*.feature 2>/dev/null | wc -l || echo "0")

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  E2E Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Features tested:     ${GREEN}${FEATURE_COUNT}${NC}"
echo -e "Scenarios tested:    ${GREEN}${SCENARIO_COUNT}${NC}"
echo -e "API URL:             ${GREEN}${API_URL}${NC}"
echo -e "Status:              ${GREEN}✓ All tests passed${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Clean up if we started the server
if [ ! -z "$API_PID" ]; then
    echo -e "${YELLOW}Stopping background API server (PID: $API_PID)...${NC}"
    kill $API_PID 2>/dev/null || true
    echo -e "${GREEN}✓ API server stopped${NC}"
fi

echo -e "${GREEN}✓ E2E testing completed successfully!${NC}"

