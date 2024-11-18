from typing import List
from pydantic import BaseModel

class Pokemon(BaseModel):
    name: str
