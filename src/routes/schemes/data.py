from pydantic import BaseModel
from typing import Optional

# basemodel is main structure of the schema



class ProcessRequest(BaseModel):
    file_id: str = None
    chunk_size: Optional[int]=100
    overlap_size: Optional[int]=20
    # do help me understand that this attribute response to do action 
    do_reset: Optional[int]=0