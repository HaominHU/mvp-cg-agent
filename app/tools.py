import json
from mmap import ACCESS_COPY
from pathlib import Path
from token import OP

from app.config import settings
from app.llm import call_llm
from app.models import AgentState, Assessment, Resource

from app.prompts import ASSESS_CASE_PROMPT, GENERATE_RESPONSE_PROMPT

from app.logger import get_logger

logger = get_logger(__name__)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_data(file_name: str):
    file_path = DATA_DIR / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def assess_case(state: AgentState) -> AgentState:
    prompt = ASSESS_CASE_PROMPT.format(user_input=state.user_input)

    raw_output = call_llm(
        prompt=prompt,
        provider=settings.DEFAULT_LLM_PROVIDER,
        model=settings.DEFAULT_OPENAI_MODEL
    )

    try:
        data = json.loads(raw_output)

        state.assessment = Assessment(
            problem_tags=data.get("problem_tags", []),
            risk_level=data.get("risk_level", "medium"),
            caregiver_emotion=data.get("caregiver_emotion", "unknown")
        )

        state.needs_escalation = data.get("needs_escalation", False)

    except Exception as e:
        logger.error("ASSESS PARSE ERROR: %s", e)
        logger.error("RAW OUTPUT: %s", raw_output)

        state.assessment = Assessment(
            problem_tags=["unknown"],
            risk_level="medium",
            caregiver_emotion="unknown"
        )
        state.needs_escalation = False

    return state


def retrieve_knowledge(state: AgentState) -> AgentState:
    knowledge_db = load_json_data("knowledge_base.json")

    if not state.assessment:
        state.knowledge = []
        return state

    matched_knowledge = []

    for item in knowledge_db:
        item_tags = item.get("tags", [])
        if any(tag in item_tags for tag in state.assessment.problem_tags):
            matched_knowledge.extend(item.get("content", []))

    state.knowledge = matched_knowledge
    return state


def retrieve_resources(state: AgentState) -> AgentState:
    resources_db = load_json_data("resources.json")

    if not state.assessment:
        state.resources = []
        return state

    matched_resources = []

    for item in resources_db:
        item_tags = item.get("tags", [])
        if any(tag in item_tags for tag in state.assessment.problem_tags):
            matched_resources.append(
                Resource(
                    name=item["name"],
                    type=item["type"]
                )
            )

    state.resources = matched_resources
    return state

def generate_response(state: AgentState) -> AgentState:
    prompt = GENERATE_RESPONSE_PROMPT.format(
        user_input=state.user_input,
        assessment=state.assessment.model_dump() if state.assessment else {},
        knowledge=state.knowledge,
        resources=[r.model_dump() for r in state.resources] if state.resources else []
    )

    output_text = call_llm(
        prompt=prompt,
        provider=settings.DEFAULT_LLM_PROVIDER,
        model=settings.DEFAULT_OPENAI_MODEL
    )

    state.response = output_text

    return state
