from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class JiraTicketRequest(BaseModel):
    ticket_type: str  # "story", "task", "bug", "epic"
    summary: str
    description: Optional[str] = None
    priority: str = "medium"
    components: Optional[List[str]] = None
    transcript_context: Optional[str] = None
    codebase_context: Optional[str] = None

@router.post("/jira-ticket")
async def generate_jira_ticket(request: JiraTicketRequest) -> Dict[str, Any]:
    """
    Generate structured Jira tickets from requirements and context
    Uses uploaded transcripts and codebase analysis for detailed specifications
    """
    try:
        # TODO: Query Chroma for relevant context from transcripts/codebase
        # TODO: Use Gemini API to generate detailed ticket description
        # TODO: Apply Jira formatting and validation

        # Generate ticket structure
        ticket_structure = {
            "ticket_type": request.ticket_type.upper(),
            "summary": request.summary,
            "description": request.description or "Generated from uploaded context",
            "priority": request.priority.upper(),
            "components": request.components or [],
            "acceptance_criteria": [
                "Define acceptance criteria based on requirements",
                "Include testing requirements",
                "Specify completion conditions"
            ],
            "story_points": "To be estimated",
            "labels": [request.ticket_type, "generated", "hackathon"],
            "attachments": [],
            "subtasks": []
        }

        # Add context-specific details
        if request.ticket_type == "story":
            ticket_structure["user_story"] = f"As a user, I want {request.summary}"
        elif request.ticket_type == "task":
            ticket_structure["task_details"] = "Technical implementation details"
        elif request.ticket_type == "bug":
            ticket_structure["reproduction_steps"] = "Steps to reproduce the issue"
            ticket_structure["expected_behavior"] = "Expected system behavior"

        logger.info(f"Jira ticket generated: {request.ticket_type} - {request.summary}")

        return {
            "status": "success",
            "document_type": "jira_ticket",
            "ticket_type": request.ticket_type,
            "ticket": ticket_structure,
            "jira_formatted": True,
            "message": f"{request.ticket_type.title()} ticket generated successfully"
        }

    except Exception as e:
        logger.error(f"Error generating Jira ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
