from pydantic import Field, BaseModel, ConfigDict
from uuid import UUID, uuid4


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    question : str
    thread_id: UUID = Field(default_factory = uuid4)


class ChatResponse(BaseModel):
    answer : str
    thread_id: UUID
    sources : list[str]

