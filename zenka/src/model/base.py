from pydantic import BaseModel, Field
from typing import Dict, Tuple, Optional
from enum import Enum


URL_ASSETS = "https://enka.network"
DEFAULT_AVATAR = "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/default_icon.png"

class HoyoAPIHeaders:
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://wiki.hoyolab.com",
        "referer": "https://wiki.hoyolab.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "x-rpc-language": "en-us",
        "x-rpc-wiki_app": "zzz"
    }

class ElementType(Enum):
    ELEC = "Electric"
    PHYSICS = "Physical"
    ICE = "Ice"
    FIRE = "Fire"
    ETHER = "Ether"

    @classmethod
    def convert(cls, value: str) -> str:
        return cls.__members__.get(value.upper(), "Unknown").value

class Lang(Enum):
    CHT = "cht"
    CN = "cn"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"
    VI = "vi"

    @classmethod
    def is_supported(cls, lang: str) -> bool:
        return lang in cls._value2member_map_

class Translator(BaseModel):
    lvl: str
    AR: str
    WL: str
    AC: str
    AB: str


class TranslationLang(BaseModel):
    translations: Dict[str, Translator] = {
        "en": Translator(lvl="LVL", AR="AR", WL="WL", AC="Achievements", AB="Abyss"),
        "ru": Translator(lvl="Уровень", AR="РП", WL="УМ", AC="Достижения", AB="Бездна"),
        "ua": Translator(lvl="Рівень", AR="РП", WL="РС", AC="Досягнення", AB="Безодня"),
        "vi": Translator(lvl="Cấp độ", AR="AR", WL="WL", AC="Thành tích", AB="Vực thẳm"),
        "th": Translator(lvl="ระดับ", AR="AR", WL="WL", AC="ความสำเร็จ", AB="Abyss"),
        "pt": Translator(lvl="Nível", AR="AR", WL="WL", AC="Conquistas", AB="Abismo"),
        "kr": Translator(lvl="레벨", AR="AR", WL="WL", AC="업적", AB="어비스"),
        "jp": Translator(lvl="レベル", AR="AR", WL="WL", AC="アチーブメント", AB="アビス"),
        "zh": Translator(lvl="等级", AR="AR", WL="WL", AC="成就总数", AB="深境螺旋"),
        "cn": Translator(lvl="等级", AR="AR", WL="WL", AC="成就总数", AB="深境螺旋"),
        "id": Translator(lvl="Level", AR="AR", WL="WL", AC="Prestasi", AB="Abyss"),
        "fr": Translator(lvl="Niveau", AR="AR", WL="WL", AC="Réalisations", AB="Abîme"),
        "es": Translator(lvl="Nivel", AR="AR", WL="WL", AC="Logros", AB="Abismo"),
        "de": Translator(lvl="Level", AR="AR", WL="WL", AC="Erfolge", AB="Abyss"),
        "chs": Translator(lvl="等级", AR="AR", WL="WL", AC="成就总数", AB="深境螺旋"),
        "cht": Translator(lvl="等級", AR="AR", WL="WL", AC="成就總數", AB="深境螺旋"),
    }

    def lang(self, lang_code: str) -> Translator:
        return self.translations.get(lang_code, self.translations["en"])
    


class CacheConfig(BaseModel):
    maxsize: int = 150
    ttl: int = 300

class Config(BaseModel):
    font: Optional[str] = None
    save: bool = False
    hide_uid: bool = False
    asset_save: bool = False
    cache: CacheConfig = CacheConfig()
    proxy: Optional[str] = None
    color: Dict[int, Tuple[int, int, int, int]] = Field(default_factory=dict)

class ErrorText(BaseModel):
    lang: Dict[int, str] = {"code": 1, "text": "This language key [{lang}] is not supported"}
    charterArt: Dict[int, str] = {"code": 2, "text": "The 'character_art' parameter must be of type Dict[Union[int, str], str], "
                "where the key is an integer or string (character ID), "
                "and the value is a string (URL)."
                }
    api: Dict[int, str] = {"code": 3, "text": "{text}"}

    def format(self, **kwargs) -> dict:
        return {"code": self.lang["code"], "text": self.lang["text"].format(**kwargs)}
    
    def format_api(self, **kwargs) -> dict:
        return {"code": self.lang["code"], "text": self.api["text"].format(**kwargs)}

