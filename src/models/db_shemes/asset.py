from pydantic import BaseModel,Field,validator,ConfigDict
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset (BaseModel):

    id: Optional[ObjectId] = Field(None,alias='_id') # document unique identifier
    asset_project_id: ObjectId
    asset_type: str = Field(...,min_length=1)
    asset_name: str = Field(...,min_length=1)
    asset_size: int = Field(None,ge=0) # optional
    asset_pushed_at:datetime = Field(default=datetime.utcnow)
    asset_config: dict = Field(None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


    @classmethod
    def get_indexes(cls):
        # list of dict because each dictionary define on index , list -> define multiple indexes
        return [
            {
            
                "key":[("asset_project_id",1)
                    ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
            
                "key":[("asset_project_id",1),
                    ("asset_name",1)
                    ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            },
        ]

