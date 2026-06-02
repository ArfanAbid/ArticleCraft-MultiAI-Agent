import os
import asyncio

os.environ["CREWAI_DISABLE_PROMPT_CACHE"] = "true"

# crewai/llm.py returns messages as-is for non-Anthropic providers without
# stripping the internal cache_breakpoint marker. Groq rejects that key.
# Patch the method to strip it before messages reach litellm.
from crewai.llm import LLM as _CrewAILLM

_orig_format = _CrewAILLM._format_messages_for_provider

def _patched_format(self, messages):
    cleaned = [
        {k: v for k, v in msg.items() if k != "cache_breakpoint"}
        for msg in messages
    ]
    return _orig_format(self, cleaned)

_CrewAILLM._format_messages_for_provider = _patched_format

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="ArticleCraft AI API",
    description="Multi-agent article generation powered by CrewAI",
    version="1.0.0",
)


class GenerateRequest(BaseModel):
    topic: str


class GenerateResponse(BaseModel):
    topic: str
    article: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_article(request: GenerateRequest):
    """
    Submit a topic and receive the fully generated article.
    Waits until all three agents finish (researcher → writer → proof reader).
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    from crew.article_crew import create_crew

    def run_crew():
        crew = create_crew()
        return crew.kickoff(inputs={"topic": request.topic})

    result = await asyncio.to_thread(run_crew)

    return GenerateResponse(topic=request.topic, article=str(result))
