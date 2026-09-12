import ollama
from harness.config import MODEL_NAME

SYSTEM_PROMPT = """You are a strict but fair content editor for a tech-focused marketing team.
Review the draft below and decide if it's ready to publish.

Respond in exactly this format:
VERDICT: GOOD or VERDICT: NEEDS_WORK
FEEDBACK: <one or two specific, actionable sentences on what to improve, or "None" if GOOD>"""

def critique_draft(draft: str) -> dict:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review this draft:\n\n{draft}"}
        ]
    )
    content = response["message"]["content"]

    verdict = "NEEDS_WORK"
    feedback = ""
    for line in content.splitlines():
        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
        elif line.startswith("FEEDBACK:"):
            feedback = line.replace("FEEDBACK:", "").strip()

    return {"verdict": verdict, "feedback": feedback}