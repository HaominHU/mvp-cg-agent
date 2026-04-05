from app.logger import get_logger
from app.models import AgentState, Assessment
from app.tools import (
    assess_case,
    generate_response,
    retrieve_knowledge,
    retrieve_resources,
)

logger = get_logger(__name__)


def run_agent(user_input: str) -> AgentState:
    state = AgentState(
        user_input=user_input,
        assessment=None,
        knowledge=None,
        resources=None,
        response=None,
        needs_escalation=False,
    )

    logger.info("INITIAL STATE: %s", state.model_dump())

    # Step 1: assess
    state = assess_case(state)
    logger.info("AFTER ASSESS: %s", state.model_dump())

    # Step 2: safety / escalation
    if state.needs_escalation:
        if not state.assessment:
            state.assessment = Assessment(
                problem_tags=["urgent concern"],
                risk_level="high",
                caregiver_emotion="concerned"
            )

        state.response = (
            "This situation may involve elevated risk. "
            "Please contact a doctor, qualified professional, "
            "or local emergency services if urgent help is needed."
        )
        logger.warning("AFTER ESCALATION: %s", state.model_dump())
        return state

    # Step 3: retrieve knowledge
    state = retrieve_knowledge(state)
    logger.info("AFTER KNOWLEDGE: %s", state.model_dump())

    # Step 4: retrieve resources
    state = retrieve_resources(state)
    logger.info("AFTER RESOURCES: %s", state.model_dump())

    # Step 5: generate final response
    state = generate_response(state)
    logger.info("AFTER RESPONSE: %s", state.model_dump())

    return state
