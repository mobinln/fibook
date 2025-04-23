from pydantic import BaseModel


class SimpleMessageResponse(BaseModel):
    details: str
