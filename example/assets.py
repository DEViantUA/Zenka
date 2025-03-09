from zenka import assets
from typing import Tuple

ICON: assets.IconAssets = assets.get_agent_icon(1151)
COLOR: assets.ColorAssets = assets.get_color_agent(1151)
RGBA: Tuple[int,int,int,int] = assets.hex_to_rgba("#ff0a37")

print(ICON)
print(COLOR)
print(RGBA)
