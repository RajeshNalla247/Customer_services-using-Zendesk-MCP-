# from fastapi import FastAPI
# from mcp.server import FastMCP
# from create_ticket import create_ticket, list_recent_tickets

# app = FastAPI()
# mcp = FastMCP(app)

# @mcp.tool()
# def create_ticket_tool(subject: str, description: str, email: str):
#     return create_ticket(subject, description, email)

# @mcp.tool()
# def list_recent_tickets_tool(limit: int = 10):
#     return list_recent_tickets(limit)
from fastapi import FastAPI
from mcp import MCPServer
from tools import create_ticket, get_ticket_status , list_recent_tickets , add_comment_to_ticket

app = FastAPI()
mcp_server = MCPServer(app)

mcp_server.include_tool(create_ticket.create_ticket)
mcp_server.include_tool(get_ticket_status.get_ticket_status)
mcp_server.include_tool(list_recent_tickets.list_recent_tickets)
mcp_server.include_tool(add_comment_to_ticket.add_comment_to_ticket)
