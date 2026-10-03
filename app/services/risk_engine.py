from dataclasses import dataclass
from typing import List


@dataclass
class RuleFinding:
    category: str
    severity: str
    evidence: str
    explanation: str
    score: int


RISK_RULES = [
    {
        "pattern": "DROP TABLE",
        "category": "database",
        "severity": "critical",
        "score": 40,
        "explanation": "Destructive database operation detected."
    },
    {
        "pattern": "DROP COLUMN",
        "category": "database",
        "severity": "high",
        "score": 30,
        "explanation": "Database column removal detected."
    },
    {
        "pattern": "DELETE FROM",
        "category": "database",
        "severity": "high",
        "score": 25,
        "explanation": "Potential destructive data deletion detected."
    },
    {
        "pattern": ".env",
        "category": "security",
        "severity": "critical",
        "score": 40,
        "explanation": "Environment configuration or secret-related file modified."
    },
    {
        "pattern": "Dockerfile",
        "category": "docker",
        "severity": "medium",
        "score": 10,
        "explanation": "Docker configuration changed."
    },
    {
        "pattern": "deployment.yaml",
        "category": "kubernetes",
        "severity": "high",
        "score": 20,
        "explanation": "Kubernetes deployment configuration changed."
    },
    {
        "pattern": "deployment.yml",
        "category": "kubernetes",
        "severity": "high",
        "score": 20,
        "explanation": "Kubernetes deployment configuration changed."
    },
    {
        "pattern": "requirements.txt",
        "category": "dependencies",
        "severity": "medium",
        "score": 10,
        "explanation": "Python dependencies changed."
    },
    {
        "pattern": "authentication",
        "category": "security",
        "severity": "high",
        "score": 20,
        "explanation": "Authentication-related code changed."
    },
    {
        "pattern": "payment",
        "category": "business",
        "severity": "high",
        "score": 20,
        "explanation": "Payment-related code changed."
    }
]


def calculate_risk_level(score: int) -> str:
    if score >= 76:
        return "critical"

    if score >= 51:
        return "high"

    if score >= 21:
        return "medium"

    return "low"


def analyze_diff(diff: str) -> tuple[int, str, List[RuleFinding]]:
    findings: List[RuleFinding] = []
    total_score = 0

    diff_upper = diff.upper()

    for rule in RISK_RULES:
        pattern = rule["pattern"]

        if pattern.upper() in diff_upper:
            finding = RuleFinding(
                category=rule["category"],
                severity=rule["severity"],
                evidence=pattern,
                explanation=rule["explanation"],
                score=rule["score"]
            )

            findings.append(finding)
            total_score += rule["score"]

    total_score = min(total_score, 100)

    risk_level = calculate_risk_level(total_score)

    return total_score, risk_level, findings