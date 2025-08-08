from mcp import tool
from pydantic import BaseModel
from typing import Optional
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")

class ListTicketsInput(BaseModel):
    limit: Optional[int] = 5  # default to 5

@tool("list_recent_tickets")
def list_recent_tickets(data: ListTicketsInput):
    """
    Fetch recent Zendesk tickets, limited by the number specified.
    """
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json?page[size]={data.limit}"
    auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()

        all_tickets = response.json().get("tickets", [])[:data.limit]
        result = [
            {
                "id": t["id"],
                "subject": t["subject"],
                "status": t["status"],
                "created_at": t["created_at"]
            }
            for t in all_tickets
        ]
        return {"tickets": result}

    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to list tickets"}
