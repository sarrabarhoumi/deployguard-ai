from fastapi import APIRouter
from app.schemas.analysis import (
    DeploymentAnalysisRequest,
    DeploymentAnalysisResponse,
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DeployGuard AI"
    }


@router.post(
    "/api/v1/analyze",
    response_model=DeploymentAnalysisResponse
)
def analyze_deployment(
    payload: DeploymentAnalysisRequest
):
    return DeploymentAnalysisResponse(
        risk_score=10,
        risk_level="low",
        summary="Initial deployment analysis completed.",
        findings=[],
        recommendations=[
            "No critical issue detected in this initial version."
        ]
    )