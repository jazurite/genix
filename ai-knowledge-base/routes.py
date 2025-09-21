from fastapi import APIRouter
from src.modules.upload.transcript.controller import router as transcript_router
from src.modules.upload.codebase.controller import router as codebase_router
from src.modules.upload.wireframe.controller import router as wireframe_router
from src.modules.generate.proposal.controller import router as proposal_router
from src.modules.generate.technical_doc.controller import router as technical_doc_router
from src.modules.generate.jira_ticket.controller import router as jira_ticket_router
from src.modules.templates.controller import router as templates_router
from src.modules.validate.controller import router as validate_router

# Main router that combines all module routers
router = APIRouter()

# Upload routes
router.include_router(transcript_router, prefix="/upload", tags=["Upload"])
router.include_router(codebase_router, prefix="/upload", tags=["Upload"])
router.include_router(wireframe_router, prefix="/upload", tags=["Upload"])

# Generate routes
router.include_router(proposal_router, prefix="/generate", tags=["Generate"])
router.include_router(technical_doc_router, prefix="/generate", tags=["Generate"])
router.include_router(jira_ticket_router, prefix="/generate", tags=["Generate"])

# Template and validation routes
router.include_router(templates_router, prefix="/templates", tags=["Templates"])
router.include_router(validate_router, prefix="/validate", tags=["Validation"])
