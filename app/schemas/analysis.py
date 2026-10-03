from typing import List

from pydantic import BaseModel, Field

class DeploymentAnalysisRequest(BaseModel):
    repository: str
    branch: str
    commit_sha: str
    diff: str


class Finding(BaseModel):
    category: str
    severity: str
    file: str | None = None
    evidence: str | None = None
    explanation: str


class DeploymentAnalysisResponse(BaseModel):
    risk_score: int = Field(ge=0, le=100)
    risk_level: str
    summary: str
    findings: List[Finding]
    recommendations: List[str]