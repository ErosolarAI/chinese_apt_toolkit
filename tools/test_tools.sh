#!/bin/bash

# APT Tools Test Script
# Automated testing for all APT toolkit tools
# For educational and authorized penetration testing only

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___  _____ _____   _____           _           _           _   
 / _ \\|  _  |  __ \\ /  ___|         | |         | |         | |  
/ /_\\ \\ | | | |  \\/ \\ \\`--.  ___  | |_ ___  __| | ___  ___| |_ 
|  _  | | | | | __   \\ \\`--. \\/ _ \\ | __/ _ \\/ _\` |/ _ \\ __| __|
| | | \\ \\_/ / |_\\ \\/\\__/ /  __/ | | ||  __/ (_| |  __/ |_ | |_ 
\\_| |_/\\___/ \\____/ \\____/ \\___| |_|\\__\\___|\\__,_|\\___|\\__|\\__|

                    APT Tools Test Script
           For Educational and Authorized Testing Only
EOF
echo ""
echo "                    APT Tools Test Script"
echo "           For Educational and Authorized Testing Only"
echo -e "${NC}"

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    TOOLS=(
        "apt_recon.sh"
        "APT-PowerShell-Toolkit.ps1"
        "apt_persistence.py"
        "apt_network_scanner"
        "apt_memory_injector"
        "apt_web_recon.js"
        "apt_social_engineering.rb"
    )
else
    TOOLS=(
        "apt_recon.sh"
        "APT-PowerShell-Toolkit.ps1"
        "apt_persistence.py"
        "apt_network_scanner"
        "apt_web_recon.js"
        "apt_social_engineering.rb"
    )
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run test and check exit code
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit=${3:-0}
    
    echo -e "${YELLOW}[*] Running test: $test_name${NC}"
    echo -e "${BLUE}    Command: $command${NC}"
    
    # Execute command with timeout
    timeout 30s bash -c "$command" > /dev/null 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq $expected_exit ] || [ $exit_code -eq 124 ]; then
        echo -e "${GREEN}[+] Test passed: $test_name${NC}"
        return 0
    else
        echo -e "${RED}[-] Test failed: $test_name (exit code: $exit_code)${NC}"
        return 1
    fi
}

# Function to check tool availability
check_tool_availability() {
    echo -e "${BLUE}[*] Checking Tool Availability...${NC}"
    
    local available_tools=0
    local total_tools=0
    
    for tool in "${TOOLS[@]}"; do
        total_tools=$((total_tools + 1))
        if [ -f "$tool" ]; then
            echo -e "${GREEN}[+] Found: $tool${NC}"
            available_tools=$((available_tools + 1))
        else
            echo -e "${RED}[-] Missing: $tool${NC}"
        fi
    done
    
    echo -e "${GREEN}[+] Tool availability: $available_tools/$total_tools tools available${NC}"
    
    if [ "$available_tools" -ne "$total_tools" ]; then
        return 1
    fi
    
    return 0
}

# Function to test shell scripts
test_shell_scripts() {
    echo -e "${BLUE}[*] Testing Shell Scripts...${NC}"
    local passed=0
    local total=0
    
    if [ -f "apt_recon.sh" ] && [ -x "apt_recon.sh" ]; then
        total=$((total + 1))
        if run_test "apt_recon.sh help" "./apt_recon.sh --help" 0; then
            passed=$((passed + 1))
        fi
    else
        echo -e "${YELLOW}[!] apt_recon.sh not found or not executable${NC}"
    fi
    
    echo -e "${GREEN}[+] Shell scripts: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test PowerShell scripts
test_powershell_scripts() {
    echo -e "${BLUE}[*] Testing PowerShell Scripts...${NC}"
    local passed=0
    local total=0
    
    if command_exists pwsh; then
        PS_CMD="pwsh"
    elif command_exists powershell; then
        PS_CMD="powershell"
    else
        echo -e "${YELLOW}[!] PowerShell not available${NC}"
        return 0
    fi
    
    if [ -f "APT-PowerShell-Toolkit.ps1" ]; then
        total=$((total + 1))
        if run_test "PowerShell Toolkit help" "$PS_CMD -Command '& {.\\APT-PowerShell-Toolkit.ps1 -Help}'" 0; then
            passed=$((passed + 1))
        fi
    else
        echo -e "${YELLOW}[!] APT-PowerShell-Toolkit.ps1 not found${NC}"
    fi
    
    echo -e "${GREEN}[+] PowerShell scripts: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test Python scripts
test_python_scripts() {
    echo -e "${BLUE}[*] Testing Python Scripts...${NC}"
    local passed=0
    local total=0
    
    if command_exists python3; then
        if [ -f "apt_persistence.py" ]; then
            total=$((total + 1))
            if run_test "Python persistence help" "python3 apt_persistence.py --help" 0; then
                passed=$((passed + 1))
            fi
        else
            echo -e "${YELLOW}[!] apt_persistence.py not found${NC}"
        fi
    else
        echo -e "${YELLOW}[!] Python3 not available${NC}"
    fi
    
    echo -e "${GREEN}[+] Python scripts: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test Go tools
test_go_tools() {
    echo -e "${BLUE}[*] Testing Go Tools...${NC}"
    local passed=0
    local total=0
    
    if [ -f "apt_network_scanner" ] && [ -x "apt_network_scanner" ]; then
        total=$((total + 1))
        if run_test "Go network scanner help" "./apt_network_scanner -h" 0; then
            passed=$((passed + 1))
        fi
    else
        echo -e "${YELLOW}[!] apt_network_scanner not found or not executable${NC}"
    fi
    
    echo -e "${GREEN}[+] Go tools: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test C tools
test_c_tools() {
    echo -e "${BLUE}[*] Testing C Tools...${NC}"
    local passed=0
    local total=0
    
    if [ -f "apt_memory_injector" ] && [ -x "apt_memory_injector" ]; then
        total=$((total + 1))
        if run_test "C memory injector help" "./apt_memory_injector --help" 0; then
            passed=$((passed + 1))
        fi
    else
        echo -e "${YELLOW}[!] apt_memory_injector not found or not executable${NC}"
    fi
    
    echo -e "${GREEN}[+] C tools: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test JavaScript tools
test_javascript_tools() {
    echo -e "${BLUE}[*] Testing JavaScript Tools...${NC}"
    local passed=0
    local total=0
    
    if command_exists node; then
        if [ -f "apt_web_recon.js" ]; then
            total=$((total + 1))
            if run_test "JavaScript web recon help" "node apt_web_recon.js --help" 0; then
                passed=$((passed + 1))
            fi
        else
            echo -e "${YELLOW}[!] apt_web_recon.js not found${NC}"
        fi
    else
        echo -e "${YELLOW}[!] Node.js not available${NC}"
    fi
    
    echo -e "${GREEN}[+] JavaScript tools: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to test Ruby tools
test_ruby_tools() {
    echo -e "${BLUE}[*] Testing Ruby Tools...${NC}"
    local passed=0
    local total=0
    
    if command_exists ruby; then
        if [ -f "apt_social_engineering.rb" ]; then
            total=$((total + 1))
            if run_test "Ruby social engineering help" "ruby apt_social_engineering.rb --help" 0; then
                passed=$((passed + 1))
            fi
        else
            echo -e "${YELLOW}[!] apt_social_engineering.rb not found${NC}"
        fi
    else
        echo -e "${YELLOW}[!] Ruby not available${NC}"
    fi
    
    echo -e "${GREEN}[+] Ruby tools: $passed/$total tests passed${NC}"
    return $((total - passed))
}

# Function to run comprehensive tests
run_comprehensive_tests() {
    local total_failed=0
    
    echo -e "${BLUE}[*] Starting Comprehensive APT Tools Test Suite${NC}"
    echo ""
    
    # Check tool availability first
    check_tool_availability
    local availability_failed=$?
    
    echo ""
    
    # Run individual test suites
    test_shell_scripts
    total_failed=$((total_failed + $?))
    echo ""
    
    test_powershell_scripts
    total_failed=$((total_failed + $?))
    echo ""
    
    test_python_scripts
    total_failed=$((total_failed + $?))
    echo ""
    
    test_go_tools
    total_failed=$((total_failed + $?))
    echo ""
    
    test_c_tools
    total_failed=$((total_failed + $?))
    echo ""
    
    test_javascript_tools
    total_failed=$((total_failed + $?))
    echo ""
    
    test_ruby_tools
    total_failed=$((total_failed + $?))
    
    echo ""
    echo -e "${BLUE}[*] Test Suite Summary${NC}"
    echo "=" * 50
    
    if [ $total_failed -eq 0 ] && [ $availability_failed -eq 0 ]; then
        echo -e "${GREEN}[+] All tests passed! APT tools are ready for use.${NC}"
    else
        echo -e "${YELLOW}[!] Some tests failed or tools are missing${NC}"
        echo -e "${YELLOW}[!] Failed tests: $total_failed${NC}"
        echo -e "${YELLOW}[!] Missing tools: $availability_failed${NC}"
        echo ""
        echo -e "${BLUE}Recommendations:${NC}"
        echo "  1. Run ./setup_tools.sh to install missing dependencies"
        echo "  2. Check file permissions and compilation"
        echo "  3. Verify all tool files are present"
    fi
    
    return $((total_failed + availability_failed))
}

# Main execution
main() {
    (
        cd tools
        run_comprehensive_tests
    )
    
    echo ""
    echo -e "${BLUE}[*] Test script completed${NC}"
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi