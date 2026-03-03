# Swire Renewable Deployment Checklist

## Pre-Deployment

- [ ] Azure CLI installed and authenticated (`az login`)
- [ ] Azure subscription set to "Azure subscription 1"
- [ ] Python 3.10+ installed
- [ ] Azure AI Foundry project created or identified
- [ ] Operations manual documents prepared

## Configuration

- [ ] Update `PROJECT_CONNECTION_STRING` in `.env`
- [ ] Verify `AGENT_NAME` matches agent in AI Foundry
- [ ] Verify `VECTOR_STORE_NAME` matches vector store in AI Foundry
- [ ] (Optional) Configure `BING_CONNECTION_NAME` if using Bing
- [ ] (Optional) Add OpenWeather API keys if needed

## Agent Setup (Run Jupyter Notebook First)

- [ ] Open `enterprise-streaming-agent.ipynb`
- [ ] Run all cells to create agent
- [ ] Upload Swire operations documents to vector store
- [ ] Test agent locally
- [ ] Note the agent name and vector store name

## Deployment

- [ ] Navigate to `infra/azure-deployment/`
- [ ] Make deploy script executable: `chmod +x deploy.sh`
- [ ] Run deployment: `./deploy.sh`
- [ ] Monitor console output for errors
- [ ] Wait for deployment to complete (5-10 minutes)

## Post-Deployment Verification

- [ ] Access web app: `https://swire-ops-manual-agent.azurewebsites.net`
- [ ] Test with sample questions
- [ ] Verify document search is working
- [ ] Check agent responses are accurate
- [ ] Review application logs if needed

## Optional Enhancements

- [ ] Add Dynamics 365 integration
- [ ] Customize UI with Swire branding
- [ ] Enable Application Insights monitoring
- [ ] Configure Azure AD authentication
- [ ] Set up custom domain
- [ ] Configure backup and disaster recovery

## Resources Created

After deployment, these resources will exist in Azure:

- Resource Group: `swire-ops-manual-rg`
- App Service Plan: `swire-ops-manual-plan`
- Web App: `swire-ops-manual-agent`
- Managed Identity: Automatically created for the web app

## Rollback Plan

If deployment fails or issues occur:

1. Delete the resource group: `az group delete --name swire-ops-manual-rg`
2. Fix configuration issues
3. Re-run deployment

## Next Phase: Operations Manual Features

After base deployment is working:

- [ ] Create spec for operations manual structure
- [ ] Add policy document generation
- [ ] Implement business intelligence integration
- [ ] Add multi-business unit support
- [ ] Create document templates
