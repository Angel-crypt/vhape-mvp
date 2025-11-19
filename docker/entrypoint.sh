#!/bin/bash
# ============================================
# Entrypoint script for Vhape bjparser container
# ============================================
# This script:
# 1. Waits for the API dummy service to be ready
# 2. Creates results directory if missing
# 3. Executes provided commands or drops to interactive shell

set -euo pipefail

# Logging function
log() {
    echo "[entrypoint] $*" >&2
}

# Wait for API Dummy service to be ready
wait_for_api() {
    local api_url="${VHAPE_API_URL:-http://api_dummy:8000}"
    local max_attempts=30
    local attempt=1
    local wait_interval=1

    log "Waiting for API Dummy at ${api_url}..."

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "${api_url}/api/health" > /dev/null 2>&1; then
            log "API Dummy is ready!"
            return 0
        fi

        log "Attempt ${attempt}/${max_attempts}: API not ready, waiting ${wait_interval}s..."
        sleep $wait_interval
        attempt=$((attempt + 1))
    done

    log "ERROR: API Dummy did not become ready after ${max_attempts} attempts"
    return 1
}

# Create results directory if it doesn't exist
create_results_dir() {
    local results_dir="${RESULTS_DIR:-/app/tests/results}"
    
    if [ ! -d "$results_dir" ]; then
        log "Creating results directory: ${results_dir}"
        mkdir -p "$results_dir"
    else
        log "Results directory exists: ${results_dir}"
    fi
}

# Main execution
main() {
    log "Starting Vhape bjparser entrypoint..."

    # Wait for API to be ready
    if ! wait_for_api; then
        log "FATAL: Failed to connect to API Dummy"
        exit 1
    fi

    # Create results directory
    create_results_dir

    # If no arguments provided, drop into interactive shell
    if [ $# -eq 0 ]; then
        log "No arguments provided, starting interactive shell..."
        log "Available commands:"
        log "  - python tests/e2e/run_e2e_tests.py --all"
        log "  - behave"
        log "  - python -c 'import requests; print(requests.get(\"${VHAPE_API_URL:-http://api_dummy:8000}/api/health\").status_code)'"
        exec /bin/bash
    else
        # Execute provided command
        log "Executing command: $*"
        exec "$@"
    fi
}

# Run main function with all arguments
main "$@"

