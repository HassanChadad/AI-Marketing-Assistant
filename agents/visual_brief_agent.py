# agents/visual_brief_agent.py

import ollama
from harness.config import MODEL_NAME

SYSTEM_PROMPT = """You are a creative director who writes visual briefs for designers.
Given a blog post topic and target platform, write a concise, actionable visual brief
for an accompanying image. Be specific about composition, style, and color — not vague.

Respond in exactly this format:
CONCEPT: <what the image depicts, one sentence>
STYLE: <art style, e.g. minimalist flat illustration, photo-realistic, etc.>
COLORS: <2-3 colors or a palette description>
COMPOSITION: <layout/framing notes, one sentence>"""

def generate_visual_brief(topic: str, platform: str = "blog") -> dict:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Topic: {topic}\nPlatform: {platform}"}
        ]
    )
    content = response["message"]["content"]

    brief = {}
    for line in content.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            brief[key.strip().lower()] = value.strip()

    return brief