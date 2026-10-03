from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    DeploymentAnalysisRequest,
    DeploymentAnalysisResponse,
    Finding,
)
from app.services.llm_service import GeminiService
from app.services.risk_engine import analyze_diff

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
    score, level, rule_findings = analyze_diff(payload.diff)

    findings = [
        Finding(
            category=finding.category,
            severity=finding.severity,
            evidence=finding.evidence,
            explanation=finding.explanation
        )
        for finding in rule_findings
    ]

    recommendations = []

    if score >= 50:
        recommendations.append(
            "Perform additional validation before deployment."
        )

    if any(
        finding.category == "database"
        for finding in rule_findings
    ):
        recommendations.append(
            "Review database migration and rollback strategy."
        )

    if any(
        finding.category == "security"
        for finding in rule_findings
    ):
        recommendations.append(
            "Perform a security review before deployment."
        )

    if not recommendations:
        recommendations.append(
            "No major deterministic risk detected."
        )

    return DeploymentAnalysisResponse(
        risk_score=score,
        risk_level=level,
        summary=f"Deployment analyzed with risk level: {level}.",
        findings=findings,
        recommendations=recommendations
    )

@router.post("/api/v1/analyze/ai")
def analyze_deployment_with_ai(
    payload: DeploymentAnalysisRequest
):
    try:
        service = GeminiService()

        return service.analyze_deployment(
            repository=payload.repository,
            branch=payload.branch,
            diff=payload.diff,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"AI analysis unavailable: {exc}"
        )