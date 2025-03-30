from pydantic import BaseModel
from typing import List
from PIL import Image
from ..tools.git import ImageCache

_of = ImageCache()
positionTeams = [
    (39,99),
    (844,99),
    (1655,99),
]

crops = {
    3: 0,
    2: 797,
    1: 1594,
}

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

   

class ZenkaGeneratorTeams(BaseModel):
    player: bool = None
    charter_id: List[int] = []
    charter_name: List[str] = []
    cards: List[ZZZCard] = []
    builds: List[Image.Image] = []

    class Config:
        arbitrary_types_allowed = True


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_image_groups(self, agent_id: List[int]) -> List[List[int]]:
        """Split build_id into groups of 3 (like images)"""
        return [agent_id[i:i+3] for i in range(0, len(agent_id), 3)]

    async def build(self, agent_id: List[int], light: bool = True) -> List[Image.Image]:
        """
        Build one or two images with up to 3 cards each
        (based on agent_id list passed in)
        """

        _of.set_mapping(3)

        groups = self.get_image_groups(agent_id)

        if light:
            full_bg = await _of.full_bg
        else:
            full_bg = await _of.full_bg_b

        
        for i, group in enumerate(groups):
            final_img = full_bg.convert("RGBA").copy()
            for j, id_ in enumerate(group):
                card = next((c for c in self.cards if c.id == id_), None)
                if card:
                    final_img.alpha_composite(card.card, positionTeams[j])

            final_img = final_img.crop((0, 0, final_img.width - crops.get(len(group)), final_img.height))
            self.builds.append(final_img)

        return self.builds
