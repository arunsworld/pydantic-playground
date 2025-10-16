from mcp.server.fastmcp import Context, FastMCP
from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
import uuid
import asyncio
load_dotenv()

import sys

# Default port
port = 8910

# Check if a port is provided as a command line argument
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port '{sys.argv[1]}', using default port {port}")

server = FastMCP(
    'Pydantic AI Server', 
    host='0.0.0.0', 
    port=port, debug=True, 
    stateless_http=True
    )

class AvailableSeats(BaseModel):
    venue: str
    seats: int

class Name(BaseModel):
    name: str = Field(description="What is your name?")

@server.tool()
async def available_seats(
        ctx: Context,
        venue: str = 'Wembley Stadium', # Optional name of venue
    ) -> AvailableSeats:
    """Respond to the user's request for available seats. If not venue is provided, default to Wembley Stadium.
    
    Args:
        venue: The venue to check for available seats (optional, default: Wembley Stadium)

    Returns:
        The number of available seats
    """
    
    print(f"metadata: {ctx.request_context.meta}. session: {ctx.session}")
    await asyncio.sleep(1)
    return AvailableSeats(venue=venue, seats=154)

class AnalyticalQueryResponse(BaseModel):
    job_id: str
    callback_webhook: str

@server.tool()
async def start_analytical_query(question: str) -> AnalyticalQueryResponse:
    """Start an analytical query. Analytical queries take time, so we will return a job ID and callback webhook.   
    Always call check_analytical_query_status to get the progress and result of the query straight after.
    Pass the output of this tool as-is to the check_analytical_query_status tool.

    Example:
    * What is my total spend?
    * How many total vendors are there?
    
    Args:
        question: The question to ask
    """
    await asyncio.sleep(1)
    job_id = str(uuid.uuid4())
    return AnalyticalQueryResponse(
        job_id=job_id, 
        callback_webhook="http://localhost:8910/mcp/check_analytical_query_status"
    )


# Always call check_analytical_query_status to get the progress and result of the query straight after.
# Pass the output of this tool as-is to the check_analytical_query_status tool.

if __name__ == '__main__':
    server.run(transport='streamable-http')