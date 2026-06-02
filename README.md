# ArticleCraft AI

**ArticleCraft AI** is a **multi-agent article generation API** built with [CrewAI](https://github.com/crewAI-Inc/crewAI) and **GPT-4o**.

A team of three specialized AI agents — Researcher, Writer, and Proof Reader — work sequentially to produce a fully researched, written, and proofread article from a single topic.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| Agents | CrewAI 1.x |
| LLM | OpenAI GPT-4o |
| Search | SerperDev (Google Search) |
| Server | Uvicorn |

---

## Project Structure

```
ArticleCraft CrewAI/
├── .env                   # API keys (not committed)
├── requirements.txt
└── Backend/
    ├── app/
    │   └── main.py        # FastAPI endpoints
    └── crew/
        ├── agents.py      # Researcher, Writer, Proof Reader agents
        ├── tasks.py       # Task definitions
        ├── tools.py       # Google search tool
        └── article_crew.py  # Crew orchestration
```

---

## Agents

| Agent | Role |
|-------|------|
| **Researcher** | Tracks emerging trends, validates findings via Google search |
| **Writer** | Transforms research into an engaging, structured article |
| **Proof Reader** | Polishes the article, adds citations and reference sources |

Agents run **sequentially** — each step builds on the previous one.

---

## Setup

**1. Clone and install dependencies**
```bash
git clone https://github.com/ArfanAbid/ArticleCraft-MultiAI-Agent.git
cd ArticleCraft-MultiAI-Agent
pip install -r requirements.txt
```

**2. Configure environment variables**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

Get your keys:
- OpenAI API key: https://platform.openai.com/api-keys
- Serper API key: https://serper.dev

**3. Start the server**
```bash
cd Backend
uvicorn app.main:app --reload
```

---

## API Endpoints

### `POST /generate`
Submit a topic and receive the fully generated article.

**Request**
```json
{
  "topic": "AI in Healthcare"
}
```

**Response**
```json
{
  "topic": "AI in Healthcare",
  "article": "## AI in Healthcare\n\n..."
}
```

> Note: This is a blocking call. The three agents run sequentially and typically take **1–3 minutes** to complete.

---

### `GET /health`
Check that the server is running.

```json
{ "status": "ok" }
```

---

## Interactive Docs

Once the server is running, open:
```
http://localhost:8000/docs
```

Swagger UI lets you call both endpoints directly from the browser.

---

*ArfanAbid*
