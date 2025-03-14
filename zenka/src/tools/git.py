# Copyright 2025 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image
import os
import threading
from pathlib import Path
from io import BytesIO

from .http import AioSession
from .cache import Cache

lock = threading.Lock()

_caches = Cache.get_cache()

assets = Path(__file__).parent.parent / 'assets'

_BASE_URL = 'https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/enka/'

font = str(assets / 'font' / 'impact.ttf')


def determine_font_path_automatically(font_file = 'Times New Roman.ttf'):
    font_dirs = [
        '/usr/share/fonts',          
        '/usr/local/share/fonts',    
        '/Library/Fonts',           
    ]
        
    for font_dir in font_dirs:
        font_path = os.path.join(font_dir, font_file)
        if os.path.isfile(font_path):
            return font_path

    return None

async def change_font(font_path = None):
    global font
    if font_path is None:
        font = str(assets / 'font' / 'impact.ttf')
    else:
        font_path = os.path.abspath(font_path)
        if os.path.isfile(font_path):
            font = font_path 
        else:
            font_path = determine_font_path_automatically(font_path)
            if font_path is None:
                font = str(assets / 'font' / 'impact.ttf')


total_style = {
    'g_five': 'stars/five.png',
    'g_four': 'stars/four.png',
    'g_three': 'stars/three.png',
    'g_two': 'stars/two.png',
    'g_one': 'stars/one.png',
    "rank_a": 'rank_icon/a.png',
    "rank_b": 'rank_icon/b.png',
    "rank_s": 'rank_icon/s.png',

    "rank_w_a": 'rank_icon/w_a.png',
    "rank_w_b": 'rank_icon/w_b.png',
    "rank_w_s": 'rank_icon/w_s.png',

    "const_0": 'const/const_0.png',
    "const_1": 'const/const_1.png',
    "const_2": 'const/const_2.png',
    "const_3": 'const/const_3.png',
    "const_4": 'const/const_4.png',
    "const_5": 'const/const_5.png',
    "const_6": 'const/const_6.png',

    "skill_1_s": 'skill_icon/IconRoleSkillKeyNormal.png',
    "skill_2_s": 'skill_icon/IconRoleSkillKeyEvade.png',
    "skill_3_s": 'skill_icon/IconRoleSkillKeySwitch.png',
    "skill_4_s": 'skill_icon/IconRoleSkillKeySpecialV2.png',
    "skill_5_s": 'skill_icon/IconRoleSkillKeyUltimateV2.png',
    "skill_6_s": 'skill_icon/IconRoleSkillKe.png',

    "core_skill_a": "core_skill/svgexport-15.png",
    "core_skill_b": "core_skill/svgexport-16.png",
    "core_skill_c": "core_skill/svgexport-17.png",
    "core_skill_d": "core_skill/svgexport-18.png",
    "core_skill_e": "core_skill/svgexport-19.png",
    "core_skill_f": "core_skill/svgexport-20.png",

    "conts_0_lvl": "const/const_0.png",
    "conts_1_lvl": "const/const_1.png",
    "conts_2_lvl": "const/const_2.png",
    "conts_3_lvl": "const/const_3.png",
    "conts_4_lvl": "const/const_4.png",
    "conts_5_lvl": "const/const_5.png",
    "conts_6_lvl": "const/const_6.png"
    
}


card_style = {
    'background': 'background/background.png',
    'cadr': 'background/cadr.png',
    'charter_bg': 'background/charter_bg.png',
    'dark_frame_info': 'background/dark_frame_info.png',
    'frame_info': 'background/frame_info.png',
    'frame': 'background/frame.png',
    'mask': 'background/mask.png',
    'shadow': 'background/shadow.png',
    'text_frame': 'background/text_frame.png',


    'frame_background_black': 'relict/frame_background_black.png',
    'frame_background': 'relict/frame_background.png',
    'frame_relict': 'relict/frame.png',
    'frame_wb_background': 'relict/frame_wb_background.png',
    'lvl': 'relict/lvl.png',
    'rank_leve': "relict/rank_level.png",
    'sets_background': 'relict/sets_background.png',
    'sets_collor': 'relict/sets_collor.png',
    'sets_count': 'relict/sets_count.png',
    'stats': 'relict/stats.png',


    'stats_background': 'stats/background.png',
    'skill_count': 'stats/skill_count.png',
    'value': 'stats/value.png',

    'weapon_background': 'weapon/background.png',
    'levl': 'weapon/levl.png',
    'up': 'weapon/up.png',
    
}

profile_style = {
    'main_background': 'profile_style_one/main_background.png',
    'background': 'profile_style_one/background.png',
    'cinema_frame': 'profile_style_one/cinema_frame.png',
    'cinema': 'profile_style_one/cinema.png',
    'frame_avatar': 'profile_style_one/frame_avatar.png',
    'frame_icon': 'profile_style_one/frame_icon.png',

    'lvl_b': 'profile_style_one/lvl_b.png',
    'lvl_c': 'profile_style_one/lvl_c.png',
    'lvl_w': 'profile_style_one/lvl_w.png',

    'mask': 'profile_style_one/mask.png',
    'shadow_charter': 'profile_style_one/shadow_charter.png',
    'texture_avatar': 'profile_style_one/texture_avatar.png',


    'uid_b': 'profile_style_one/uid_b.png',
    'uid_c': 'profile_style_one/uid_c.png',
    'uid_w': 'profile_style_one/uid_w.png',
    'medal':'profile_style_one/medal.png'
    
}

class ImageCache:
    
    _assets_download = False
    _mapping = {}
            
    @classmethod
    async def set_assets_download(cls, download = False):
        cls._assets_download = download
    
    @classmethod
    def set_mapping(cls,style: int = 1) -> None:
        if style == 1:
            cls._mapping = card_style
        elif style == 2:
            cls._mapping = profile_style

        
    @classmethod
    async def _load_image(cls, name):
        
        try:
            image = _caches[name]
        except KeyError:
            try:
                _caches[name] = image = Image.open(assets / name)
                return _caches[name]
            except Exception as e:
                pass
        
        try:
            _caches[name] = image = Image.open(assets / name)
            return _caches[name]
        except Exception as e:
            pass
        
        url = _BASE_URL + name
        if url in _caches:
            return _caches[name]
        else:
            image_data = await AioSession.get(url, response_format= "bytes")
            image = Image.open(BytesIO(image_data))
            _caches[name] = image
        
        if cls._assets_download:
            file_path = assets / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(str(assets / name))
        
        return image

    async def __getattr__(cls, name):
        if name in cls._mapping:
            return await cls._load_image(cls._mapping[name])
        else:
            if name in total_style:
                return await cls._load_image(total_style[name]) 
            else:
                raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{name}'")