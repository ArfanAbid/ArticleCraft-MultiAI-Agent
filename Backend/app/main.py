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
def generate_article(request: GenerateRequest):
    """
    Submit a topic and receive the fully generated article.
    This is a blocking call — it waits until all three agents finish.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    from crew.article_crew import create_crew
    crew = create_crew()
    result = crew.kickoff(inputs={"topic": request.topic})

    return GenerateResponse(topic=request.topic, article=str(result))
