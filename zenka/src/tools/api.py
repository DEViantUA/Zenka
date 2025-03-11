import asyncio
import json
import os
import difflib
from typing import List, Optional,Tuple,Union
from .http import AioSession
from .error import ZZZError
from ..model.base import Lang, HoyoAPIHeaders, ErrorText
from ..model.api import CharacterDataHoYo, ZenkaApi

API_URL = "https://enka.network/api/zzz/uid/{uid}"
RAW_BASE_URL = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/zzz/"
RAW_BASE_URL_ZENKA = "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/json/"
HOYO_MENU = "https://sg-wiki-api-static.hoyolab.com/hoyowiki/zzz/wapi/home/hot_content?menu_id=8"
HOYO_WIKI = "https://sg-wiki-api-static.hoyolab.com/hoyowiki/zzz/wapi/entry_page?entry_page_id={pid}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "..", "jsons")

FORCE_LOAD_FILES = {
    "level_format.json",
    "star_format.json", 
    "discs_format.json"
}
JSON_FILES = [
    "avatars.json",
    "equipments.json",
    "locs.json",
    "medals.json",
    "namecards.json",
    "pfps.json",
    "property.json",
    "titles.json",
    "weapons.json",
    "hoyolink.json",
    "level_format.json",
    "star_format.json",
    "discs_format.json",
]

jsons_data = {}
lang: str = Lang.EN.value

async def fetch_json(filename: str):
    if filename in ["level_format.json", "star_format.json", "hoyolink.json", "discs_format.json"]:
        if filename == "hoyolink.json":
            return
        url = RAW_BASE_URL_ZENKA + filename
    else:
        url = RAW_BASE_URL + filename
    
    data = await AioSession.get(url, response_format= "json")
    key = filename.replace(".json", "_data")
    jsons_data[key] = data

async def get_json_files():
    tasks = [fetch_json(filename) for filename in JSON_FILES]
    await asyncio.gather(*tasks)
    await fetch_hoyowiki_data()


async def fetch_hoyowiki_data() -> None:
    json_res = await AioSession.get(HOYO_MENU, headers=HoyoAPIHeaders.HEADERS, response_format= "json")
    tasks = [fetch_page(i["ep_abstract"]["entry_page_id"], i["ep_abstract"]["name"]) 
                for i in json_res["data"]["contents"]]
    results = await asyncio.gather(*tasks)
    
    results = [x for x in results if x is not None]

    enka_names = {jsons_data["locs_data"][lang][c_data["Name"]]: cid 
                    for cid, c_data in jsons_data["avatars_data"].items()}
    
    hoyo_data = {name: CharacterDataHoYo(name=name, link=link, id=hcid, faction=faction, type=tipe, element=element)
                    for name, link, hcid, faction, tipe, element in results}

    matches = {}
    unmatched = []

    for b_name in enka_names.keys():
        exact_match = next((h_name for h_name in hoyo_data.keys() if b_name.lower() in h_name.lower()), None)
        
        if exact_match:
            matches[b_name] = exact_match
        else:
            unmatched.append(b_name)

    remaining_hoyo_keys = set(hoyo_data.keys()) - set(matches.values())
    for b_name in unmatched:
        best_match = find_best_match(b_name, list(remaining_hoyo_keys))
        if best_match:
            matches[b_name] = best_match
            remaining_hoyo_keys.remove(best_match) 
    jsons_data["hoyolink_data"] = {
        enka_names[e_name]: hoyo_data[h_name].model_dump()
        for e_name, h_name in matches.items() if h_name
    }

async def fetch_page(pid: str, name: str) -> Union[Tuple[str, str, str, str, str, str], bool]:
    json_res = await AioSession.get(HOYO_WIKI.format(pid = pid), headers=HoyoAPIHeaders.HEADERS, response_format= "json")
    data = json_res["data"]["page"]["filter_values"]

    faction = data.get("agent_faction", {}).get("value_types", [{}])
    if faction:
        faction = faction[0].get("icon", "default_faction_icon")

    if data.get("agent_stats", {})["value_types"]:
        element = data.get("agent_stats", {}).get("value_types", [{}])[0].get("icon", "unknown")
    if data.get("agent_specialties", {})["value_types"]:
        tipe = data.get("agent_specialties", {}).get("value_types", [{}])[0].get("icon", "")
    else:
        return None


    return name, json_res["data"]["page"]["header_img_url"], pid, faction, tipe, element.strip()

def find_best_match(name: str, candidates: List[str]) -> Optional[str]:
    return next((c for c in candidates if name.lower() in c.lower()),
                (difflib.get_close_matches(name, candidates, n=1, cutoff=0.2) or [None])[0])

class DataManager:
    def __init__(self):
        os.makedirs(JSON_DIR, exist_ok=True)

    async def collect_data(self, assets_save: bool = False) -> dict:
        global jsons_data
        if assets_save and self.check_existing_files():
            jsons_data = self.load_local_data()
            return jsons_data

        await get_json_files()
        self.extra_open()

        if assets_save:
            self.save_all_data()
        return jsons_data

    async def update_data(self):
        await get_json_files()
        self.save_all_data()

    def save_all_data(self):
        for key, data in jsons_data.items():
            filename = os.path.join(JSON_DIR, f"{key}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    def load_local_data(self) -> dict:
        loaded_data = {}
        for filename in JSON_FILES:
            key = filename.replace(".json", "_data")
            filepath = os.path.join(JSON_DIR, filename.replace(".json", "_data.json"))
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    loaded_data[key] = json.load(f)
        return loaded_data
    
    def extra_open(self):
        for filename in FORCE_LOAD_FILES:
            key = filename.replace(".json", "_data")
            filepath = os.path.join(JSON_DIR, filename.replace(".json", "_data.json"))
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    jsons_data[key] = json.load(f)

    def get_data(self) -> dict:
        return jsons_data

    def check_existing_files(self) -> bool:
        return all(os.path.exists(os.path.join(JSON_DIR, f.replace(".json", "_data.json"))) for f in JSON_FILES)


async def fetch_user(uid: int, original: bool = False) -> ZenkaApi:
    data = await AioSession.get(API_URL.format(uid = uid), response_format= "json")
    if data.get("message"):
        raise ZZZError(ErrorText().format_api(text = data.get("message")))
    
    if original:
        return data
    
    return ZenkaApi(jsons_data=jsons_data, lang=lang, **data["PlayerInfo"])

