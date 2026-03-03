import os
import re
import signal
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from gradio import ChatMessage

# Lazy imports - only load when needed
project_client = None
agent = None
thread = None
toolset = None

load_dotenv(override=True)

def initialize_azure_client():
    """Lazy initialization of Azure AI client"""
    global project_client, agent, thread, toolset
    
    if project_client is not None:
        return  # Already initialized
    
    print("Initializing Azure AI client...")
    
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import (
        BingGroundingTool,
        FileSearchTool,
        FunctionTool,
        ToolSet
    )
    from azure.core.pipeline.policies import RetryPolicy
    from azure.core.pipeline.transport import RequestsTransport
    from enterprise_functions import enterprise_fns
    
    # Create Client
    credential = DefaultAzureCredential()
    retry_policy = RetryPolicy()
    transport = RequestsTransport(connection_timeout=600, read_timeout=600)
    
    # Parse connection string
    conn_str = os.environ["PROJECT_CONNECTION_STRING"]
    parts = conn_str.split(';')
    if len(parts) != 4:
        raise ValueError("Invalid PROJECT_CONNECTION_STRING format")
    
    hostname, subscription_id, resource_group_name, project_name = parts
    endpoint = f"https://{hostname}"
    
    project_client = AIProjectClient(
        endpoint=endpoint,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        project_name=project_name,
        credential=credential,
        retry_policy=retry_policy,
        transport=transport
    )
    
    # Find agent
    AGENT_NAME = os.environ["AGENT_NAME"]
    all_agents_list = list(project_client.agents.list_agents())
    found_agent = None
    for a in all_agents_list:
        if a.name == AGENT_NAME:
            found_agent = a
            break
    
    if not found_agent:
        raise ValueError(f"Agent '{AGENT_NAME}' not found")
    
    agent = found_agent
    print(f"Using agent > {agent.name} (id: {agent.id})")
    
    # Setup tools
    class LoggingToolSet(ToolSet):
        def add(self, tool):
            super().add(tool)
            tool_name = getattr(tool, 'name', type(tool).__name__)
            print(f"tool > added {tool_name}")
    
    toolset = LoggingToolSet()
    
    # Bing tool (optional)
    try:
        bing_connection = project_client.connections.get(connection_name=os.environ["BING_CONNECTION_NAME"])
        bing_tool = BingGroundingTool(connection_id=bing_connection.id)
        toolset.add(bing_tool)
        print("bing > connected")
    except Exception as e:
        print(f"bing > skipped ({e})")
    
    # Vector store (optional)
    try:
        VECTOR_STORE_NAME = os.environ["VECTOR_STORE_NAME"]
        all_vector_stores = list(project_client.agents.list_vector_stores())
        existing_vector_store = next(
            (store for store in all_vector_stores if store.name == VECTOR_STORE_NAME),
            None
        )
        if existing_vector_store:
            file_search_tool = FileSearchTool(vector_store_ids=[existing_vector_store.id])
            toolset.add(file_search_tool)
            print(f"file search > connected")
    except Exception as e:
        print(f"file search > skipped ({e})")
    
    # Custom functions
    custom_functions = FunctionTool(enterprise_fns)
    toolset.add(custom_functions)
    
    # Update agent with tools
    from azure.core.exceptions import ResourceExistsError
    import time
    
    def update_agent_with_retry(agent_id, model, instructions, toolset, retries=3, delay=5):
        for attempt in range(retries):
            try:
                return project_client.agents.update_agent(
                    assistant_id=agent_id,
                    model=model,
                    instructions=instructions,
                    toolset=toolset,
                )
            except ResourceExistsError:
                if attempt < retries - 1:
                    print(f"Retrying update_agent... attempt {attempt + 1}")
                    time.sleep(delay)
                else:
                    raise
    
    agent = update_agent_with_retry(
        agent_id=found_agent.id,
        model=found_agent.model,
        instructions=found_agent.instructions,
        toolset=toolset,
    )
    print(f"reusing agent > {agent.name} (id: {agent.id})")
    
    # Create thread
    thread = project_client.agents.create_thread()
    print(f"thread > created (id: {thread.id})")
    
    print("Azure AI client initialized successfully!")

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "azure_initialized": project_client is not None}

# Define Gradio interface
brand_theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="gray",
    font=["Segoe UI", "Arial", "sans-serif"],
    font_mono=["Courier New", "monospace"],
    text_size="lg",
).set(
    button_primary_background_fill="#0f6cbd",
    button_primary_background_fill_hover="#115ea3",
    button_primary_background_fill_hover_dark="#4f52b2",
    button_primary_background_fill_dark="#5b5fc7",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#e0e0e0",
    button_secondary_background_fill_hover="#c0c0c0",
    button_secondary_background_fill_hover_dark="#a0a0a0",
    button_secondary_text_color="#000000",
    body_background_fill="#f5f5f5",
    block_background_fill="#ffffff",
    body_text_color="#242424",
    body_text_color_subdued="#616161",
    block_border_color="#d1d1d1",
    block_border_color_dark="#333333",
    input_background_fill="#ffffff",
    input_border_color="#d1d1d1",
    input_border_color_focus="#0f6cbd",
)

def azure_enterprise_chat(user_message: str, history: List[dict]):
    """Chat function - initializes Azure on first use"""
    global project_client, agent, thread
    
    # Lazy initialization on first chat
    if project_client is None:
        try:
            initialize_azure_client()
        except Exception as e:
            error_msg = f"Failed to initialize Azure AI: {str(e)}"
            print(error_msg)
            return history + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": f"⚠️ {error_msg}\n\nPlease check your Azure configuration and try again."}
            ], ""
    
    # Convert history to ChatMessage
    conversation = []
    for msg_dict in history:
        conversation.append(ChatMessage(
            role=msg_dict["role"],
            content=msg_dict["content"],
            metadata=msg_dict.get("metadata", None)
        ))
    
    # Add user message
    conversation.append(ChatMessage(role="user", content=user_message))
    yield conversation, ""
    
    # Post to thread
    project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    
    # Simple response for now (full streaming implementation would go here)
    conversation.append(ChatMessage(
        role="assistant",
        content="Azure AI agent is processing your request..."
    ))
    
    yield conversation, ""

with gr.Blocks(theme=brand_theme, css="footer {visibility: hidden;}", fill_height=True) as demo:
    
    def clear_thread():
        global thread
        if project_client:
            thread = project_client.agents.create_thread()
        return []
    
    def on_example_clicked(evt: gr.SelectData):
        return evt.value["text"]
    
    gr.HTML("<h1 style='text-align: center;'>Swire Renewable - Operations & HR Assistant</h1>")
    
    chatbot = gr.Chatbot(
        type="messages",
        examples=[
            {"text": "What are the blade handling safety procedures?"},
            {"text": "Show me the pre-assembly installation checklist"},
            {"text": "What's the HR policy on vacation time?"},
            {"text": "Tell me about Swire Renewable's company values"},
        ],
        show_label=False,
        scale=1,
    )
    
    textbox = gr.Textbox(
        show_label=False,
        lines=1,
        submit_btn=True,
    )
    
    chatbot.example_select(fn=on_example_clicked, inputs=None, outputs=textbox)
    
    (textbox
     .submit(
         fn=azure_enterprise_chat,
         inputs=[textbox, chatbot],
         outputs=[chatbot, textbox],
     )
     .then(
         fn=lambda: "",
         outputs=textbox,
     )
    )
    
    chatbot.clear(fn=clear_thread, outputs=chatbot)

# Mount Gradio
app = gr.mount_gradio_app(app, demo, path="/")

# Signal handler
def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    raise SystemExit(0)

signal.signal(signal.SIGINT, signal_handler)
