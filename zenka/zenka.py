import datetime
import asyncio
import os
from PIL import Image
from typing import Dict, List, Union, Optional, Tuple
from .src.model.base import Config, Lang, ErrorText, TranslationLang
from .src.model.generator import ZenkaGenerator
from .src.tools import cache, error, http, git, options, api
from .src.generator import style_one, style_one_profile

def save_file(id: int, card: Image.Image):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    folder = os.path.dirname(f"ZCard/{id}_{data}.png")
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    card.save(f"ZCard/{id}_{data}.png")

class Client:
    def __init__(
        self, lang: Union[Lang,str] = Lang.EN.value,
        character_art: Optional[Dict[Union[int,str], str]] = None,
        character_id: Optional[List[int]] = None,
        config: Config = None
    ):
        self.lang = lang.value if isinstance(lang, Lang) else lang
        self.character_art = character_art if character_art is not None else {}
        self.character_id = character_id if character_id is not None else []
        self.config = config if config is not None else Config()


    async def __aenter__(self):
        cache.Cache.get_cache(maxsize = self.config.cache.maxsize, ttl = self.config.cache.ttl)
        await http.AioSession.enter(self.config.proxy)
        await git.ImageCache.set_assets_download(self.config.asset_save)
        await git.change_font(font_path = self.config.font)
        await api.DataManager().collect_data(self.config.asset_save)
        if not isinstance(self.character_art, dict):
            raise error.ZZZError(ErrorText.charterArt)
    
        if not Lang.is_supported(self.lang):
            raise error.ZZZError(ErrorText().format(self.lang))
        
        self.translateLang = TranslationLang().lang(self.lang)
        api.lang = self.lang
        self.config.color = await options.get_color_user(self.config.color)

        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await http.AioSession.exit(exc_type, exc, tb)

    async def get_api(self, uid: Union[str,int], original: bool = False) -> api.ZenkaApi:
        return  await api.fetch_user(uid, original)
    
    async def update_asset(self) -> None:
        await api.DataManager().update_data()

    async def profile(self, uid: int, color: Tuple[int,int,int,int] = None) -> ZenkaGenerator:
        result = ZenkaGenerator()
        data =  await api.fetch_user(uid)
        for key in data.character_info.characters:           
            result.charter_name.append(key.name)
            result.charter_id.append(key.id)

        result.cards.append(await style_one_profile.StyleOneProfile(key, data.player, self.translateLang, color = color, hide = self.config.hide_uid).start())
        result.player = data.player
        
        if self.config.save:
            for key in result.cards:
                save_file(uid, key.card)
        
        return result
    
    async def card(self, uid: int) -> ZenkaGenerator:
        result = ZenkaGenerator()
        data =  await api.fetch_user(uid)
        task = []
        for key in data.character_info.characters:
            result.charter_name.append(key.name)
            result.charter_id.append(key.id)

            if self.character_id:
                if not key.id in self.character_id:
                    continue 
        
            task.append(style_one.StyleOne(key, data.player, self.translateLang, art = self.character_art.get(key.id), color = self.config.color.get(key.id), hide = self.config.hide_uid).start())
        
        result.player = data.player
        result.cards = await asyncio.gather(*task)


        if self.config.save:
            for key in result.cards:
                save_file(key.id, key.card)


        return result



