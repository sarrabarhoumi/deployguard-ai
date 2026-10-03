import os
import time

from google import genai

from app.schemas.ai_analysis import AIAnalysisResult


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

    def analyze_deployment(
        self,
        repository: str,
        branch: str,
        diff: str,
    ) -> AIAnalysisResult:

        prompt = self._build_prompt(
            repository=repository,
            branch=branch,
            diff=diff,
        )

        max_retries = 3

        for attempt in range(max_retries):

            try:
                interaction = self.client.interactions.create(
                    model=self.model,
                    input=prompt,
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": AIAnalysisResult.model_json_schema(),
                    },
                )

                return AIAnalysisResult.model_validate_json(
                    interaction.output_text
                )

            except Exception as exc:

                if attempt == max_retries - 1:
                    raise exc

                wait_time = 2 ** attempt

                time.sleep(wait_time)

    @staticmethod
    def _build_prompt(
        repository: str,
        branch: str,
        diff: str,
    ) -> str:

        return f"""
You are DeployGuard AI, a senior DevOps deployment risk analyst.

Analyze this deployment.

Repository:
{repository}

Branch:
{branch}

Git Diff:
{diff}

Analyze:

- database migrations
- API breaking changes
- authentication changes
- payment logic
- Docker changes
- Kubernetes configuration
- dependency changes
- security risks
- deployment failures

Rules:

1. Do not invent information.
2. Use evidence from the diff.
3. Give a risk score between 0 and 100.
4. Recommendations must be actionable.
"""