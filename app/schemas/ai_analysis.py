from typing import List, Literal
from pydantic import BaseModel, Field


class AIFinding(BaseModel):
    category: str
    severity: Literal["low", "medium", "high", "critical"]
    file: str | None = None
    evidence: str | None = None
    explanation: str


class AIAnalysisResult(BaseModel):
    contextual_risk_score: int = Field(ge=0, le=100)

    summary: str

    findings: List[AIFinding]

    recommendations: List[str]