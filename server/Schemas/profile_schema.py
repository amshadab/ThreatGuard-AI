
from pydantic import BaseModel, Field
from datetime import datetime


class ProfileCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

class ProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    created_at: datetime

    model_config = {"from_attributes": True}