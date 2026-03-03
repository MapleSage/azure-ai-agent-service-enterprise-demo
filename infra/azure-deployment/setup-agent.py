#!/usr/bin/env python3
"""
Swire Renewable - Automated Agent Setup
Creates the AI agent, vector store, and uploads documents
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()

def main():
    print("=" * 60)
    print("Swire Renewable - Agent Setup")
    print("=" * 60)
    print()
    
    # Check required environment variables
    conn_str = os.getenv("PROJECT_CONNECTION_STRING")
    if not conn_str or conn_str == "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>":
        print("❌ ERROR: PROJECT_CONNECTION_STRING not configured in .env")
        print("Please update .env with your Azure AI Foundry connection string")
        sys.exit(1)
    
    agent_name = os.getenv("AGENT_NAME", "swire-operations-manual-assistant")
    vector_store_name = os.getenv("VECTOR_STORE_NAME", "swire-ops-docs-vectorstore")
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    
    print(f"Agent Name: {agent_name}")
    print(f"Vector Store: {vector_store_name}")
    print(f"Model: {model_name}")
    print()
    
    # Initialize Azure AI Project Client
    print("🔗 Connecting to Azure AI Foundry...")
    try:
        credential = DefaultAzureCredential()
        
        # Parse connection string: hostname;subscription;resourcegroup;projectname
        parts = conn_str.split(';')
        if len(parts) != 4:
            print(f"❌ Invalid connection string format")
            print("Expected format: hostname;subscription;resourcegroup;projectname")
            sys.exit(1)
        
        hostname, subscription_id, resource_group_name, project_name = parts
        endpoint = f"https://{hostname}"
        
        project_client = AIProjectClient(
            endpoint=endpoint,
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            project_name=project_name,
            credential=credential
        )
        print("✓ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    
    print()
    
    # Check if agent already exists
    print(f"🤖 Checking for existing agent '{agent_name}'...")
    existing_agent = None
    try:
        agents = list(project_client.agents.list_agents())
        for agent in agents:
            if agent.name == agent_name:
                existing_agent = agent
                break
        
        if existing_agent:
            print(f"✓ Agent already exists (ID: {existing_agent.id})")
            print("  Skipping agent creation")
        else:
            print("  Agent not found, creating new agent...")
            
            # Create agent
            agent = project_client.agents.create_agent(
                model=model_name,
                name=agent_name,
                instructions="""You are an operations and HR assistant for Swire Renewable Energy. 
                
Your role is to help employees find information about:
- Operations manuals and procedures for all departments (Blades, Pre-Assembly & Installation, Service & Maintenance)
- HR policies and employee information
- Safety procedures and compliance requirements
- Company information and values
- Training requirements and certifications

Always provide accurate, helpful information based on the company documentation. 
If you're unsure about something, say so and suggest who to contact.
Prioritize safety and compliance in all responses."""
            )
            print(f"✓ Agent created successfully (ID: {agent.id})")
            existing_agent = agent
    except Exception as e:
        print(f"❌ Agent setup failed: {e}")
        sys.exit(1)
    
    print()
    
    # Check if vector store already exists
    print(f"📚 Checking for existing vector store '{vector_store_name}'...")
    existing_vector_store = None
    try:
        vector_stores = list(project_client.agents.list_vector_stores())
        for store in vector_stores:
            if store.name == vector_store_name:
                existing_vector_store = store
                break
        
        if existing_vector_store:
            print(f"✓ Vector store already exists (ID: {existing_vector_store.id})")
            print("  Skipping vector store creation")
        else:
            print("  Vector store not found, creating new vector store...")
            
            # Create vector store
            vector_store = project_client.agents.create_vector_store_and_poll(
                name=vector_store_name,
                file_ids=[]
            )
            print(f"✓ Vector store created successfully (ID: {vector_store.id})")
            existing_vector_store = vector_store
    except Exception as e:
        print(f"❌ Vector store setup failed: {e}")
        sys.exit(1)
    
    print()
    
    # Upload documents
    print("📄 Checking for documents to upload...")
    docs_path = Path("../../enterprise-data")
    
    if not docs_path.exists():
        print(f"⚠ Warning: {docs_path} not found")
        print("  No documents to upload. You can add documents later.")
    else:
        # Find all markdown and text files
        doc_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.txt"))
        doc_files = [f for f in doc_files if not f.name.startswith('.')]
        
        if not doc_files:
            print("  No documents found in enterprise-data/")
            print("  Add your operations manuals and run this script again to upload them")
        else:
            print(f"  Found {len(doc_files)} document(s)")
            print()
            print("📤 Uploading documents to vector store...")
            
            uploaded_count = 0
            for doc_file in doc_files:
                try:
                    rel_path = doc_file.relative_to(docs_path)
                    print(f"  Uploading: {rel_path}...", end=" ")
                    
                    with open(doc_file, "rb") as f:
                        file = project_client.agents.upload_file_and_poll(
                            file=f,
                            purpose="assistants"
                        )
                    
                    # Add file to vector store
                    project_client.agents.create_vector_store_file_and_poll(
                        vector_store_id=existing_vector_store.id,
                        file_id=file.id
                    )
                    
                    print("✓")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ ({e})")
            
            print()
            print(f"✓ Uploaded {uploaded_count}/{len(doc_files)} documents successfully")
    
    print()
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print(f"Agent ID: {existing_agent.id}")
    print(f"Agent Name: {existing_agent.name}")
    print(f"Vector Store ID: {existing_vector_store.id}")
    print(f"Vector Store Name: {existing_vector_store.name}")
    print()
    print("Next step: Run the deployment script")
    print("  cd infra/azure-deployment")
    print("  ./deploy.sh")
    print()

if __name__ == "__main__":
    main()
