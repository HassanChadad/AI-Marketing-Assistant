# test_seo_agent.py

from agents.seo_agent import review_seo

draft = """Local LLMs are transforming content creation.
By running language models locally, teams gain more control over their content pipeline."""

result = review_seo(draft, keyword="local LLMs")
print(result)