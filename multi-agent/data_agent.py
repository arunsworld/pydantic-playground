from pydantic_ai import Agent
from .config import get_model
from pydantic import BaseModel
import uuid
import time
import random

data_agent = Agent(
    get_model(),
    instructions="""You are a helpful assistant that can answer questions with the tools available to you. 
    If you cannot find an appropriate tool, you should respond by saying that you are unable to answer the question.
    You must use the tools available to you to answer the question.
    """
 )

class AvailableSeats(BaseModel):
    venue: str
    seats: int

@data_agent.tool_plain
def available_seats(venue: str = 'Wembley Stadium') -> AvailableSeats:
    """Respond to the user's request for available seats. If not venue is provided, default to Wembley Stadium.
    
    Args:
        venue: The venue to check for available seats (optional, default: Wembley Stadium)

    Returns:
        The number of available seats
    """
    
    return AvailableSeats(venue=venue, seats=random.randint(0, 100))

class AnalyticalQueryResponse(BaseModel):
    job_id: str
    callback_webhook: str

@data_agent.tool_plain
def start_analytical_query(question: str) -> AnalyticalQueryResponse:
    """Start an analytical query. Analytical queries take time, so we will return a job ID and callback webhook.   
    Always call check_analytical_query_status to get the progress and result of the query straight after.
    Pass the output of this tool as-is to the check_analytical_query_status tool.

    Example:
    * What is my total spend?
    * How many total vendors are there?
    
    Args:
        question: The question to ask
    """
    time.sleep(1)
    job_id = str(uuid.uuid4())
    return AnalyticalQueryResponse(
        job_id=job_id, 
        callback_webhook="http://localhost:8910/mcp/check_analytical_query_status"
    )