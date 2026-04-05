from enum import Enum
from pydantic import BaseModel
from typing import Optional

class LLMProvider(str, Enum):
    OPENAI = "openai"

class OpenAIModel(str, Enum):
    GPT_5_MINI = "gpt-5.4-mini"
    GPT_5 = "gpt-5.4"

class LLMTestRequest(BaseModel):
    prompt: str
    provider: LLMProvider = LLMProvider.OPENAI
    model: OpenAIModel = OpenAIModel.GPT_5_MINI

class LLMTestResponse(BaseModel):
    provider: str
    model: str
    output_text: str

class Assessment(BaseModel):
    problem_tags: list[str]
    risk_level: str
    caregiver_emotion: str

class Resource(BaseModel):
    name: str
    type: str

class AgentRunRequest(BaseModel):
    user_input: str

class AgentRunResponse(BaseModel):
    assessment: Assessment
    recommendations: list[str]
    resources: list[Resource]
    final_message: str

class AgentState(BaseModel):
    user_input: str

    # step 1
    assessment: Optional[Assessment] = None

    # step 2
    knowledge: Optional[list[str]] = None

    # step 3
    resources: Optional[list[Resource]] = None

    # final
    response: Optional[str] = None

    # control
    needs_escalation: bool = False
