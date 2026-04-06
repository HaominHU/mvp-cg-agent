import json
from pathlib import Path

from app.config import settings
from app.llm import call_llm
from app.models import AgentState, Assessment, AssessmentResult, Resource, RiskLevel

from app.prompts import ASSESS_CASE_PROMPT, GENERATE_RESPONSE_PROMPT

from app.logger import get_logger

logger = get_logger(__name__)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_data(file_name: str):
    file_path = DATA_DIR / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_problem_tags(value: object) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized_tags: list[str] = []
    seen: set[str] = set()

    for item in value:
        if not isinstance(item, str):
            continue

        tag = item.strip().lower()
        if not tag:
            continue

        if tag in seen:
            continue

        seen.add(tag)
        normalized_tags.append(tag)

    return normalized_tags

def normalize_risk_level(value: object) -> RiskLevel:
    if not isinstance(value, str):
        return "medium"

    normalized = value.strip().lower()

    if normalized == "low":
        return "low"
    if normalized == "medium":
        return "medium"
    if normalized == "high":
        return "high"

    return "medium"

def normalize_needs_escalation(value: object) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {"true", "yes", "y", "1"}:
            return True

        if normalized in {"false", "no", "n", "0"}:
            return False

    return False

def normalize_search_queries(value: object) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized_queries: list[str] = []
    seen: set[str] = set()

    for item in value:
        if not isinstance(item, str):
            continue

        query = item.strip()
        if not query:
            continue

        if query in seen:
            continue

        seen.add(query)
        normalized_queries.append(query)

    return normalized_queries

def parse_assessment_result(raw_output: str) -> AssessmentResult:
    data = json.loads(raw_output)

    return AssessmentResult(
        problem_tags=normalize_problem_tags(data.get("problem_tags")),
        risk_level=normalize_risk_level(data.get("risk_level")),
        caregiver_emotion=data.get("caregiver_emotion", "unknown"),
        needs_escalation=normalize_needs_escalation(data.get("needs_escalation")),
        search_queries=normalize_search_queries(data.get("search_queries"))
    )

def build_default_assessment_result() -> AssessmentResult:
    return AssessmentResult(
        problem_tags=["unknown"],
        risk_level="medium",
        caregiver_emotion="unknown",
        needs_escalation=False,
        search_queries=[],
    )

def build_public_assessment(assessment_result: AssessmentResult) -> Assessment:
    return Assessment(
        problem_tags=assessment_result.problem_tags,
        risk_level=assessment_result.risk_level,
        caregiver_emotion=assessment_result.caregiver_emotion,
    )

def assess_case(state: AgentState) -> AgentState:
    prompt = ASSESS_CASE_PROMPT.format(user_input=state.user_input)

    raw_output = call_llm(
        prompt=prompt,
        provider=settings.DEFAULT_LLM_PROVIDER,
        model=settings.DEFAULT_OPENAI_MODEL
    )

    try:
        assessment_result = parse_assessment_result(raw_output)
    except Exception as e:
        logger.error("ASSESS PARSE ERROR: %s", e)
        logger.error("RAW OUTPUT: %s", raw_output)
        assessment_result = build_default_assessment_result()

    state.assessment_result = assessment_result
    state.assessment = build_public_assessment(assessment_result)
    state.needs_escalation = assessment_result.needs_escalation

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
