from mcp.server.fastmcp import Context, FastMCP
from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
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

server = FastMCP('Pydantic AI Server', host='0.0.0.0', port=port, debug=True, stateless_http=True)

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
    return AvailableSeats(venue=venue, seats=154)


if __name__ == '__main__':
    server.run(transport='streamable-http')