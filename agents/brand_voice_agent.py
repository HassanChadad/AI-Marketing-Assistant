import ollama
from harness.config import MODEL_NAME

BRAND_GUIDELINES = """
- Tone: professional but approachable — avoid stiff corporate jargon ("synergy", "leverage", "utilize")
- Voice: active voice preferred over passive ("we built this" not "this was built by us")
- Avoid excessive superlatives ("revolutionary", "game-changing", "best-in-class")
- Sentences should be direct — avoid unnecessary hedging ("might potentially perhaps")
- Never use exclamation points in body text
"""

SYSTEM_PROMPT = f"""You are a brand-voice reviewer. Check the draft against these guidelines:
{BRAND_GUIDELINES}

Respond in exactly this format:
VERDICT: GOOD or VERDICT: NEEDS_WORK
FEEDBACK: <one or two specific sentences citing which guideline was violated, or "None" if GOOD>"""

def review_brand_voice(draft: str) -> dict:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Draft:\n{draft}"}
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