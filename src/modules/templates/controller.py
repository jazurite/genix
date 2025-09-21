from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Predefined document templates
DOCUMENT_TEMPLATES = {
    "proposal": {
        "standard": {
            "name": "Standard Presale Proposal",
            "sections": ["executive_summary", "project_overview", "scope_of_work", "timeline", "budget", "team", "deliverables", "terms"],
            "description": "Standard business proposal template"
        },
        "technical": {
            "name": "Technical Proposal",
            "sections": ["technical_overview", "architecture", "implementation", "testing", "deployment", "maintenance"],
            "description": "Technical-focused proposal template"
        }
    },
    "technical_doc": {
        "api": {
            "name": "API Documentation",
            "sections": ["introduction", "authentication", "endpoints", "examples", "error_handling"],
            "description": "REST API documentation template"
        },
        "architecture": {
            "name": "System Architecture",
            "sections": ["overview", "components", "data_flow", "deployment", "security"],
            "description": "System architecture documentation template"
        }
    },
    "jira_ticket": {
        "story": {
            "name": "User Story",
            "fields": ["summary", "description", "acceptance_criteria", "story_points"],
            "description": "User story template for feature requests"
        },
        "task": {
            "name": "Technical Task",
            "fields": ["summary", "description", "implementation_notes", "definition_of_done"],
            "description": "Technical task template"
        }
    }
}

@router.get("/{doc_type}")
async def get_templates(doc_type: str) -> Dict[str, Any]:
    """
    Get available templates for a specific document type
    Supports: proposal, technical_doc, jira_ticket
    """
    try:
        if doc_type not in DOCUMENT_TEMPLATES:
            available_types = list(DOCUMENT_TEMPLATES.keys())
            raise HTTPException(
                status_code=404, 
                detail=f"Document type '{doc_type}' not found. Available types: {available_types}"
            )

        templates = DOCUMENT_TEMPLATES[doc_type]

        logger.info(f"Templates retrieved for document type: {doc_type}")

        return {
            "status": "success",
            "document_type": doc_type,
            "templates": templates,
            "count": len(templates),
            "message": f"Templates for {doc_type} retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error retrieving templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@router.get("/")
async def get_all_templates() -> Dict[str, Any]:
    """
    Get all available document templates
    """
    try:
        template_summary = {}
        total_templates = 0

        for doc_type, templates in DOCUMENT_TEMPLATES.items():
            template_summary[doc_type] = {
                "count": len(templates),
                "available": list(templates.keys())
            }
            total_templates += len(templates)

        logger.info("All templates retrieved")

        return {
            "status": "success",
            "total_templates": total_templates,
            "document_types": template_summary,
            "full_templates": DOCUMENT_TEMPLATES,
            "message": "All templates retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Error retrieving all templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")
