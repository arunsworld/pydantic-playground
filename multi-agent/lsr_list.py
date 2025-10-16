from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from textwrap import dedent
from typing import List
import json
from .lsr import LSRState
from .config import get_model

lsr_list_agent = Agent(
    get_model(),
    deps_type=StateDeps[List[LSRState]],
 )

@lsr_list_agent.instructions()
async def language_instructions(ctx: RunContext[StateDeps[List[LSRState]]]) -> str:
    """Instructions for the Legal Service Request agent.
    Args:
        ctx: The run context containing Legal Service Request state information.
    Returns:
        Instructions string for the Legal Service Request agent.
    """
    # ctx.deps.state is a list of dicts, not LSRState objects
    state_json = json.dumps(ctx.deps.state, indent=2)
    
    return dedent(
        f"""
        You are a helpful assistant for helping the user summarize and answer questions about the Legal Service Requests.
        The current state of the Legal Service Request is: "{state_json}"
        """
    )
