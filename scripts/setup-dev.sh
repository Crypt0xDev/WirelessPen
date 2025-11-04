#!/usr/bin/env bash

# WirelessPen Framework v2.2.0
# Development setup script

set -e

echo "🔧 Setting up WirelessPen development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        echo -e "${RED}❌ This script only supports Linux systems${NC}"
        exit 1
    fi
}

# Install development dependencies
install_dev_deps() {
    echo -e "${BLUE}📦 Installing development dependencies...${NC}"
    
    # Python development packages
    python3 -m pip install --upgrade pip
    pip3 install -r requirements-dev.txt
    
    echo -e "${GREEN}✅ Development dependencies installed${NC}"
}

# Setup git hooks
setup_git_hooks() {
    echo -e "${BLUE}🔗 Setting up git hooks...${NC}"
    
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"
    else
        echo -e "${YELLOW}⚠️ Pre-commit not found, skipping git hooks${NC}"
    fi
}

# Run initial tests
run_tests() {
    echo -e "${BLUE}🧪 Running initial tests...${NC}"
    
    # Code formatting check
    if command -v black &> /dev/null; then
        black --check . || echo -e "${YELLOW}⚠️ Code formatting issues found${NC}"
    fi
    
    # Linting
    if command -v flake8 &> /dev/null; then
        flake8 . || echo -e "${YELLOW}⚠️ Linting issues found${NC}"
    fi
    
    # Type checking
    if command -v mypy &> /dev/null; then
        mypy main.py config.py --ignore-missing-imports || echo -e "${YELLOW}⚠️ Type checking issues found${NC}"
    fi
    
    # Security scan
    if command -v bandit &> /dev/null; then
        bandit -r . -f json || echo -e "${YELLOW}⚠️ Security scan found potential issues${NC}"
    fi
    
    echo -e "${GREEN}✅ Initial checks completed${NC}"
}

# Create development directories
create_dev_dirs() {
    echo -e "${BLUE}📁 Creating development directories...${NC}"
    
    mkdir -p tests/unit
    mkdir -p tests/integration
    mkdir -p tests/fixtures
    mkdir -p logs
    mkdir -p temp
    
    echo -e "${GREEN}✅ Development directories created${NC}"
}

# Main setup function
main() {
    echo -e "${GREEN}🚀 WirelessPen Development Setup${NC}"
    echo "================================="
    
    check_os
    install_dev_deps
    create_dev_dirs
    setup_git_hooks
    run_tests
    
    echo ""
    echo -e "${GREEN}🎉 Development environment setup completed!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Read the contributing guide: doc/CONTRIBUTING.md"
    echo "2. Run tests: python -m pytest"
    echo "3. Start coding with: black . && flake8 ."
    echo ""
    echo -e "${YELLOW}Happy coding! 🚀${NC}"
}

# Run main function
main "$@"