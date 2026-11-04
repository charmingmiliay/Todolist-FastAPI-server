from pydantic import Field

from app.schemas.base import CamelModel

class AskRequest(CamelModel):
    question: str = Field(min_length=1, max_length=500)

class AskResponse(CamelModel):
    answer: str
    model: str
