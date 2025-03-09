from pydantic import BaseModel
from typing import List
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

