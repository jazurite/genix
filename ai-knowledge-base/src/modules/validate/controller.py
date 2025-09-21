from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ValidationRequest(BaseModel):
    document_type: str
    content: Dict[str, Any]
    validation_rules: Optional[List[str]] = None

class ValidationResult(BaseModel):
    is_valid: bool
    score: float
    issues: List[Dict[str, str]]
    suggestions: List[str]

@router.post("/{doc_id}")
async def validate_document(doc_id: str, request: ValidationRequest) -> Dict[str, Any]:
    """
    Validate generated documents against quality criteria
    Checks: completeness, structure, content quality, formatting
    """
    try:
        validation_results = ValidationResult(
            is_valid=True,
            score=0.0,
            issues=[],
            suggestions=[]
        )

        # Document type specific validation
        if request.document_type == "proposal":
            validation_results = await _validate_proposal(request.content)
        elif request.document_type == "technical_doc":
            validation_results = await _validate_technical_doc(request.content)
        elif request.document_type == "jira_ticket":
            validation_results = await _validate_jira_ticket(request.content)
        else:
            validation_results = await _validate_generic(request.content)

        logger.info(f"Document validated: {doc_id} - Score: {validation_results.score}")

        return {
            "status": "success",
            "document_id": doc_id,
            "document_type": request.document_type,
            "validation": {
                "is_valid": validation_results.is_valid,
                "score": validation_results.score,
                "issues": validation_results.issues,
                "suggestions": validation_results.suggestions
            },
            "message": "Document validation completed"
        }

    except Exception as e:
        logger.error(f"Error validating document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

async def _validate_proposal(content: Dict[str, Any]) -> ValidationResult:
    """Validate proposal document structure and content"""
    issues = []
    suggestions = []
    score = 100.0

    required_sections = ["executive_summary", "project_overview", "scope_of_work", "timeline", "budget_estimate"]

    for section in required_sections:
        if section not in content or not content[section]:
            issues.append({
                "type": "missing_section",
                "severity": "high",
                "message": f"Required section '{section}' is missing or empty"
            })
            score -= 20.0

    if not issues:
        suggestions.append("Consider adding client testimonials or case studies")
        suggestions.append("Include detailed project milestones")

    return ValidationResult(
        is_valid=len(issues) == 0,
        score=max(0.0, score),
        issues=issues,
        suggestions=suggestions
    )

async def _validate_technical_doc(content: Dict[str, Any]) -> ValidationResult:
    """Validate technical documentation structure and content"""
    issues = []
    suggestions = []
    score = 100.0

    # TODO: Implement specific technical documentation validation
    # Check for code examples, proper formatting, completeness

    suggestions.append("Consider adding code examples")
    suggestions.append("Include diagrams or flowcharts")

    return ValidationResult(
        is_valid=True,
        score=score,
        issues=issues,
        suggestions=suggestions
    )

async def _validate_jira_ticket(content: Dict[str, Any]) -> ValidationResult:
    """Validate Jira ticket structure and content"""
    issues = []
    suggestions = []
    score = 100.0

    required_fields = ["summary", "description", "priority"]

    for field in required_fields:
        if field not in content or not content[field]:
            issues.append({
                "type": "missing_field",
                "severity": "medium",
                "message": f"Required field '{field}' is missing"
            })
            score -= 15.0

    if content.get("ticket_type") == "story" and "acceptance_criteria" not in content:
        suggestions.append("User stories should include acceptance criteria")

    return ValidationResult(
        is_valid=len([i for i in issues if i["severity"] == "high"]) == 0,
        score=max(0.0, score),
        issues=issues,
        suggestions=suggestions
    )

async def _validate_generic(content: Dict[str, Any]) -> ValidationResult:
    """Generic validation for any document type"""
    issues = []
    suggestions = []
    score = 85.0  # Default score for generic validation

    if not content:
        issues.append({
            "type": "empty_content",
            "severity": "high",
            "message": "Document content is empty"
        })
        score = 0.0

    suggestions.append("Consider using specific document type validation")

    return ValidationResult(
        is_valid=len(issues) == 0,
        score=score,
        issues=issues,
        suggestions=suggestions
    )
