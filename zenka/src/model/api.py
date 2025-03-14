from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional, Dict, Union
import math

ICON_PROPS = {
    11101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-3.png",  # HP [Base]
    11102: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-3.png",  # HP%
    11103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-3.png",  # HP [Flat]
    12101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-4.png",  # ATK [Base]
    12102: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-4.png",  # ATK%
    12103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-4.png",  # ATK [Flat]
    12201: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-6.png",  # Impact [Base]
    12202: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-6.png",  # Impact%
    13101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-5.png",  # Def [Base]
    13102: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-5.png",  # Def%
    13103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-5.png",  # Def [Flat]
    20101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-7.png",  # Crit Rate [Base]
    20103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-7.png",  # Crit Rate [Flat]
    21101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-8.png",  # Crit DMG [Base]
    21103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-8.png",  # Crit DMG [Flat]
    23101: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-11.png",  # Pen Ratio [Base]
    23103: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-11.png",  # Pen Ratio [Flat]
    23201: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-12.png",  # PEN [Base]
    23203: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-12.png",  # PEN [Flat]
    30501: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-13.png",  # Energy Regen [Base]
    30502: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-13.png",  # Energy Regen%
    30503: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-13.png",  # Energy Regen [Flat]
    31201: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-9.png",  # Anomaly Proficiency [Base]
    31203: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-9.png",  # Anomaly Proficiency [Flat]
    31401: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-10.png",  # Anomaly Mastery [Base]
    31402: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-10.png",  # Anomaly Mastery%
    31403: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-10.png",  # Anomaly Mastery [Flat]
    31501: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(1).png",  # Physical DMG Bonus [Base]
    31503: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(1).png",  # Physical DMG Bonus [Flat]
    31601: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(2).png",  # Fire DMG Bonus [Base]
    31603: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(2).png",  # Fire DMG Bonus [Flat]
    31701: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2.png",  # Ice DMG Bonus [Base]
    31703: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2.png",  # Ice DMG Bonus [Flat]
    31801: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(3).png",  # Electric DMG Bonus [Base]
    31803: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(3).png",  # Electric DMG Bonus [Flat]
    31901: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(4).png",  # Ether DMG Bonus [Base]
    31903: "https://raw.githubusercontent.com/DEViantUA/ZZZeroCardData/refs/heads/main/icon/svgexport-2%20(4).png"   # Ether DMG Bonus [Flat]
}


def weapon_main(jsons_data:dict, level:int, asc:int, v:int):
    main_value = jsons_data["weapons_data"][str(v)]["MainStat"]["PropertyValue"]
    wp_level_value = jsons_data["level_format_data"][str(jsons_data["weapons_data"][str(v)]["Rarity"])][str(level)]["value"]
    wp_star_value = jsons_data["star_format_data"][str(jsons_data["weapons_data"][str(v)]["Rarity"])][str(asc)]["main_value"]
    formula = main_value * (1 + wp_level_value / 10000 + wp_star_value / 10000)
    return int(formula)

def weapon_sub(jsons_data:dict, asc:int, v:int):
    main_value = jsons_data["weapons_data"][str(v)]["SecondaryStat"]["PropertyValue"]
    wp_star_value = jsons_data["star_format_data"][str(jsons_data["weapons_data"][str(v)]["Rarity"])][str(asc)]["second_value"]
    formula = main_value * (1 + wp_star_value / 10000)
    return int(formula)

def calculate_stats(jsons_data: dict, level: int, promotion: int, core: int, cid: int, weapon: WeaponData, equipped: List[EquippedList], lang_dict: dict):
   
    promotion = int(promotion)
    avatar_data = jsons_data["avatars_data"].get(str(cid), {})
    if not avatar_data:
        raise ValueError(f"No character data found for CID {cid}")

    base_props = avatar_data.get("BaseProps", {}).copy()
    growth_props = avatar_data.get("GrowthProps", {})
    promotion_props = avatar_data.get("PromotionProps", [])
    core_enhancement_props = avatar_data.get("CoreEnhancementProps", {})

    if promotion - 1 >= len(promotion_props):
        raise ValueError(f"Incorrect promotion {promotion} for CID {cid}")

    promotion_values = promotion_props[promotion - 1]
    core_enhancement_values = core_enhancement_props[core]

    for key, base_value in base_props.items():
        growth_value = (growth_props.get(key, 0) * (level - 1)) / 10000
        promotion_value = promotion_values.get(key, 0)
        core_enhancement_value = core_enhancement_values.get(key, 0)

        base_props[key] = int(base_value) + int(growth_value) + int(promotion_value) + int(core_enhancement_value)
    if "23103" not in base_props:
        base_props["23103"] = 0
    if "23203" not in base_props:
        base_props["23203"] = 0

    main_base_props = base_props.copy()

    if weapon:
        base_props["12101"] += weapon.main.value
        for stat in [weapon.sub]:
            stat_id = str(stat.id)
            if stat_id in base_props:
                base_props[stat_id] += stat.value
            elif str(stat.id - 1) in base_props and stat.id - 1 not in [20101, 21101, 23101]:
                base_props[str(stat.id - 1)] += (stat.value / 10000) * main_base_props[str(stat.id - 1)]
            elif str(stat.id - 2) in base_props:
                base_props[str(stat.id - 2)] += stat.value
            else:
                base_props[stat_id] = stat.value
    sets = []
    for item in equipped:
        equipment = item.equipment
        if not equipment:
            continue
        sets.append(equipment.sets)
        for main_stat in equipment.main:
            stat_id = str(main_stat.id)
            if stat_id in base_props:
                base_props[stat_id] += main_stat.value
            elif str(main_stat.id-2) in base_props:
                base_props[str(main_stat.id-2)] += main_stat.value
            elif str(main_stat.id - 1) in base_props and main_stat.id - 1 not in [20101, 21101, 23101]:
                base_props[str(main_stat.id - 1)] += (main_stat.value / 10000) * main_base_props[str(main_stat.id - 1)]
            else:
                base_props[stat_id] = main_stat.value
        for sub_stat in equipment.sub:
            stat_id = str(sub_stat.id)
            if stat_id in base_props:
                base_props[stat_id] += sub_stat.value
            elif str(sub_stat.id - 1) in base_props and sub_stat.id - 1 not in [20101, 21101, 23101]:
                base_props[str(sub_stat.id - 1)] += (sub_stat.value / 10000) * main_base_props[str(sub_stat.id - 1)]
            elif str(sub_stat.id - 2) in base_props:
                base_props[str(sub_stat.id - 2)] += sub_stat.value
            else:
                base_props[stat_id] = sub_stat.value
                
    main_bonus = []
    for ijk in sets:
        if ijk not in main_bonus:
            cou = sets.count(ijk)
            if cou >= 2:
                main_bonus.append(ijk)
    for mnp in main_bonus:
        i = mnp.bonus
        if i == {}:
            continue
        sid = list(i.keys())[0]
        val = list(i.values())[0]
        if sid in base_props:
            base_props[sid] += val
        elif str(int(sid) - 1) in base_props and str(int(sid) - 1) not in [20101, 21101, 23101]:
            base_props[str(int(sid) - 1)] += (val / 10000) * main_base_props[str(int(sid) - 1)]
        elif str(int(sid) - 2) in base_props:
            base_props[str(int(sid) - 2)] += val
        else:
            base_props[sid] = val

    property_data = jsons_data.get("property_data", {})
    BaseStats = [
        Stat(
            id=int(key),
            key = property_data.get(key, {}).get("Name", "Unknown"),
            name= lang_dict.get(property_data.get(key, {}).get("Name", "Unknown")),
            value= int(value),
            format=property_data.get(key, {}).get("Format", "{}"),
            base = main_base_props.get(key, 0),
            add = int(value) - main_base_props.get(key, 0),
            icon = ICON_PROPS.get(int(key), "")
        )
        for key, value in base_props.items()
    ]
    return BaseStats


class CharacterDataHoYo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    link: str
    id: str
    faction: Optional[Union[str, List[str]]] = None
    type: Optional[str] = None
    element: str


class Stat(BaseModel):
    id: int
    key: str
    name: str
    value: Union[str, int,float]
    icon: str = None
    format: str
    base: int = None
    add: int = None

    
    def get_value(self, base: bool = False, add: bool = False) -> str:
        if base:
            val = self.base
        elif add:
            val = self.add
        else:
            val = self.value

        if self.id in [12101, 13101, 12201, 31401, 31201, 23203]:
            return str(int(val))
        elif self.id == 30501:
            return "{:.1f}".format(math.floor((val/100) * 10) / 10)
        if self.format == "{0:0}":
            return "{:.0f}".format(math.floor(val))
        elif self.format == "{0:0.#}":
            return "{:.1f}".format(math.floor(val * 10) / 10)
        elif self.format == "{0:0.##}":
            return "{:.2f}".format(math.floor(val * 100) / 100)
        elif self.format == "{0:0.#%}":
            return "{:.1f}%".format(math.floor((val/100) * 10) / 10)
        else:
            return val

class Title(BaseModel):
    id: int = None
    name: str = None
    color: Color = None

class Medal(BaseModel):
    id: int = Field(alias="MedalIcon")
    name: str = None
    value: int = Field(alias="Value")
    type: int = Field(alias="MedalType")
    icon: str = None

class ProfileDetail(BaseModel):
    nickname: str = Field(alias="Nickname")
    avatar_id: int = Field(alias="AvatarId")
    icon: str = None
    uid: int = Field(alias="Uid")
    level: int = Field(alias="Level")
    title: Union[Title, int] = Field(alias="Title")
    pfp_id: int = Field(alias="ProfileId")

    @field_validator("title")
    def validate_title(cls, value):
        if isinstance(value, int):
            return Title(id=value)
        return value

class WeaponData(BaseModel):
    id: int = Field(alias="Id")
    uid: int = Field(alias="Uid")
    name: str = None
    rarity: int = None
    level: int = Field(alias="Level")
    cons: int = Field(alias="UpgradeLevel")
    icon: str = None
    professio: str = None
    main: dict = None
    sub: dict = None
    asc: int = Field(alias="BreakLevel")

class SkillLevelList(BaseModel):
    level: int = Field(alias="Level")
    index: int = Field(alias="Index")

class SubProperty(BaseModel):
    id: int = Field(alias="PropertyId")
    rolls: int = Field(alias="PropertyLevel")
    icon: str = None
    value: int = Field(alias="PropertyValue")
    format: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = ICON_PROPS.get(int(self.id), "")
        self.value *= self.rolls

    def get_value(self) -> str:
        if self.id in [12103, 13103]:
            return str(int(self.value))
        if self.format == "{0:0}":
            return "{:.0f}".format(math.floor(self.value))
        elif self.format == "{0:0.#}":
            return "{:.1f}".format(math.floor(self.value * 10) / 10)
        elif self.format == "{0:0.##}":
            return "{:.2f}".format(math.floor(self.value * 100) / 100)
        elif self.format == "{0:0.#%}":
            return "{:.1f}%".format(math.floor((self.value/100) * 10) / 10)
        else:
            return self.value

class MainProperty(BaseModel):
    id: int = Field(alias="PropertyId")
    icon: str = None
    value: int = Field(alias="PropertyValue")
    format: str = None
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = ICON_PROPS.get(int(self.id), "")

    def get_value(self) -> str:
        if self.id in [12103, 13103]:
            return str(int(self.value))
        if self.format == "{0:0}":
            return "{:.0f}".format(math.floor(self.value))
        elif self.format == "{0:0.#}":
            return "{:.1f}".format(math.floor(self.value * 10) / 10)
        elif self.format == "{0:0.##}":
            return "{:.2f}".format(math.floor(self.value * 100) / 100)
        elif self.format == "{0:0.#%}":
            return "{:.1f}%".format(math.floor((self.value/100) * 10) / 10)
        else:
            return self.value 

class Equipment(BaseModel):
    id: int = Field(alias="Id")
    uid: int = Field(alias="Uid")
    rarity: int = 2
    icon: str = None
    level: int = Field(alias="Level")
    break_level: int = Field(alias="BreakLevel")
    max_level: int = 9
    avalibale: bool = Field(alias="IsAvailable")
    locked: bool = Field(alias="IsLocked")
    trash: bool = Field(alias="IsTrash")
    main: List[MainProperty] = Field(alias="MainPropertyList")
    sub: List[SubProperty] = Field(alias="RandomPropertyList")
    sets: dict = None

class EquippedList(BaseModel):
    slot: int = Field(alias="Slot")
    equipment: Equipment = Field(alias="Equipment")

class CharterShowCase(BaseModel):
    id: int
    name: str
    icon: CharterIcon
    element: Element
    rarity: int
    color: Color
    level: int
    max_level: int


class Character(BaseModel):
    id: int = Field(alias="Id")
    name: str = None
    icon: str = None
    element: str = None
    faction: str = None
    profession: str = None
    rarity: int = None
    color: dict = None
    level: int = Field(alias="Level")
    max_level: int = Field(alias="PromotionLevel")
    skills: List[SkillLevelList] = Field(alias="SkillLevelList")
    core_skill: int = Field(alias="CoreSkillEnhancement")
    cinema: List[bool] = Field(alias="TalentToggleList")
    const: int = Field(alias="TalentLevel")
    weapon: Optional[WeaponData]  = Field(None, alias="Weapon")
    equippe: List[EquippedList] = Field(alias="EquippedList")
    stats: list = None
    reward: Optional[List[int]] = Field(alias="ClaimedRewardList")
    
    model_config = ConfigDict(populate_by_name=True)

class CharacterData(BaseModel):
    characters: List[Character] = Field(alias="AvatarList")

class PlayerData(BaseModel):
    medal_list: List[Medal] = Field(alias="MedalList")
    profile: ProfileDetail = Field(alias="ProfileDetail")
    desc: str = Field(alias="Desc")
    characters: list = []

class CharterIcon(BaseModel):
    icon: str
    circle_icon: str

class Element(BaseModel):
    name: str
    icon: str

class Profession(BaseModel):
    name: str
    icon: str

class Color(BaseModel):
    accent: str
    mindscape: str

class Sets(BaseModel):
    id: int
    name: str
    icon: str = None
    bonus: Dict[str, int]

class WeaponProps(BaseModel):
    id: int
    value: int
    icon: str = None
    format: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_value(self) -> str:
        if self.id in [12103, 13103]:
            return str(int(self.value))
        if self.format == "{0:0}":
            return "{:.0f}".format(math.floor(self.value))
        elif self.format == "{0:0.#}":
            return "{:.1f}".format(math.floor(self.value * 10) / 10)
        elif self.format == "{0:0.##}":
            return "{:.2f}".format(math.floor(self.value * 100) / 100)
        elif self.format == "{0:0.#%}":
            return "{:.1f}%".format(math.floor((self.value/100) * 10) / 10)
        else:
            return self.value


class ZenkaApi(BaseModel):
    player: Optional[PlayerData] = Field(alias="SocialDetail")
    character_info: CharacterData = Field(alias="ShowcaseDetail")

    def __init__(self, jsons_data: Dict, lang: str, **data):
        super().__init__(**data)
        data_charter = jsons_data.get("avatars_data")
        data_lang = jsons_data.get("locs_data")
        data_lang = data_lang.get(lang)
        hoyolink_data = jsons_data.get("hoyolink_data")
        weapon_data = jsons_data.get("weapons_data")
        equipments_data = jsons_data.get("equipments_data")
        property_data = jsons_data.get("property_data", {})
        medal_data = jsons_data.get("medals_data", {})
        titles_data = jsons_data.get("titles_data", {})
        pfps_data = jsons_data.get("pfps_data", {})

        for charters in self.character_info.characters:
            data_charters = data_charter.get(str(charters.id))
            hoyolink_datas = hoyolink_data.get(str(charters.id))
            charters.name = data_lang.get(data_charters.get("Name"))
            charters.icon = CharterIcon(icon = data_charters.get("Image"), circle_icon = data_charters.get("CircleIcon"))
            charters.element = Element(name = data_charters.get("ElementTypes")[0], icon=hoyolink_datas.get("element"))
            charters.profession = Profession(name= data_charters.get("ProfessionType"), icon=hoyolink_datas.get("type"))
            charters.faction = hoyolink_datas.get("faction")
            charters.rarity = data_charters.get("Rarity")
            charters.color = Color(accent=data_charters.get("Colors").get("Accent"), mindscape = data_charters.get("Colors").get("Mindscape"))
            
            if charters.weapon:
                weapon_datas = weapon_data.get(str(charters.weapon.id)) 
                charters.weapon.name = data_lang.get(weapon_datas.get("ItemName"))
                charters.weapon.icon = weapon_datas.get("ImagePath")
                charters.weapon.professio = weapon_datas.get("ProfessionType")
                charters.weapon.rarity = weapon_datas.get("Rarity")
                main_id = int(weapon_datas.get("MainStat").get("PropertyId"))
                charters.weapon.main = WeaponProps(id = main_id, value = weapon_main(jsons_data, charters.weapon.level, charters.weapon.asc,charters.weapon.id), icon = ICON_PROPS.get(main_id, ""))
            
                sub_id = int(weapon_datas.get("SecondaryStat").get("PropertyId"))
                charters.weapon.sub = WeaponProps(id = sub_id, value = weapon_sub(jsons_data, charters.weapon.asc,charters.weapon.id), icon = ICON_PROPS.get(sub_id, ""), format=property_data.get(str(sub_id), {}).get("Format"))

            self.player.characters.append(
                CharterShowCase(
                    id = charters.id,
                    name = charters.name,
                    rarity=charters.rarity,
                    icon= charters.icon,
                    element = charters.element,
                    color = charters.color,
                    level = charters.level,
                    max_level = charters.max_level
                )
            )
            for key in charters.equippe:
                sets_id = equipments_data["Items"].get(str(key.equipment.id)).get("SuitId")
                key.equipment.icon = equipments_data["Suits"].get(str(sets_id)).get("Icon")
                key.equipment.rarity = equipments_data["Items"].get(str(key.equipment.id)).get("Rarity")
                key.equipment.main[0].value *= (1 + jsons_data["discs_format_data"][str(key.equipment.rarity)][str(key.equipment.level)] / 10000)
                key.equipment.sets = Sets(
                    id = sets_id,
                    name = data_lang.get(equipments_data["Suits"].get(str(sets_id)).get("Name")),
                    icon = key.equipment.icon,
                    bonus = equipments_data["Suits"].get(str(sets_id)).get("SetBonusProps")
                )


            charters.stats = calculate_stats(jsons_data, charters.level, charters.max_level / 10, charters.core_skill, charters.id, charters.weapon, charters.equippe, data_lang)

            for key in charters.equippe:
                key.equipment.main[0].format = property_data.get(str(key.equipment.main[0].id), {}).get("Format", "{}")
                for subs in key.equipment.sub:
                    subs.format = property_data.get(str(subs.id), {}).get("Format", "{}")

        for medal in self.player.medal_list:
            medal.name = data_lang.get(medal_data.get(str(medal.id)).get("Name"))
            medal.icon = medal_data.get(str(medal.id)).get("Icon")
        
        title = titles_data.get(str(self.player.profile.title.id))
        self.player.profile.icon = pfps_data.get(str(self.player.profile.pfp_id)).get("Icon")
        if title:
            self.player.profile.title.name =  data_lang.get(title.get("TitleText"))
            self.player.profile.title.color = Color(accent= title.get("ColorA"), mindscape= title.get("ColorB"))
        else:
            self.player.profile.title = None