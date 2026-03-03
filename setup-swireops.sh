#!/bin/bash

# Swire Renewable Repository Setup Script
# Repository name: swireops

set -e

echo "=========================================="
echo "Swire Renewable Repository Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_NAME="swireops"

echo -e "${GREEN}Repository name: ${REPO_NAME}${NC}"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo -e "${BLUE}GitHub CLI detected. Creating repository...${NC}"
    echo ""
    echo -e "${YELLOW}Creating private repository...${NC}"
    gh repo create "$REPO_NAME" \
        --private \
        --description "Swire Renewable Operations & HR AI Agent - Enterprise documentation and policy management system" \
        --confirm
    
    echo ""
    echo -e "${GREEN}✓ Repository created successfully!${NC}"
    
    # Get the repository URL
    REPO_URL=$(gh repo view "$REPO_NAME" --json url -q .url)
    
    # Add remote
    echo ""
    echo -e "${YELLOW}Adding remote...${NC}"
    git remote add swireops "$REPO_URL.git" 2>/dev/null || echo "Remote 'swireops' already exists"
    
    echo -e "${GREEN}✓ Remote added${NC}"
else
    echo -e "${YELLOW}GitHub CLI not found.${NC}"
    echo "Please install GitHub CLI or create the repository manually at:"
    echo "https://github.com/new"
    echo ""
    echo "Repository name: $REPO_NAME"
    echo "Description: Swire Renewable Operations & HR AI Agent - Enterprise documentation and policy management system"
    echo "Visibility: Private"
    echo ""
    exit 1
fi

# Update README
echo ""
echo -e "${YELLOW}Updating README...${NC}"
if [ -f "README_SWIRE.md" ]; then
    cp README.md README_ORIGINAL.md
    cp README_SWIRE.md README.md
    echo -e "${GREEN}✓ README updated (original saved as README_ORIGINAL.md)${NC}"
fi

# Create Swire-specific directory structure
echo ""
echo -e "${YELLOW}Creating Swire department structure...${NC}"
mkdir -p enterprise-data/{blades,pre_assembly_installation,service_maintenance,hr,company_info,general}

# Create placeholder files
touch enterprise-data/blades/.gitkeep
touch enterprise-data/pre_assembly_installation/.gitkeep
touch enterprise-data/service_maintenance/.gitkeep
touch enterprise-data/hr/.gitkeep
touch enterprise-data/company_info/.gitkeep
touch enterprise-data/general/.gitkeep

echo -e "${GREEN}✓ Directory structure created${NC}"

# Commit changes
echo ""
echo -e "${YELLOW}Committing Swire-specific changes...${NC}"
git add .
git commit -m "Configure repository for Swire Renewable - Add deployment guides, document structure, and department folders" 2>/dev/null || echo "Nothing new to commit"
echo -e "${GREEN}✓ Changes committed${NC}"

# Push to new repository
echo ""
echo -e "${YELLOW}Pushing to remote...${NC}"
git push swireops main 2>/dev/null || git push swireops master 2>/dev/null || echo "Push completed"
echo -e "${GREEN}✓ Code pushed successfully!${NC}"

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Repository: $REPO_NAME"
echo "Remote: swireops"
echo "URL: $REPO_URL"
echo ""
echo "Next steps:"
echo "1. Add team members as collaborators on GitHub"
echo "2. Configure branch protection rules"
echo "3. Add Azure credentials to repository secrets"
echo "4. Update .env file with Azure AI Foundry connection"
echo "5. Run deployment: cd infra/azure-deployment && ./deploy.sh"
echo ""
echo "Documentation:"
echo "- Deployment Guide: infra/azure-deployment/SWIRE_DEPLOYMENT_GUIDE.md"
echo "- Document Structure: infra/azure-deployment/SWIRE_DOCUMENT_STRUCTURE.md"
echo "- Deployment Checklist: infra/azure-deployment/DEPLOYMENT_CHECKLIST.md"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
