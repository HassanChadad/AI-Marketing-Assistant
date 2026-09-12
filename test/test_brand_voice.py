# test_brand_voice_agent.py

from agents.brand_voice_agent import review_brand_voice

draft = """Our revolutionary platform will absolutely transform how you work! 
This game-changing tool was leveraged by thousands of users."""

result = review_brand_voice(draft)
print(result)