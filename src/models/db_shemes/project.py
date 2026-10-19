
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from bson import ObjectId


class Project(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
