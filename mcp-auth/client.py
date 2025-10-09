from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
from typing import Any
import uuid
import os
load_dotenv()

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

server = MCPServerStreamableHTTP(mcp_endpoint, process_tool_call=process_tool_call)  
agent = Agent(
    agent_model,
    toolsets=[server],
    instructions="""You are a helpful assistant that can answer questions with the tools available to you. 
    If you cannot find an appropriate tool, you should respond by saying that you are unable to answer the question.
    You must use the tools available to you to answer the question.
    """
 )  

if __name__ == '__main__':
    jwttoken = str(uuid.uuid4())
    agent.to_cli_sync(deps={'jwttoken': jwttoken})