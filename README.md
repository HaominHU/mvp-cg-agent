# 🧠 Caregiver Agent Prototype
**Part of my AI-Assisted Learning Journey** | [View Full Series](#-about-this-learning-journey)

> A minimal, production-style agent system for dementia caregiver support.  
> Built to understand real-world agent architecture beyond single LLM calls.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](/LICENSE)

---

## 🎯 Learning Focus

- Agent Architecture (state + tools + orchestration)
- FastAPI backend for AI systems
- LLM integration (OpenAI)
- Prompt engineering (tool-level prompts)
- Config-driven model switching

---

## 🤖 Tech Stack

- **Backend:** FastAPI
- **Language:** Python 3.12
- **LLM:** OpenAI (configurable)
- **Data Layer:** Local JSON (proto knowledge base)
- **Environment:** Conda + macOS

---

## 🏗️ System Architecture

```

POST /agent/run
↓
FastAPI (main.py)
↓
Agent Orchestrator (agent.py)
├── assess_case (LLM → parse → normalize → AssessmentResult)
├── retrieve_knowledge (local JSON)
├── retrieve_resources (local JSON)
└── generate_response (LLM)
↓
Structured JSON Response

```

---

## 🧩 Core Concepts Demonstrated

### 1. Stateful Agent Design
- `AgentState` as internal working memory
- Multi-step flow instead of single LLM call

### 2. Tool-based Architecture
- Each step = one tool
- Clear separation of responsibilities

### 3. Orchestration Layer
- `agent.py` controls flow
- Supports branching (e.g., escalation)

### 4. Config-driven LLM
- `.env` + enum-based model/provider switching
- Decoupled from business logic

### 5. Prompt as Behavior
- Prompts extracted into `prompts.py`
- Treated as configurable instruction layer

### 6. Structured Assessment Contract
- `AssessmentResult` as the internal typed result for assessment
- Parsing and normalization layer between LLM output and agent state
- Public `Assessment` kept separate from internal assessment result

---

## 📁 Project Structure

```

app/
├── main.py        # API entrypoint
├── agent.py       # Orchestrator (workflow)
├── tools.py       # Tool implementations
├── llm.py         # LLM abstraction layer
├── prompts.py     # Prompt templates
├── models.py      # Data models (Pydantic)
├── config.py      # Settings & environment
└── logger.py      # Logging

data/
├── knowledge_base.json
└── resources.json

.env

````

---

## 🚀 How to Run

```bash
uvicorn app.main:app --reload
````

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Request

```json
{
  "user_input": "My mother keeps walking around at night and I feel exhausted."
}
```

---

## 📤 Example Response

```json
{
  "assessment": {
    "problem_tags": ["sleep disturbance", "wandering"],
    "risk_level": "medium",
    "caregiver_emotion": "overwhelmed"
  },
  "recommendations": [],
  "resources": [],
  "final_message": "..."
}
```

---

## ✅ What’s Completed
### Minimal viable agent prototype with core architecture and flow implemented:
* [x] FastAPI backend setup
* [x] LLM integration (OpenAI)
* [x] AgentState design
* [x] Tool-based architecture
* [x] Orchestrator (multi-step workflow)
* [x] Local knowledge & resource retrieval
* [x] Prompt extraction (`prompts.py`)
* [x] Config-driven model switching (`.env` + enum)
* [x] Basic logging system
### Assessment parsing and normalization layer with a dedicated internal assessment result model:
* [x] Dedicated internal assessment result model (`AssessmentResult`)
* [x] Assessment parsing + normalization layer
* [x] Separation between internal assessment result and public assessment response

---

## 🚧 What Can Be Improved

### Agent Logic

* [ ] Add retry / repair strategy for malformed LLM assessment output
* [ ] Add unit tests for assessment parsing and normalization
* [ ] Add `search_queries` into retrieval pipeline

### Knowledge Layer

* [ ] Replace tag matching with keyword search
* [ ] Upgrade to vector database (FAISS / Chroma)
* [ ] Implement full RAG pipeline

### System Design

* [ ] Move to graph-based orchestration (LangGraph)
* [ ] Add unit tests / evaluation cases
* [ ] Introduce structured logging

### Productization

* [ ] Add frontend (simple UI)
* [ ] Add authentication (optional)
* [ ] Deploy (Docker / cloud)

---

## 🧠 Key Learnings
*Minimal viable agent prototype*
* An **agent is not a single LLM call**
* State is essential for multi-step reasoning
* Tools should be **small and composable**
* Orchestrator defines intelligence, not the model alone
* Prompt = behavior configuration, not just text

*Assessment parsing and normalization layer*
* LLM output should pass through parsing, normalization, and typed contracts before entering business logic

---

## 📚 About This Learning Journey

<details>
<summary><b>🤖 How I Used AI to Learn AI Engineering</b></summary>

### My Approach

This project represents my **AI-assisted learning methodology**:

1. **ChatGPT for Brainstorming** - Initial ideation and project scoping
2. **Gemini (Google AI Studio) for UI** - Quick setup for a modern website design
3. **Hands-on Building** - Claude Code + GitHub Copilot for actual coding and debugging
4. **Research job only** - Gemini for Deep Research with SoTA knowledge, and Claude for tutorials, documentation & writing

**For Claude Code:**
```
1. /init: Set up CLAUDE.md
2. Every time, ask fora  plan & wait for coding, ask to confirm, generate TODO, and code step by step, with explanations and comments
3. Use/compact to summarize the previous discussion after a backlog completion
```

### More in This Series

1. **[Private] Real-world local shop website quick setup - Prompt Engineering** ✅
2. **Brainstormed Claude Skills Archive - Prompt Engineering + Claude Skills Creation** ✅
3. **[This Project] Caregiver Agent Prototype** - Agent Architecture & Orchestration ✅

</details>

---

## 📄 License & Acknowledgments

**License:** MIT

**AI Tools Used:**
- ChatGPT - Step-by-step tutor
    - prompt -> tutorial -> checklist review -> prompt -> next step
- GitHub Copilot - Coding assistance and debugging


---

*Part of the AI-Assisted Learning Journey | Last updated: 2026*

---
