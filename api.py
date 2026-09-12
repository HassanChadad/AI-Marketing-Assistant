from fastapi import FastAPI
from pydantic import BaseModel
from core.api_handler import run_content_loop

app = FastAPI(title="AI Content Marketing Assistant")

class ContentRequest(BaseModel):
    topic: str
    platform: str = "blog"

@app.post("/marketing/content")
def generate_content(request: ContentRequest):
    print(f"Received request: topic='{request.topic}', platform='{request.platform}'")
    result = run_content_loop(topic=request.topic, platform=request.platform)
    return result