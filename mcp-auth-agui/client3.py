from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
from typing import Any
from fastapi import FastAPI, Request
from pydantic_ai.ag_ui import handle_ag_ui_request
import uvicorn
import sys
import os
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

async def process_tool_call(
    ctx: RunContext[Any],
    call_tool,
    name: str,
    tool_args: dict[str, Any],
) -> Any:
    """Process tool calls by adding session ID metadata"""

    metadata = {
        "jwttoken": ctx.deps['jwttoken']
    }

    # Call the MCP tool with metadata
    return await call_tool(name, tool_args, metadata)

# server = MCPServerStreamableHTTP(mcp_endpoint, process_tool_call=process_tool_call)
agent = Agent(
    agent_model,
    # toolsets=[server],
    instructions="""You are a helpful assistant that can answer questions with the tools available to you. 
    If you cannot find an appropriate tool, you should respond by saying that you are unable to answer the question.
    You must use the tools available to you to answer the question.
    """
 )

app = FastAPI(
    title="AskAI API",
    description="AI-powered chat API with session management and AG-UI protocol",
)

@app.post("/")
async def run_agent(request: Request):
    """Run the agent via AG-UI and persist assistant messages on completion."""

    print(f"request: {request.headers}")
    jwttoken = request.headers.get("jwttoken")
    print(f"jwttoken: {jwttoken}")

    server = MCPServerStreamableHTTP(mcp_endpoint, process_tool_call=process_tool_call)  

    return await handle_ag_ui_request(
        agent,
        request,
        deps={'jwttoken': jwttoken},
        toolsets=[server],
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="debug",
    )

