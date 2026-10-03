from app.services.risk_engine import (
    analyze_diff,
    calculate_risk_level,
)


def test_low_risk():
    score, level, findings = analyze_diff(
        "Updated README documentation"
    )

    assert score == 0
    assert level == "low"
    assert findings == []


def test_database_risk():
    score, level, findings = analyze_diff(
        "ALTER TABLE users DROP COLUMN phone;"
    )

    assert score == 30
    assert level == "medium"
    assert len(findings) == 1


def test_critical_risk():
    diff = """
    DROP TABLE payments;
    Dockerfile
    deployment.yaml
    payment service
    """

    score, level, findings = analyze_diff(diff)

    assert score >= 76
    assert level == "critical"
    assert len(findings) >= 3


def test_score_never_exceeds_100():
    diff = """
    DROP TABLE users;
    DROP COLUMN email;
    DELETE FROM users;
    .env
    Dockerfile
    deployment.yaml
    requirements.txt
    authentication
    payment
    """

    score, level, findings = analyze_diff(diff)

    assert score == 100
    assert level == "critical"