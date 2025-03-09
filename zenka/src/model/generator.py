from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from ..model.api import PlayerData
from PIL import Image


class ZZZProfileCard(BaseModel):
    color: tuple
    card: Image.Image
    class Config:
        arbitrary_types_allowed = True

class ZZZCard(BaseModel):
    id: int
    name: str
    color: tuple
    icon: str
    card: Image.Image
    
    class Config:
        arbitrary_types_allowed = True

class ZenkaGenerator(BaseModel):
    player: bool = None
    charter_id: List[int] = []
    charter_name: List[str] = []
    cards: List[ZZZCard] = []

