# test_visual_brief.py

from agents.visual_brief_agent import generate_visual_brief

brief = generate_visual_brief("local LLMs for content creation", platform="linkedin")
print(brief)