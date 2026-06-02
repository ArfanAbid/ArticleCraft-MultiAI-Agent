# ArticleCraft AI

**ArticleCraft AI** is a production-ready **multi-agent content generation application** built with [CrewAI](https://github.com/joaomdmoura/crewai), **Groq LLaMA 3.3 70B**, and a **Streamlit** web interface.

Given a single topic, it orchestrates three specialized AI agents — Researcher, Writer, and Proof Reader — to produce a well-researched, polished, citation-backed markdown article through a sequential pipeline.

---

## Table of Contents

- [Demo](#demo)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Agent Roles](#agent-roles)
- [Task Pipeline](#task-pipeline)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Output Format](#output-format)
- [Rate Limiting](#rate-limiting)

---

## Demo

1. Enter a topic (e.g., *"AI in Healthcare"*, *"Quantum Computing"*, *"Space Technology"*)
2. Click **Generate Article**
3. The three agents run sequentially — research → write → proofread
4. A formatted markdown article with inline citations and 3 reference sources is displayed
5. Download the article as a `.md` file

---

## Architecture

```
User Input (Topic)
        │
        ▼
┌───────────────────┐
│   Streamlit UI    │  ← Rate-limited, session-state managed
└────────┬──────────┘
         │
         ▼
┌───────────────────────────────────────────────────────────────┐
│                        CrewAI Crew                            │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐ │
│  │  Researcher │──▶│   Writer    │──▶│    Proof Reader     │ │
│  │  (Task 1)   │   │  (Task 2)   │   │      (Task 3)       │ │
│  └─────────────┘   └─────────────┘   └─────────────────────┘ │
│         │                 │                     │             │
│    SerperDevTool     SerperDevTool         SerperDevTool      │
│    (web search)      (web search)          (web search)       │
└───────────────────────────────────────────────────────────────┘
         │
         ▼
   Final Markdown Article
   (4 paragraphs + citations + 3 sources)
```

All three agents use the **Groq LLaMA 3.3 70B Versatile** model with `temperature=0` for deterministic, consistent output.

---

## Tech Stack

| Component | Library / Service |
|---|---|
| Multi-agent orchestration | `crewai==0.157.0` |
| LLM | Groq — `llama-3.3-70b-versatile` |
| LLM wrapper | `langchain-groq` (`ChatGroq`) |
| Web search | Serper API (`crewai_tools.SerperDevTool`) |
| Web UI | `streamlit` |
| Environment config | `python-dotenv` |

---

## Agent Roles

### 1. Researcher — Technology Intelligence Specialist

- **Goal:** Track emerging breakthroughs, identify patterns, predict inflection points, and assess real-world impact
- **Backstory:** Former quantum computing researcher with expertise across 47 countries monitoring 140+ information streams
- **Tools:** SerperDevTool (web search)
- **Memory:** Enabled
- **Delegation:** Allowed

### 2. Writer — Technology Storyteller & Innovation Chronicler

- **Goal:** Transform complex research into compelling, engaging narratives accessible at multiple technical levels
- **Backstory:** Former quantum physicist, 15 years of science communication, published in Nature, WIRED, and MIT Technology Review
- **Technique:** *Progressive Depth* — content works at three layers: surface (casual reader), middle (informed professional), deep (technical expert)
- **Tools:** SerperDevTool
- **Memory:** Enabled
- **Delegation:** Allowed

### 3. Proof Reader — Principal Proofreader

- **Goal:** Ensure the article is polished, factually accurate, and ready for stakeholder delivery
- **Responsibilities:** Grammar and clarity, inline citations, verification of sources, readability check
- **Output requirement:** Must include 3 reference sources
- **Tools:** SerperDevTool
- **Memory:** Enabled
- **Delegation:** Allowed

---

## Task Pipeline

The crew runs in **sequential process** — each task receives the output of the previous one.

```
Task 1: Research
├── Agent:  Researcher
├── Input:  User-provided topic
└── Output: 3-paragraph report — key trends, pros/cons, market opportunities, risks

Task 2: Write
├── Agent:  Writer
├── Input:  Research output + topic
└── Output: 4-paragraph markdown article — engaging, latest trends, industry impact

Task 3: Proof Read
├── Agent:  Proof Reader
├── Input:  Written article + topic
└── Output: 4-paragraph polished markdown article + inline citations + 3 reference sources
```

---

## Project Structure

```
ArticleCraft CrewAI/
├── NewsAgents/
│   ├── agents.py       # Agent definitions (Researcher, Writer, Proof Reader)
│   ├── tasks.py        # Task definitions bound to each agent
│   ├── crew.py         # Crew assembly, Streamlit UI, rate limiting logic
│   └── tools.py        # Tool and LLM initialization (Groq + SerperDevTool)
├── .env                # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com/) (free tier available)
- A [Serper API key](https://serper.dev/) (free tier: 2,500 searches/month)

### Install

```bash
git clone https://github.com/your-username/ArticleCraft-CrewAI.git
cd "ArticleCraft CrewAI"

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

These are loaded automatically via `python-dotenv` before the agents are initialized.

---

## Running the App

```bash
streamlit run NewsAgents/crew.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

**Streamlit UI features:**

- Topic input field
- Generate Article button (auto-disabled during rate-limit cooldown)
- Real-time MM:SS countdown when rate-limited
- Agent information sidebar
- Markdown-rendered article output
- Download button for the generated `.md` file
- Error recovery — rate limit resets on failure so you can retry immediately

---

## Output Format

Each generated article follows this structure:

```markdown
## [Article Title]

[Paragraph 1 — Introduction and context]

[Paragraph 2 — Current state, key trends, data points]

[Paragraph 3 — Industry impact and market opportunities]

[Paragraph 4 — Future outlook and risks]

### References
1. [Source 1 title](url)
2. [Source 2 title](url)
3. [Source 3 title](url)
```

---

## Rate Limiting

A **60-second cooldown** is enforced between generation requests to manage API usage and prevent cost spikes.

- The Generate button disables and shows a live countdown after each request
- The timer resets immediately if an error occurs, so you can retry without waiting
- Session state persists the last-run timestamp across Streamlit reruns

---

*Built by [Arfan Abid](https://github.com/ArfanAbid)*
