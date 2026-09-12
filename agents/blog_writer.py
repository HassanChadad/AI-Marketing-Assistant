import ollama
from harness.config import MODEL_NAME

BASE_SYSTEM_PROMPT = """You are a skilled writer for a tech-focused content marketing team.
Keep the tone informative but conversational."""

PLATFORM_INSTRUCTIONS = {
    "blog": (
        "Write a full blog post (400-600 words). Use short paragraphs and clear subheadings. "
        "Aim for depth and detail suitable for someone researching the topic."
    ),
    "linkedin": (
        "Write a LinkedIn post (under 200 words). Start with a strong hook in the first line. "
        "Use short, punchy sentences — often one sentence per line for mobile readability. "
        "No subheadings. End with 2-3 relevant hashtags."
    ),
    "instagram": (
        "Write an Instagram caption (under 150 words). Start with an attention-grabbing first line "
        "since Instagram truncates captions after ~2 lines. Use a casual, friendly tone with emojis "
        "where natural. End with 5-8 relevant hashtags on a new line."
    ),
}

def write_blog_draft(topic: str, platform: str = "blog", keyword: str = None,
                      feedback: str = None, examples: list[str] = None) -> str:
    platform_instruction = PLATFORM_INSTRUCTIONS.get(platform, PLATFORM_INSTRUCTIONS["blog"])
    system_prompt = f"{BASE_SYSTEM_PROMPT}\n\n{platform_instruction}"

    instructions = [f"Write content about: {topic}"]

    if examples:
        examples_text = "\n\n---\n\n".join(examples)
        instructions.append(
            f"Here are past posts we've written on similar topics for this platform, "
            f"for style/structure reference (don't copy content, just match the voice):\n\n{examples_text}"
        )

    if keyword:
        instructions.append(f"Naturally include the phrase \"{keyword}\" a few times throughout — don't force it, but make sure it appears.")

    if feedback:
        instructions.append(f"This is a revision. Address this feedback from the editor: {feedback}")

    user_message = "\n\n".join(instructions)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response["message"]["content"]