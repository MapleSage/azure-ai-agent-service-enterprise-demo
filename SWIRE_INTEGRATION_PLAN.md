# Swire Renewable - Complete Integration Plan

## Overview

This document outlines how to integrate the new Operations & HR Agent with your existing Swire Intelligence Assistant infrastructure.

## Current State

### Existing Systems

1. **SageGreen AI (swire-intelligence-assistant)**
   - URL: https://sagegreen.vercel.app
   - Backend: Azure Container Instance (20.72.179.10)
   - Tech: Next.js frontend + FastAPI multi-agent backend
   - Knowledge: Azure Cognitive Search (swire-wind-services index)
   - Focus: ESG & Renewable Energy

2. **Swire Copilot Assistant**
   - Platform: Microsoft Copilot Studio
   - Integration: Teams, Power BI
   - Region: West Europe (EU compliance)
   - Focus: Enterprise data (Finance, HSE, HR)

3. **New Operations Agent (swireops)**
   - URL: https://swire-ops-manual-agent.azurewebsites.net
   - Status: Deployed but timing out
   - Tech: Gradio UI + Azure AI Agent Service
   - Focus: Operations manuals & HR policies

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIFIED SWIRE ASSISTANT                       │
│                                                                   │
│  Single entry point for all Swire AI services                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   SageGreen  │  │  Operations  │  │   Copilot    │
│   AI Agent   │  │  Manual      │  │   Studio     │
│              │  │  Agent       │  │              │
│  ESG &       │  │              │  │  Enterprise  │
│  Renewable   │  │  Ops & HR    │  │  Data        │
│  Energy      │  │  Policies    │  │  (Teams/PBI) │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Phase 1: Fix Current Deployment (Immediate)

### Issue: Gateway Timeout

**Root Cause**: App tries to initialize Azure AI client on startup, which takes too long.

**Solution**: Already implemented in `main_fixed.py` - lazy initialization

**Steps to Deploy**:

```bash
cd azure-ai-agent-service-enterprise-demo/infra/azure-deployment

# The fixed version is already in place
# Just need to restart the app service

az webapp restart --name swire-ops-manual-agent --resource-group swire-ops-manual-rg

# Wait 30 seconds, then test
curl https://swire-ops-manual-agent.azurewebsites.net/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "azure_initialized": false
}
```

After first chat message, it will initialize and return:
```json
{
  "status": "healthy",
  "azure_initialized": true
}
```

## Phase 2: Integrate with Existing SageGreen Backend

### Option A: Add Operations Agent to FastAPI Multi-Agent System

Add a new specialist agent to your existing `swire-agent-core`:

**File**: `swire-intelligence-assistant/swire-agent-core/src/agents/operations_specialist_agent.py`

```python
class OperationsSpecialistAgent:
    """
    Specialist agent for operations manuals and HR policies
    """
    def __init__(self, azure_client):
        self.azure_client = azure_client
        self.domain = "operations"
        self.capabilities = [
            "blade_operations",
            "pre_assembly",
            "installation",
            "service_maintenance",
            "hr_policies",
            "safety_procedures"
        ]
    
    def can_handle(self, query: str) -> bool:
        keywords = [
            "operations", "manual", "procedure", "hr", "policy",
            "blade", "installation", "maintenance", "safety",
            "vacation", "training", "certification"
        ]
        return any(kw in query.lower() for kw in keywords)
    
    def process(self, query: str) -> dict:
        # Connect to swire-gpt-4o agent
        # Use Azure AI Agent Service
        # Return structured response
        pass
```

**Update**: `swire-intelligence-assistant/swire-agent-core/src/agents/multi_agent_orchestrator.py`

```python
from .operations_specialist_agent import OperationsSpecialistAgent

class MultiAgentOrchestrator:
    def __init__(self):
        # ... existing agents ...
        self.operations_agent = OperationsSpecialistAgent(azure_client)
        self.agents.append(self.operations_agent)
```

### Option B: Create Unified API Gateway

Create a new API that routes to appropriate backend:

**File**: `swire-unified-gateway/main.py`

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

BACKENDS = {
    "sagegreen": "http://20.72.179.10",
    "operations": "https://swire-ops-manual-agent.azurewebsites.net",
    "copilot": "https://copilot-studio-endpoint"
}

@app.post("/chat")
async def unified_chat(query: str):
    # Analyze query
    if is_operations_query(query):
        backend = BACKENDS["operations"]
    elif is_esg_query(query):
        backend = BACKENDS["sagegreen"]
    else:
        backend = BACKENDS["copilot"]
    
    # Forward to appropriate backend
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{backend}/chat", json={"query": query})
        return response.json()
```

## Phase 3: Add Operations Manual Features

### Feature 1: Document Structure Management

Create structured templates for each department:

```python
# swire-agent-core/src/tools/operations_manual.py

DEPARTMENT_TEMPLATES = {
    "blades": {
        "sections": [
            "Safety Procedures",
            "Quality Standards",
            "Maintenance Guidelines",
            "Inspection Checklist"
        ]
    },
    "pre_assembly_installation": {
        "sections": [
            "Site Preparation",
            "Assembly Procedures",
            "Installation Guidelines",
            "Safety Protocols"
        ]
    },
    # ... other departments
}

def generate_operations_manual(department: str, data: dict) -> str:
    """Generate structured operations manual from business data"""
    template = DEPARTMENT_TEMPLATES[department]
    # Use Azure OpenAI to generate content
    # Apply structure and formatting
    return formatted_manual
```

### Feature 2: Policy Document Generation

```python
# swire-agent-core/src/tools/policy_generator.py

def generate_policy_document(
    policy_type: str,
    business_intelligence: dict,
    compliance_requirements: list
) -> str:
    """
    Generate policy documents based on business intelligence
    
    Args:
        policy_type: "hr", "safety", "environmental", etc.
        business_intelligence: Data from Dynamics 365, Power BI
        compliance_requirements: Regulatory requirements
    
    Returns:
        Formatted policy document
    """
    # Use Azure OpenAI with specific prompts
    # Include compliance checks
    # Format according to company standards
    pass
```

### Feature 3: Dynamics 365 Integration

```python
# swire-agent-core/src/integrations/dynamics365.py

from msal import ConfidentialClientApplication
import requests

class Dynamics365Client:
    def __init__(self):
        self.authority = "https://login.microsoftonline.com/YOUR_TENANT_ID"
        self.client_id = os.getenv("DYNAMICS_CLIENT_ID")
        self.client_secret = os.getenv("DYNAMICS_CLIENT_SECRET")
        self.resource = "https://YOUR_ORG.crm.dynamics.com"
    
    def get_employee_data(self, employee_id: str):
        """Fetch employee data from Dynamics 365"""
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{self.resource}/api/data/v9.2/contacts({employee_id})",
            headers=headers
        )
        return response.json()
    
    def get_service_tickets(self, filters: dict):
        """Fetch service tickets"""
        # Query Dynamics 365 CRM
        pass
```

## Phase 4: Unified Frontend

### Option A: Extend SageGreen Frontend

Add operations manual tab to existing Next.js app:

```typescript
// swire-frontend/pages/operations.tsx

export default function OperationsPage() {
  return (
    <div>
      <h1>Operations & HR Assistant</h1>
      <ChatInterface 
        backend="/api/operations-chat"
        examples={[
          "What are the blade handling safety procedures?",
          "Show me the pre-assembly checklist",
          "What's the HR policy on vacation?"
        ]}
      />
    </div>
  );
}
```

### Option B: Create Unified Portal

New Next.js app that combines all services:

```
swire-unified-portal/
├── pages/
│   ├── index.tsx           # Landing page
│   ├── esg.tsx            # SageGreen AI
│   ├── operations.tsx      # Operations Manual
│   └── copilot.tsx        # Copilot Studio embed
├── components/
│   ├── UnifiedChat.tsx    # Smart routing chat
│   └── ServiceSelector.tsx # Choose which service
└── api/
    └── unified-chat.ts    # Routes to appropriate backend
```

## Phase 5: Teams Integration

### Integrate Operations Agent into Teams

**File**: `swire-copilot-assistant/teams-integration/manifest.json`

Add operations agent as a bot:

```json
{
  "bots": [
    {
      "botId": "operations-agent-bot-id",
      "scopes": ["personal", "team"],
      "commandLists": [
        {
          "commands": [
            {
              "title": "Operations Manual",
              "description": "Search operations manuals"
            },
            {
              "title": "HR Policies",
              "description": "Find HR policies and procedures"
            }
          ]
        }
      ]
    }
  ]
}
```

## Deployment Strategy

### Recommended Approach

1. **Week 1**: Fix current deployment timeout
   - Deploy `main_fixed.py`
   - Test basic functionality
   - Add operations documents to vector store

2. **Week 2**: Integrate with SageGreen backend
   - Add OperationsSpecialistAgent
   - Test multi-agent routing
   - Deploy to Azure Container Instance

3. **Week 3**: Add operations manual features
   - Document structure templates
   - Policy generation
   - Dynamics 365 integration

4. **Week 4**: Unified frontend
   - Extend SageGreen UI or create new portal
   - Teams integration
   - User testing

## Configuration

### Environment Variables

Add to all services:

```bash
# Operations Agent
OPERATIONS_AGENT_URL=https://swire-ops-manual-agent.azurewebsites.net
OPERATIONS_AGENT_ID=swire-gpt-4o

# Dynamics 365
DYNAMICS_TENANT_ID=your-tenant-id
DYNAMICS_CLIENT_ID=your-client-id
DYNAMICS_CLIENT_SECRET=your-secret
DYNAMICS_RESOURCE=https://your-org.crm.dynamics.com

# Unified Gateway
SAGEGREEN_BACKEND=http://20.72.179.10
COPILOT_ENDPOINT=your-copilot-endpoint
```

## Testing Plan

### Unit Tests
```bash
# Test operations agent
pytest swire-agent-core/tests/test_operations_agent.py

# Test policy generation
pytest swire-agent-core/tests/test_policy_generator.py

# Test Dynamics 365 integration
pytest swire-agent-core/tests/test_dynamics365.py
```

### Integration Tests
```bash
# Test unified routing
pytest tests/test_unified_routing.py

# Test end-to-end flow
pytest tests/test_e2e_operations.py
```

## Monitoring & Observability

### Application Insights

Add to all services:

```python
from applicationinsights import TelemetryClient

tc = TelemetryClient(os.getenv("APPINSIGHTS_KEY"))

@app.post("/chat")
async def chat(query: str):
    tc.track_event("chat_request", {"query_length": len(query)})
    # ... process ...
    tc.track_metric("response_time", response_time)
```

### Dashboards

Create Power BI dashboard showing:
- Usage by department
- Most common queries
- Response times
- Error rates
- User satisfaction

## Security Considerations

1. **Authentication**: Use Azure AD for all services
2. **Authorization**: Role-based access control (RBAC)
3. **Data Encryption**: All data encrypted at rest and in transit
4. **Audit Logging**: Log all access to sensitive documents
5. **Compliance**: GDPR compliance for EU data

## Cost Optimization

### Current Costs
- SageGreen: ~$150/month (Container Instance + Cognitive Search)
- Operations Agent: ~$150/month (App Service + AI Agent Service)
- Copilot Studio: Included in M365 licenses

### Optimization
- Use same Azure AI Foundry project for both agents
- Share Cognitive Search service
- Use B1 tier for development, scale to P1V2 for production

## Next Steps

1. **Immediate**: Restart the operations agent app service
2. **This Week**: Add operations documents to vector store
3. **Next Week**: Integrate with SageGreen backend
4. **Month 1**: Complete unified portal
5. **Month 2**: Teams integration and user training

## Support & Documentation

- Technical docs: `docs/` directory
- API documentation: Auto-generated with FastAPI
- User guides: Create in SharePoint
- Training videos: Record and upload to Teams

---

**Created**: March 3, 2026
**Status**: Planning
**Owner**: Swire IT Team
