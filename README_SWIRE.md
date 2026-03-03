# Swire Renewable - Operations & HR AI Agent

Enterprise AI-powered operations manual and HR policy assistant for Swire Renewable Energy, built on Azure AI Agent Service.

## Overview

This intelligent agent provides instant access to operations manuals, HR policies, safety procedures, and departmental documentation across Swire Renewable's organization. Built on Azure AI Agent Service with GPT-4o, it delivers real-time answers using company documentation through retrieval-augmented generation (RAG).

## Departments Covered

- **Blades** - Manufacturing, inspection, and quality control
- **Pre-Assembly & Installation** - Site preparation and turbine installation
- **Service & Maintenance** - Ongoing maintenance and repairs
- **HR** - Human resources policies and procedures
- **Company Information** - About Swire Renewable, values, and structure
- **General** - Cross-departmental policies and procedures

## Features

### Core Capabilities
- **Instant Documentation Access** - Query any operations manual or policy document
- **Cross-Department Search** - Find related procedures across departments
- **Safety Information** - Quick access to safety protocols and procedures
- **Training Requirements** - Identify required training and certifications
- **Real-Time Answers** - Streaming responses with source citations
- **Bing Integration** - Access to current industry information and regulations

### Technical Features
- **Vector Store RAG** - Semantic search across all documentation
- **Streaming Responses** - Real-time partial updates
- **Tool Integration** - Extensible with custom functions
- **Managed Identity** - Secure Azure authentication
- **Gradio UI** - Interactive chat interface
- **FastAPI Backend** - Scalable REST API

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Swire Renewable Users                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Azure Web App (Gradio Interface)                │
│                  swire-ops-manual-agent                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Azure AI Agent Service                      │
│                      (GPT-4o Model)                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌───────────────────────┐   ┌───────────────────────┐
│   Vector Store        │   │   Bing Grounding      │
│   (Operations Docs)   │   │   (Web Search)        │
└───────────────────────┘   └───────────────────────┘
```

## Quick Start

### Prerequisites
- Azure subscription (Azure subscription 1)
- Azure AI Foundry project
- Python 3.10+
- Azure CLI

### Deployment

1. **Configure environment:**
```bash
cd infra/azure-deployment
cp .env.example .env
# Edit .env with your Azure AI Foundry connection string
```

2. **Create agent and upload documents:**
```bash
# Run the Jupyter notebook
jupyter notebook ../../enterprise-streaming-agent.ipynb
```

3. **Deploy to Azure:**
```bash
chmod +x deploy.sh
./deploy.sh
```

4. **Access the agent:**
```
https://swire-ops-manual-agent.azurewebsites.net
```

See [SWIRE_DEPLOYMENT_GUIDE.md](infra/azure-deployment/SWIRE_DEPLOYMENT_GUIDE.md) for detailed instructions.

## Documentation Structure

Operations manuals are organized by department:

```
enterprise-data/
├── blades/
│   ├── operations_manual.md
│   ├── safety_procedures.md
│   └── quality_standards.md
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
│   └── about_swire_renewable.md
└── general/
    ├── safety_policies.md
    └── compliance_procedures.md
```

See [SWIRE_DOCUMENT_STRUCTURE.md](infra/azure-deployment/SWIRE_DOCUMENT_STRUCTURE.md) for complete structure guidelines.

## Example Queries

- "What are the safety procedures for blade handling?"
- "Show me the pre-assembly installation checklist"
- "What are the maintenance schedules for wind turbines?"
- "What is the HR policy on vacation time?"
- "Tell me about Swire Renewable's sustainability commitment"
- "What training is required for installation technicians?"

## Integration with Existing Systems

### Dynamics 365 Integration
The agent can be extended to integrate with Swire's Dynamics 365 CRM:
- Employee data lookup
- Service ticket information
- Asset management data
- Customer information

### Microsoft 365 Integration
- SharePoint document access
- Teams notifications
- Outlook calendar integration
- OneDrive document storage

## Security & Compliance

- **Managed Identity** - No credentials stored in code
- **Azure AD Authentication** - Secure user access (configurable)
- **HTTPS Only** - Encrypted communication
- **Role-Based Access** - Department-specific permissions (future)
- **Audit Logging** - Application Insights tracking

## Cost Estimation

Approximate monthly costs:
- App Service Plan (B1): ~$13/month
- Azure AI Foundry: Pay-per-use (~$50-100/month)
- Azure AI Search: ~$75/month (Basic tier)
- **Total: ~$150-200/month**

## Roadmap

### Phase 1: Base Deployment ✓
- [x] Azure infrastructure setup
- [x] Agent deployment
- [x] Document upload
- [x] Basic chat interface

### Phase 2: Operations Manual Features (In Progress)
- [ ] Structured document generation
- [ ] Policy document templates
- [ ] Cross-department linking
- [ ] Document approval workflows

### Phase 3: Advanced Integration
- [ ] Dynamics 365 integration
- [ ] Microsoft Teams bot
- [ ] Mobile app
- [ ] Advanced analytics

### Phase 4: AI-Powered Features
- [ ] Automated policy generation from business intelligence
- [ ] Compliance checking
- [ ] Procedure optimization suggestions
- [ ] Predictive maintenance insights

## Support & Maintenance

### Monitoring
- Application Insights for usage tracking
- Azure Monitor for infrastructure health
- Custom alerts for errors and performance

### Updates
- Quarterly document reviews
- Monthly agent performance optimization
- Continuous security updates

## Contributing

This is a private repository for Swire Renewable. For internal contributions:
1. Create a feature branch
2. Make your changes
3. Submit a pull request
4. Request review from team lead

## License

Proprietary - Swire Renewable Energy
All rights reserved.

## Contact

For questions or support:
- **Technical Issues:** [Your IT Support Email]
- **Content Updates:** [Department Managers]
- **Access Requests:** [HR Contact]

## Acknowledgments

Built on [Azure AI Agent Service Enterprise Demo](https://github.com/Azure-Samples/azure-ai-agent-service-enterprise-demo)
- Azure AI Agent Service
- Gradio UI Framework
- FastAPI Backend

---

**Swire Renewable Energy** - Powering a sustainable future
