import ollama
from harness.config import MODEL_NAME
from agents.editor import critique_draft
from agents.seo_agent import review_seo
from agents.brand_voice_agent import review_brand_voice

TOTAL_MODELS = 3  # editor, seo, brand_voice

SYSTEM_PROMPT = """You are the lead editor overseeing content review. You've received feedback
from three specialist reviewers: a general Editor, an SEO specialist, and a Brand-Voice specialist.
Some feedback may overlap or conflict. Synthesize it into ONE clear, prioritized set of
instructions for the writer. If specialists conflict, use your judgment on what matters most
for a professional tech blog post, and briefly note the tradeoff.

Do not explain what you are doing or reference the synthesis process itself — output only the
actual instructions for the writer, as if you were giving direct editorial notes.

Respond in exactly this format:
FEEDBACK: <the instructions themselves, nothing else>"""

GOOD_THRESHOLD = 100 / TOTAL_MODELS  # 2 out of 3 specialists GOOD = 66%, still counts as "needs a bit more work" not GOOD
# Only 100% (all 3 GOOD) actually stops the loop — your call on whether 66% should also pass

def orchestrate_review(draft: str, keyword: str, platform: str = "blog") -> dict:
    editor_result = critique_draft(draft)      # still returns {verdict, feedback} — unchanged
    seo_result = review_seo(draft, keyword=keyword, platform=platform)
    brand_result = review_brand_voice(draft)

    all_results = {"editor": editor_result, "seo": seo_result, "brand_voice": brand_result}
    good_count = sum(1 for r in all_results.values() if r["verdict"] == "GOOD")
    score_pct = round((good_count / TOTAL_MODELS) * 100)

    if good_count == TOTAL_MODELS:
        return {"score": 100, "verdict": "GOOD", "feedback": "None", "specialist_results": all_results}

    specialist_summary = "\n".join(
        f"{name.upper()} — {r['verdict']}: {r['feedback']}" for name, r in all_results.items()
    )
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Draft:\n{draft}\n\nSpecialist feedback:{specialist_summary}"}
        ]
    )
    feedback = extract_feedback(response["message"]["content"])

    return {"score": score_pct, "verdict": "NEEDS_WORK", "feedback": feedback, "specialist_results": all_results}

def extract_feedback(content: str) -> str:
    if "FEEDBACK:" in content: # if feedback is present in the string, extract it
        return content.split("FEEDBACK:", 1)[1].strip()
    return content.strip()  # fallback: if the model didn't follow the format, just use everything