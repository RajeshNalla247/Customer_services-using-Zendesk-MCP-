from mcp import tool
from pydantic import BaseModel
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")

class AddCommentInput(BaseModel):
    ticket_id: int
    comment: str
    public: bool = True  # default to public comment

@tool("add_comment_to_ticket")
def add_comment_to_ticket(data: AddCommentInput):
    """
    Add a comment to a Zendesk ticket.
    """
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets/{data.ticket_id}.json"
    auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

    payload = {
        "ticket": {
            "comment": {
                "body": data.comment,
                "public": data.public
            }
        }
    }

    try:
        response = requests.put(url, json=payload, auth=auth)
        response.raise_for_status()
        return {
            "success": True,
            "message": f"Comment added to ticket {data.ticket_id}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to add comment: {str(e)}"
        }
