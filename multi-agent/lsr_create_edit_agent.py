from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from textwrap import dedent
from datetime import datetime
from ag_ui.core import StateSnapshotEvent
from .lsr import LSRState
from .config import get_model

lsr_create_edit_agent = Agent(
    get_model(),
    deps_type=StateDeps[LSRState],
 )

@lsr_create_edit_agent.instructions()
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

@lsr_create_edit_agent.tool
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