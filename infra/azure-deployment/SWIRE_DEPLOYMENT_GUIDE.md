# Swire Renewable - Operations Manual Agent Deployment Guide

## Overview
This guide walks you through deploying the Azure AI Enterprise Agent for Swire Renewable's operations manual system across their four business units.

## Prerequisites

1. **Azure CLI** installed and authenticated
2. **Azure AI Foundry** project created
3. **Python 3.10+** installed locally
4. **Azure subscription** access (you're using: Azure subscription 1 / Microsoft Azure Sponsorship)

## Step 1: Set Up Azure AI Foundry

### 1.1 Create Azure AI Foundry Project (if not exists)

```bash
# Login to Azure
az login

# Set your subscription
az account set --subscription "Azure subscription 1"

# Create AI Foundry project (if needed)
# Or use existing project from swire-copilot-dev-rg
```

### 1.2 Run the Automated Setup Script

Instead of using a Jupyter notebook, we have a modern Python script that automates everything:

```bash
cd infra/azure-deployment

# Install required packages (if not already installed)
pip install azure-ai-projects azure-identity python-dotenv

# Run the setup script
python setup-agent.py
```

This script will:
- Create the AI agent in Azure AI Foundry
- Create the vector store for document search
- Upload all documents from `enterprise-data/` folder
- Configure everything automatically

No notebook required!

## Step 2: Configure Environment Variables

The `.env` file has been created in `infra/azure-deployment/.env`. Update these values:

### Required Configuration:

```bash
# Get this from Azure AI Foundry project
PROJECT_CONNECTION_STRING="<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"

# Resource names (already configured)
RESOURCE_GROUP="swire-ops-manual-rg"
APP_SERVICE_PLAN="swire-ops-manual-plan"
WEB_APP_NAME="swire-ops-manual-agent"
LOCATION="eastus"

# Agent details (from notebook)
AGENT_NAME="swire-operations-manual-assistant"
VECTOR_STORE_NAME="swire-ops-docs-vectorstore"

# Optional: Bing connection (if configured in AI Foundry)
BING_CONNECTION_NAME="swire-bing-connection"
```

### How to get PROJECT_CONNECTION_STRING:

1. Go to Azure AI Foundry portal
2. Navigate to your project
3. Go to Settings → Project details
4. Copy the connection string

## Step 3: Prepare Operations Documents

Replace the sample documents in `enterprise-data/` with Swire Renewable's actual operations manuals organized by department:

```bash
enterprise-data/
├── blades/
│   ├── blades_operations_manual.md
│   ├── blades_safety_procedures.md
│   └── blades_quality_standards.md
├── pre_assembly_installation/
│   ├── pre_assembly_procedures.md
│   ├── installation_guidelines.md
│   └── site_preparation_checklist.md
├── service_maintenance/
│   ├── maintenance_schedules.md
│   ├── service_procedures.md
│   └── troubleshooting_guide.md
├── hr/
│   ├── hr_policies.md
│   ├── employee_handbook.md
│   └── training_requirements.md
├── company_info/
│   ├── about_swire_renewable.md
│   ├── company_values.md
│   └── organizational_structure.md
└── general/
    ├── safety_policies.md
    ├── compliance_procedures.md
    └── standard_operating_procedures.md
```

Upload these documents when running the Jupyter notebook.

## Step 4: Deploy to Azure Web App

### 4.1 Navigate to deployment directory

```bash
cd infra/azure-deployment
```

### 4.2 Make deploy script executable

```bash
chmod +x deploy.sh
```

### 4.3 Run deployment

```bash
./deploy.sh
```

The script will:
1. Create the resource group `swire-ops-manual-rg`
2. Create App Service Plan
3. Create Web App with Python 3.10 runtime
4. Enable Managed Identity
5. Assign necessary roles (Contributor, Azure AI Developer)
6. Deploy the application
7. Configure environment variables

### 4.4 Monitor deployment

Watch the console output for any errors. The deployment takes approximately 5-10 minutes.

## Step 5: Verify Deployment

Once deployment completes, access your agent at:

```
https://swire-ops-manual-agent.azurewebsites.net
```

Test with questions like:
- "What are the safety procedures for Blades operations?"
- "Show me the pre-assembly installation guidelines"
- "What are the maintenance schedules for Service & Maintenance?"
- "What is Swire Renewable's HR policy on remote work?"
- "Tell me about Swire Renewable's company values"

## Step 6: Integration with Dynamics 365 (Optional)

To integrate with Swire's Dynamics 365 system:

1. Update `enterprise_functions.py` to add Dynamics 365 API calls
2. Add Dynamics 365 credentials to `.env`
3. Redeploy using `./deploy.sh`

Example function to add:

```python
def fetch_dynamics_data(entity: str, filter: str) -> str:
    """Fetch data from Dynamics 365 CRM"""
    # Implementation here
    pass
```

## Troubleshooting

### Issue: Agent not found
- Ensure you ran the Jupyter notebook first
- Verify AGENT_NAME matches the agent created in AI Foundry

### Issue: Vector store not found
- Check VECTOR_STORE_NAME in .env
- Verify documents were uploaded in the notebook

### Issue: Deployment fails
- Check Azure CLI is authenticated: `az account show`
- Verify subscription has necessary permissions
- Check resource group name doesn't conflict

### Issue: Web app doesn't start
- Check logs: `az webapp log tail --name swire-ops-manual-agent --resource-group swire-ops-manual-rg`
- Verify all environment variables are set correctly

## Next Steps

After successful deployment:

1. **Add more operations documents** - Upload additional manuals through the notebook
2. **Customize the UI** - Update `main.py` to match Swire branding
3. **Add Dynamics 365 integration** - Connect to existing CRM data
4. **Set up monitoring** - Enable Application Insights for usage tracking
5. **Configure authentication** - Add Azure AD authentication for secure access

## Support

For issues or questions:
- Check Azure Web App logs
- Review Application Insights metrics
- Consult Azure AI Agent Service documentation

## Cost Estimation

Approximate monthly costs:
- App Service Plan (B1): ~$13/month
- Azure AI Foundry: Pay-per-use (varies by usage)
- Azure AI Search (if used): ~$75/month (Basic tier)
- Total estimated: $100-200/month depending on usage

## Security Considerations

- Managed Identity is enabled (no credentials in code)
- All secrets stored in Azure App Settings
- HTTPS enforced by default
- Consider adding Azure AD authentication for production
