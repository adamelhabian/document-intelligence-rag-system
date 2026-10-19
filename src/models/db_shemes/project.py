from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId # It allows you to convert a string ID into a MongoDB ObjectId
# bson -> binary json


class Project(BaseModel):
    _id: Optional[ObjectId] # document unique identifier
    project_id: str = Field(...,min_length=1)

    # design custom validation
    @validator('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project id must be alphanumeric")
        return value


    class Config:
        aribtrary_types_allowed=True