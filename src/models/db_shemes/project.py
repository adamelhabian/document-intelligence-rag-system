
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from bson import ObjectId


class Project(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    # ... means field is required 
    project_id: str = Field(..., min_length=1)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value

    # to define static function you can use it without need to create object from this class 
    @classmethod
    def get_indexes(cls):
        # list of dict because each dictionary define on index , list -> define multiple indexes
        return [
            {
                # 1 -> decsending order , -1 -> asceinding order 
                # name must be unique
                # key take one or more key
                "key":[("project_id",1)
                    ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]
