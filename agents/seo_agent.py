import ollama
import textstat
from harness.config import MODEL_NAME
from harness.config import SEO_THRESHOLDS

SYSTEM_PROMPT = """You are an SEO specialist. You will be given a draft, computed SEO
metrics, and a specific issue that has already been identified by rule-based analysis.
Your only job is to phrase that issue as one or two clear, actionable sentences for the writer.
Do not second-guess or recalculate the metrics — just explain the given issue clearly.

Respond in exactly this format:
FEEDBACK: <one or two sentences>"""

def compute_seo_metrics(draft: str, keyword: str) -> dict:
    word_count = len(draft.split())
    keyword_count = draft.lower().count(keyword.lower())
    density = (keyword_count / word_count) * 100 if word_count > 0 else 0
    readability = textstat.flesch_reading_ease(draft)

    return {
        "word_count": word_count,
        "keyword_count": keyword_count,
        "keyword_density": round(density, 2),
        "readability_score": round(readability, 1)
    }

def decide_seo_issues(metrics: dict, platform: str = "blog") -> dict:
    thresholds = SEO_THRESHOLDS.get(platform, SEO_THRESHOLDS["blog"])
    issues = []

    if metrics["keyword_density"] < thresholds["min_density"]:
        issues.append("keyword density is too low, needs more mentions of the keyword")
    elif metrics["keyword_density"] > thresholds["max_density"]:
        issues.append("keyword density is too high, needs fewer mentions of the keyword")

    if metrics["readability_score"] < thresholds["min_readability"]:
        issues.append("text is too complex, needs simpler sentences and words")

    if issues:
        return {"verdict": "NEEDS_WORK", "issues": issues}
    return {"verdict": "GOOD", "issues": []}

def review_seo(draft: str, keyword: str, platform: str = "blog") -> dict:
    metrics = compute_seo_metrics(draft, keyword)
    decision = decide_seo_issues(metrics, platform)

    if decision["verdict"] == "GOOD":
        return {"verdict": "GOOD", "feedback": "None", "metrics": metrics}

    metrics_summary = (
        f"Word count: {metrics['word_count']}\n"
        f"Keyword '{keyword}' appears {metrics['keyword_count']} times "
        f"(density: {metrics['keyword_density']}%)\n"
        f"Flesch reading ease score: {metrics['readability_score']}\n"
        f"Identified issues: {decision['issues']}"
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Draft:\n{draft}\n\nMetrics:\n{metrics_summary}"}
        ]
    )
    content = response["message"]["content"]

    feedback = ""
    for line in content.splitlines():
        if line.startswith("FEEDBACK:"):
            feedback = line.replace("FEEDBACK:", "").strip()

    return {"verdict": decision["verdict"], "feedback": feedback, "metrics": metrics}

def select_keyword(topic: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": (
                "You extract SEO keywords. Given a content topic, respond with ONLY "
                "the single most important 2-4 word SEO keyword phrase — no punctuation, "
                "no explanation, just the phrase itself."
            )},
            {"role": "user", "content": f"Topic: {topic}"}
        ]
    )
    return response["message"]["content"].strip()