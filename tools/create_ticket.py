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

class CreateTicketInput(BaseModel):
    subject: str
    description: str
    email: str

@tool("create_ticket")
def create_ticket(data: CreateTicketInput):
    """
    Creates a new support ticket in Zendesk.
    """
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json"
    headers = {"Content-Type": "application/json"}
    payload = {
    "ticket": {
        "subject": data.subject,
        "comment": {
            "body": data.description
        }
    }
}

    auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

    try:
        response = requests.post(url, headers=headers, auth=auth, json=payload)
        response.raise_for_status()
        result = response.json()
        return {
            "ticket_id": result["ticket"]["id"],
            "status": result["ticket"]["status"],
            "message": "Ticket created successfully"
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to create ticket"}
