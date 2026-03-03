#!/bin/bash

# Swire Renewable - Complete Deployment Script
# This script handles everything: agent setup + web app deployment

set -e

echo "=========================================="
echo "Swire Renewable - Complete Deployment"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found"
    echo "Please create .env file with your Azure configuration"
    exit 1
fi

# Check if PROJECT_CONNECTION_STRING is configured
if grep -q "<HostName>" .env; then
    echo "❌ ERROR: PROJECT_CONNECTION_STRING not configured"
    echo "Please update .env with your Azure AI Foundry connection string"
    exit 1
fi

echo "Step 1: Setting up AI Agent and Vector Store"
echo "=============================================="
echo ""

# Run the agent setup script
python3 setup-agent.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Agent setup failed. Please fix the errors and try again."
    exit 1
fi

echo ""
echo "Step 2: Deploying Web Application"
echo "=================================="
echo ""

# Run the deployment script
./deploy.sh

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Web app deployment failed. Please check the errors above."
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Swire Renewable Operations Agent is now live!"
echo ""
