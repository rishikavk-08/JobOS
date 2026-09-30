import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"


def analyze_job(job_description: str, evidence: str):

    prompt = f"""
You are JobOS, a career analysis system.

Analyze the following job description.

JOB DESCRIPTION:
{job_description}

CAREER EVIDENCE:
{evidence}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "fit_score": 0,
  "recommendation": "APPLY",
  "reasoning": "brief explanation",
  "requirements": [
    {{
      "requirement": "requirement from the job",
      "requirement_type": "STRATEGY",
      "importance": "REQUIRED",
      "matched": true,
      "match_score": 0,
      "evidence_ids": [],
      "reasoning": "brief explanation"
    }}
  ]
}}

Rules:

1. Extract the most important job requirements.
2. Use only evidence provided in CAREER EVIDENCE.
3. Do not invent experience.
4. Set matched to true only when the evidence supports the requirement.
5. match_score must be between 0 and 100.
6. importance must be REQUIRED or PREFERRED.
7. recommendation must be APPLY, REVIEW, or SKIP.
8. Keep reasoning brief.
9. Return JSON only.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "format": "json",
            "options": {
                "temperature": 0
            }
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    output = result.get("response", "").strip()

    if not output:
        raise ValueError(
            f"Ollama returned no response. "
            f"Thinking field: {result.get('thinking', '')}"
        )

    return json.loads(output)
