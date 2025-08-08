from mcp import tool
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")

class TicketStatusInput(BaseModel):
    ticket_id: int

@tool("get_ticket_status")
def get_ticket_status(data: TicketStatusInput):
    """
    Get status, priority, and assignee of a Zendesk ticket by ID.
    """
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets/{data.ticket_id}.json"
    auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        ticket = response.json()["ticket"]

        return {
            "status": ticket["status"],
            "priority": ticket.get("priority"),
            "assignee_id": ticket.get("assignee_id"),
            "message": "Ticket fetched successfully"
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to get ticket status"}
