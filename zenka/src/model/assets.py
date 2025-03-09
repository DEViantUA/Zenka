from pydantic import BaseModel
from typing import Tuple
from ..tools.api import DataManager
from ..model.base import URL_ASSETS

ICON = "https://act-webstatic.hoyoverse.com/game_record/zzzv2/role_square_avatar/role_square_avatar_{agent_id}.png"

def hex_to_rgba(hex_code: str) -> Tuple[int,int,int,int]:
    hex_code = hex_code.strip('#')
    
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)
    
    alpha = 255 
    
    return red, green, blue, alpha

class IconAssets(BaseModel):
    icon: str = None
    image: str = None
    full: str = None
    circle_icon: str = None
    
class ColorAssets(BaseModel):
    accent: Tuple[int,int,int,int]
    mindscape: Tuple[int,int,int,int]

def get_agent_icon(id: int) -> IconAssets:
    data = DataManager().get_data()
    return IconAssets(
        icon = ICON.format(agent_id = id),
        image = data.get("hoyolink_data").get(str(id)).get("link"),
        full = URL_ASSETS + data.get("avatars_data").get(str(id)).get("Image"),
        circle_icon = URL_ASSETS + data.get("avatars_data").get(str(id)).get("CircleIcon"),
    )


def get_color_agent(id: int) -> ColorAssets:
    data = DataManager().get_data()
    return ColorAssets(
        accent= hex_to_rgba(data.get("avatars_data").get(str(id)).get("Colors").get("Accent")),
        mindscape= hex_to_rgba(data.get("avatars_data").get(str(id)).get("Colors").get("Mindscape"))
    )