from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ProposalRequest(BaseModel):
    client_name: str
    project_description: str
    requirements: List[str]
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    template_type: str = "standard"

@router.post("/proposal")
async def generate_proposal(request: ProposalRequest) -> Dict[str, Any]:
    """
    Generate presale proposals from requirements and client information
    Uses uploaded transcripts, codebase analysis, and wireframes as context
    """
    try:
        # TODO: Query Chroma for relevant context
        # TODO: Use Gemini API to generate structured proposal
        # TODO: Apply validation layers

        # Mock response structure for now
        proposal_structure = {
            "executive_summary": f"Proposal for {request.client_name}",
            "project_overview": request.project_description,
            "scope_of_work": request.requirements,
            "timeline": request.timeline or "To be determined",
            "budget_estimate": request.budget_range or "To be determined",
            "technical_approach": "Based on uploaded codebase and wireframes",
            "team_composition": "Recommended team structure",
            "deliverables": "Project deliverables and milestones",
            "terms_and_conditions": "Standard terms and conditions"
        }

        logger.info(f"Proposal generated for client: {request.client_name}")

        return {
            "status": "success",
            "document_type": "presale_proposal",
            "client_name": request.client_name,
            "template_used": request.template_type,
            "proposal": proposal_structure,
            "message": "Presale proposal generated successfully"
        }

    except Exception as e:
        logger.error(f"Error generating proposal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
