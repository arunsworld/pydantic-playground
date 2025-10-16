from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
from typing import Any
from fastapi import FastAPI, Request
from pydantic_ai.ag_ui import handle_ag_ui_request, run_ag_ui
from ag_ui.core import StateSnapshotEvent, EventType, StateDeltaEvent
import uvicorn
import sys
import os
import asyncio
from pydantic import BaseModel
from enum import Enum
from pydantic_ai.ag_ui import StateDeps
from textwrap import dedent
from datetime import datetime
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel
load_dotenv()


# Default port
port = 9010

# Check if a port is provided as a command line argument
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port '{sys.argv[1]}', using default port {port}")


mcp_endpoint = os.environ.get("MCP_ENDPOINT", "http://localhost:8910/mcp")
print(f"mcp_endpoint: {mcp_endpoint}")
agent_model = os.environ.get("AGENT_MODEL", "openai:gpt-4.1")
print(f"agent_model: {agent_model}")

app = FastAPI(
    title="AskAI API",
    description="AI-powered chat API with session management and AG-UI protocol",
)

class LSRType(str, Enum):
    CONTRACT_REVIEW = "Contract Review"
    LEGAL_OPINION = "Legal Opinion"
    LITIGATION_SUPPORT = "Litigation Support"
    COMPLIANCE_REVIEW = "Compliance Review"
    INTELLECTUAL_PROPERTY = "Intellectual Property"
    EMPLOYMENT_LAW = "Employment Law"
    REGULATORY_MATTERS = "Regulatory Matters"
    OTHER = "Other"
    NONE = ""

class LSRPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    NONE = ""

class LSRState(BaseModel):
    title: str = ''
    description: str = ''
    requestorName: str = ''
    requestorEmail: str = ''
    requestorDepartment: str = ''
    requestType: LSRType = ''
    priority: LSRPriority = ''
    dueDate: str = ''
    estimatedHours: int = 0
    notes: str = ''

ollama_model = OpenAIChatModel(
    model_name='gpt-oss:20b',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
)

agent = Agent(
    agent_model,
    # ollama_model,
    deps_type=StateDeps[LSRState],
 )

@agent.instructions()
async def language_instructions(ctx: RunContext[StateDeps[LSRState]]) -> str:
    """Instructions for the Legal Service Request agent.
    Args:
        ctx: The run context containing Legal Service Request state information.
    Returns:
        Instructions string for the Legal Service Request agent.
    """
    return dedent(
        f"""
        You are a helpful assistant for helping the user fill out and edit an Legal Service Request form.
        The current state of the Legal Service Request is: "{ctx.deps.state.model_dump_json(indent=2)}"
        The date today is: "{datetime.now().strftime('%Y-%m-%d')}" to help you with date calculations.

        Call the populate_lsr tool to populate the Legal Service Request with data from the user.
        Make your best guesses for any missing data from the user.
        """
    )

@agent.tool
def populate_lsr(ctx: RunContext[StateDeps[LSRState]], lsr: LSRState) -> StateSnapshotEvent:
    """Populate the Legal Service Request with data from the user. 
    Use this tool also when the user asks to create a new Legal Service Request also known as LSR.

    IMPORTANT:
        Title, Description and Due Date are mandatory.
        If the request type and priority are blank, make your best guess at it
        Estimated hours are optional.
        Additional notes are optional.
    """
    updatedLSR = ctx.deps.state.model_copy()
    
    # Update fields from lsr only if they are not blank/empty
    if lsr.title.strip():
        updatedLSR.title = lsr.title
    if lsr.description.strip():
        updatedLSR.description = lsr.description
    if lsr.requestorName.strip():
        updatedLSR.requestorName = lsr.requestorName
    if lsr.requestorEmail.strip():
        updatedLSR.requestorEmail = lsr.requestorEmail
    if lsr.requestorDepartment.strip():
        updatedLSR.requestorDepartment = lsr.requestorDepartment
    if lsr.requestType:
        updatedLSR.requestType = lsr.requestType
    if lsr.priority:
        updatedLSR.priority = lsr.priority
    if lsr.dueDate.strip():
        updatedLSR.dueDate = lsr.dueDate
    if lsr.estimatedHours>0:
        updatedLSR.estimatedHours = lsr.estimatedHours
    if lsr.notes.strip():
        updatedLSR.notes = lsr.notes
    
    return StateSnapshotEvent(snapshot=updatedLSR)

@app.post("/")
async def run_agent(request: Request):
    """Run the agent via AG-UI and persist assistant messages on completion."""
    #     )

    # run_ag_ui()
    
    return await handle_ag_ui_request(
        agent,
        request,
        deps=StateDeps(LSRState()),
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="debug",
    )

