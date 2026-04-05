from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from app.llm import call_llm
from app.models import (
    AgentRunRequest,
    AgentRunResponse,
    Assessment,
    LLMTestRequest,
    LLMTestResponse,
)

from app.agent import run_agent as run_agent_workflow

app = FastAPI(title="MVP Caregiver Agent")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "CG agent backend is running."
    }

@app.post("/test-llm", response_model=LLMTestResponse)
def test_llm(request: LLMTestRequest):
    try:
        output_text = call_llm(
            prompt=request.prompt,
            provider=request.provider,
            model=request.model,
        )

        return LLMTestResponse(
            provider=request.provider,
            model=request.model,
            output_text=output_text,
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/run", response_model=AgentRunResponse)
def run_agent(request: AgentRunRequest):
    state = run_agent_workflow(request.user_input)
    return AgentRunResponse(
        assessment=state.assessment or Assessment(
            problem_tags=["unknown"],
            risk_level="medium",
            caregiver_emotion="unknown"
        ),
        recommendations=state.knowledge or [],
        resources=state.resources or [],
        final_message=state.response or ""
    )
