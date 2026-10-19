from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId



class DataChunk(BaseModel):

    _id: Optional[ObjectId] # document unique identifier
    chunk_text: str = Field(...,min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(...,gt=0)
    chunk_project_id: ObjectId




    class Config:
            aribtrary_types_allowed=True
