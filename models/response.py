from pydantic import BaseModel
from typing import List

class Pokemon_List(BaseModel):
    pokemon_names: List[str]