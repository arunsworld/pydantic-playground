import uvicorn
from fastapi import FastAPI, Request
from pydantic_ai.ag_ui import handle_ag_ui_request
from pydantic_ai.mcp import MCPServerStreamableHTTP

from typing import List
from pydantic_ai.ag_ui import StateDeps
from .data_agent import data_agent
from .lsr_create_edit_agent import lsr_create_edit_agent
from .lsr import LSRState
from .lsr_list import lsr_list_agent
from .config import APP_HOST, APP_PORT

app = FastAPI(
    title="Multi-Agent API",
    description="Multi-Agent API with AG-UI support",
)

@app.post("/lsr-list")
async def lsr_list(request: Request):
    return await handle_ag_ui_request(
        lsr_list_agent,
        request,
        deps=StateDeps(list[LSRState]()),
    )

@app.post("/lsr-create-edit")
async def lsr_create_edit(request: Request):
    return await handle_ag_ui_request(
        lsr_create_edit_agent,
        request,
        deps=StateDeps(LSRState()),
    )

@app.post("/data-agent")
async def data(request: Request):
    return await handle_ag_ui_request(
        data_agent,
        request,
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=APP_HOST,
        port=APP_PORT,
        reload=False,
        log_level="debug",
    )
