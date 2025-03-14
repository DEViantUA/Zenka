import asyncio
from PIL import Image, ImageDraw
from typing import Tuple
from ..model.base import Translator
from ..model.api import Character, Equipment, PlayerData
from ..tools.git import ImageCache
from ..tools import pill
from ..model.generator import ZZZCard
from ..model.base import URL_ASSETS
from ..model.assets import get_agent_icon, get_color_agent

_of = ImageCache()
_of.set_mapping(1)


async def get_skill_icon(index: int) -> Image.Image:
    return {
        0: await _of.skill_1_s,
        1: await _of.skill_4_s,
        2: await _of.skill_2_s,
        3: await _of.skill_5_s,
        5: await _of.skill_6_s,
        6: await _of.skill_3_s,
    }.get(index, await _of.skill_1_s)


async def get_stars(index: int) -> Image.Image:
    return {
        1: await _of.g_one,
        2: await _of.g_two,
        3: await _of.g_three,
        4: await _of.g_four,
        5: await _of.g_five,
    }.get(index, await _of.g_one)


async def get_rarity(index: int) -> Image.Image:
    return {
        2: await _of.rank_w_b,
        3: await _of.rank_w_a,
        4: await _of.rank_w_s,
    }.get(index, await _of.rank_w_b)

async def get_rank_color(index: int) -> Tuple[int,int,int,int]:
    return {
        2: (7,158,254),
        3: (181,7,254),
        4: (254,181,7)
    }.get(index, (254,181,7))

async def get_core(index: int) -> Image.Image:
    return {
        0: await _of.core_skill_a,
        1: await _of.core_skill_b,
        2: await _of.core_skill_c,
        3: await _of.core_skill_d,
        4: await _of.core_skill_e,
        5: await _of.core_skill_f,
    }.get(index, await _of.core_skill_a)


async def get_cinema(index: int) -> Image.Image:
    return {
        0: await _of.conts_1_lvl,
        1: await _of.conts_2_lvl,
        2: await _of.conts_3_lvl,
        3: await _of.conts_4_lvl,
        4: await _of.conts_5_lvl,
        5: await _of.conts_6_lvl,
    }.get(index, await _of.conts_1_lvl)


class StyleOne:
    def __init__(self, data: Character, player: PlayerData, lang: Translator, art: str = None, color: tuple = None, hide: bool = False):
        self.data = data
        self.player = player
        self.lang = lang
        self.art = art
        self.hide = hide
        
        if color:
            self.color = color
        elif art:
            self.color = None
        else:
            colors = get_color_agent(data.id)
            self.color = colors.mindscape

        _of.set_mapping(1)
        
    async def create_background(self):
        full_background = Image.new("RGBA", (1927,802), (0,0,0,0))
        image_background = Image.new("RGBA",(1927,802), (0,0,0,0))
        text_frame = await _of.text_frame
        background = await _of.background
        self.background = background.convert("RGBA").copy()
        mask = await _of.mask
        shadow = await _of.shadow

        frame_info = await _of.frame_info
        frame_info = frame_info.copy()

        dark_frame_info = await _of.dark_frame_info
        cadr = await _of.cadr
        frame = await _of.frame
        charter_bg = await _of.charter_bg


        if self.art:
            self.art = await pill.get_user_image(self.art)
            user_image = await pill.get_center_size((563,802), self.art)
            if not self.color:
                self.color = await pill.get_colors(user_image.convert("RGBA"), 5, common=True, radius=30, quality=800)
                ll = await pill.light_level(self.color[:3])
                if ll < 45:
                    self.color = await pill.get_light_pixel_color(self.color[:3],up = True)
            image_background.alpha_composite(user_image)
            full_background.paste(image_background,(0,0), mask.convert("L"))
            self.background.alpha_composite(full_background)
        else:
            text_frame = await pill.recolor_image(text_frame, self.color[:3])
            self.background.alpha_composite(charter_bg)
            self.background.alpha_composite(text_frame, (-2,8))
            icon = get_agent_icon(self.data.id)
            user_image = await pill.get_download_img(icon.image, size=(942,946))
            user_image_w = await pill.recolor_image(user_image, (255,255,255))
            user_image_b = await pill.recolor_image(user_image, (0,0,0))
            image_background.alpha_composite(user_image_w, (-191,0))
            image_background.alpha_composite(user_image_b, (-203,0))
            image_background.alpha_composite(user_image, (-196, 0))
            full_background.paste(image_background,(0,0), mask.convert("L"))
            self.background.alpha_composite(full_background)
        
        await self.create_litetal()
        self.background.alpha_composite(shadow, (379,-17))
        
        frame_info = await pill.recolor_image(frame_info.copy(), self.color[:3])
        cadr = await pill.recolor_image(cadr.copy(), self.color[:3]) 

        frame_info.alpha_composite(dark_frame_info)
        frame_info.alpha_composite(cadr)


        self.background.alpha_composite(frame_info, (398,0))
        self.background.alpha_composite(self.literal, (410,399))
        self.background.alpha_composite(frame, (389, 0))

        self.white_color = (255,255,255,255) if await pill.is_white_text_readable(self.color, 120) else (32,32,32,32)

    async def create_name(self):
        self.name = Image.new("RGBA", (491,142), (0,0,0,0))

        name_main = await pill.create_image_with_text(self.data.name, 69, stroke_width=2, stroke_fill= (0,0,0,255), max_width= 492)
        name = await pill.create_image_with_text(self.data.name, 69, max_width= 492)
        name = await pill.recolor_image(name, self.color[:3]) 
        lvl = f"{self.lang.lvl}: {self.data.level}/{self.data.max_level*10}"
        lvl_main = await pill.create_image_with_text(lvl, 50, stroke_width=2, stroke_fill= (0,0,0,255) , max_width= 492)
        lvl = await pill.create_image_with_text(lvl, 50, max_width= 492)
        lvl = await pill.recolor_image(lvl, self.color[:3]) 
        self.name.alpha_composite(name, (13,9))
        self.name.alpha_composite(name_main, (11,5))
        self.name.alpha_composite(lvl, (17,87))
        self.name.alpha_composite(lvl_main, (15,83))

    async def create_skill(self):
        self.skill = Image.new("RGBA", (363,165), (0,0,0,0))
        skill_coont = await _of.skill_count
        font = await pill.get_font(25)
        last_true_index = next((i for i in reversed(range(len(self.data.cinema))) if self.data.cinema[i]), 0)

        position_skill = [
            (0,0),
            (115,0),
            (230,0),
            (48,90),
            (163,90),
            (269,90),
        ]

        for i, key in enumerate(self.data.skills):
            skill_icon = Image.new("RGBA", (85,75), (0,0,0,0))
            count = skill_coont.copy()
            icon = await get_skill_icon(key.index)
            lvl = key.level
            if last_true_index >= 3 and i != 4:
                lvl += 2
            if last_true_index >= 5 and i != 4:
                lvl += 2
                
            d = ImageDraw.Draw(count)
            x = int(font.getlength(str(lvl)) / 2)
            d.text((22 - x, -3), str(lvl), font=font, fill=self.color)
            
            skill_icon.alpha_composite(icon.resize((75,75)))
            skill_icon.alpha_composite(count,(40,49))
            
            self.skill.alpha_composite(skill_icon, position_skill[i])

    async def create_weapon(self):
        self.weapon = Image.new("RGBA", (458,176), (0,0,0,0))
        if not self.data.weapon:
            return
        
        bg = await _of.weapon_background
        icon = await pill.get_download_img(URL_ASSETS + self.data.weapon.icon, (167,167))
        icon_color = await pill.recolor_image(icon, self.color[:3]) 
        icon_w = await pill.recolor_image(icon, (255,255,255))
        stars = await get_stars(self.data.weapon.cons)

        self.weapon.alpha_composite(bg)
        self.weapon.alpha_composite(icon_w, (0,9))
        self.weapon.alpha_composite(icon_color, (9,0))
        self.weapon.alpha_composite(icon, (5,3))
        self.weapon.alpha_composite(stars.resize((117,42)), (90,124))
        
        name_main = await pill.create_image_with_text(self.data.weapon.name, 33, stroke_width=2, stroke_fill= (0,0,0,255), max_width= 309)
        name = await pill.create_image_with_text(self.data.weapon.name, 33, max_width= 309)
        name = await pill.recolor_image(name, self.color[:3]) 
        xyz = 0
        if name_main.size[1] > 60:
            xyz = 20
        self.weapon.alpha_composite(name, (157,32-xyz))
        self.weapon.alpha_composite(name_main, (155,30-xyz))
        
        lvl_bg = await _of.levl
        lvl_bg = lvl_bg.copy()

        font = await pill.get_font(24)
        d = ImageDraw.Draw(lvl_bg)
        text_lvl = f"LVL: {self.data.weapon.level}"
        x = int(font.getlength(text_lvl) / 2)
        d.text((47 - x, 3), text_lvl, font=font, fill=self.color)
        x = int(font.getlength(text_lvl) / 2)
        d.text((43 - x, 0), text_lvl, font=font, fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))
        self.weapon.alpha_composite(lvl_bg, (211,123))

        font = await pill.get_font(22)
        up_bg = await _of.up
        up_bg = up_bg.copy()
        d = ImageDraw.Draw(up_bg)
        text_up = f"R{self.data.weapon.cons}"
        x = int(font.getlength(text_up) / 2)
        d.text((17 - x, 3), text_up, font=font, fill=(37,37,37,255))
        self.weapon.alpha_composite(up_bg, (313,123))


        icon_main = await pill.get_download_img(self.data.weapon.main.icon, size=(30,30))
        icon_sub = await pill.get_download_img(self.data.weapon.main.icon, size=(30,30))
        font = await pill.get_font(27)
        d = ImageDraw.Draw(self.weapon)

        self.weapon.alpha_composite(icon_main, (181,82))
        self.weapon.alpha_composite(icon_sub, (286,82))
        d.text((218, 82), str(self.data.weapon.main.value), font=font, fill=(255,255,255,255))
        formatted_percentage = self.data.weapon.sub.get_value()
        d.text((321, 82), str(formatted_percentage), font=font, fill=(255,255,255,255))

        rarity = await get_rarity(self.data.weapon.rarity)
        self.weapon.alpha_composite(rarity.convert("RGBA").resize((35,35)), (22,18))

    async def create_disc(self, data: Equipment):
        echo_background = Image.new("RGBA", (193,212), (0,0,0,0))
        
        background = Image.new("RGBA", (193,209), (0,0,0,0))
        icon_disc = await pill.get_download_img(URL_ASSETS + data.icon, (152,152))
        color = await pill.get_colors(icon_disc.convert("RGBA"), 15, common=True, radius=5, quality=800)
        frame_background = await _of.frame_background
        frame_background = await pill.recolor_image(frame_background, color[:3])

        background.alpha_composite(icon_disc, (20,0))
        background.alpha_composite(await _of.frame_background_black)
        background.alpha_composite(frame_background)
        background.alpha_composite(await _of.frame_relict)

        lvl_frame = await _of.lvl
        lvl_frame.copy()

        font = await pill.get_font(25)
        d = ImageDraw.Draw(lvl_frame)
        x = int(font.getlength(f"+{data.level}") / 2)
        d.text((26-x, -4), f"+{data.level}", font=font, fill=(255,255,255,255))
        background.alpha_composite(lvl_frame, (130,80))

        stats_frame = await _of.stats
        stats_frame.copy()
        icon_main = await pill.get_download_img(data.main[0].icon, (22,22))
        stats_frame.alpha_composite(icon_main, (8,1))

        value = str(data.main[0].get_value())
        font = await pill.get_font(20)
        d = ImageDraw.Draw(stats_frame)
        x = int(font.getlength(value) / 2)
        d.text((76-x, 0), value, font=font, fill=(255,255,255,255))
        background.alpha_composite(stats_frame, (7,80))

        position = [
            (15,126),
            (101,126),
            (15,162),
            (101,162),
        ]

        rolls_line =  Image.new("RGBA", (11,1), color)
        font = await pill.get_font(18)
        for i, key in enumerate(data.sub):
            sub_bg = Image.new("RGBA", (75,26), (0,0,0,0))
            sub_icon = await pill.get_download_img(key.icon, (22,22))
            sub_bg.alpha_composite(sub_icon)
            value = str(key.get_value())
            d = ImageDraw.Draw(sub_bg)
            d.text((24, 0), value, font=font, fill=(255,255,255,255))
            x = 2
            for _ in range(key.rolls-1):
                sub_bg.alpha_composite(rolls_line, (x, 25))
                x += 15
            background.alpha_composite(sub_bg, position[i])

        
        background_w_b = await _of.frame_wb_background
        echo_background.alpha_composite(background_w_b)
        echo_background.alpha_composite(background.resize((187,201)), (3,11))

        rarity = await get_rarity(data.rarity)
        rank_leve = await _of.rank_leve
        rank_leve = await pill.recolor_image(rank_leve, await get_rank_color(data.rarity))
        echo_background.alpha_composite(rank_leve)
        echo_background.alpha_composite(rarity.copy().convert("RGBA").resize((27,27)), (10,16))
        return echo_background

    async def create_litetal(self):
        self.literal = Image.new("RGBA", (222,391))
        
        position = [
            (171,0),
            (137,68),
            (103,136),
            (69,203),
            (36,269),
            (0,340),
        ]
        for i in range(6):
            icon = await get_core(i)
            icon = icon.resize((51,51))
            if self.data.core_skill-1 >= i:
                icon = await pill.recolor_image(icon, self.color[:3])
            else:
                icon = await pill.recolor_image(icon, (32,32,32))
            self.literal.alpha_composite(icon, position[i])

    async def create_cinema(self):
        self.cinema = Image.new("RGBA", (190,346), (0,0,0,0))
        position = [
            (0,0),
            (28,59),
            (55,117),
            (82,176),
            (110,235),
            (137,293),
        ]
        
        for i in range(6):
            icon = await get_cinema(i)
            if i < self.data.const and self.data.const != 0:
                icon = await pill.recolor_image(icon, (0,0,0))
            else:
                icon = await pill.recolor_image(await _of.conts_0_lvl, (0,0,0))
                
            self.cinema.alpha_composite(icon.resize((53,53)),position[i])

    async def create_stats(self):
        self.stats = Image.new("RGBA", (727,296), (0,0,0,0))
        stats_background = await _of.stats_background
        stats_value = await _of.value
        stats_value = await pill.recolor_image(stats_value, self.color[:3])
        xx = 0
        y = 0
        for i, key in enumerate(self.data.stats):
            bg = stats_background.copy()
            bg_val = stats_value.copy()
            icon = await pill.get_download_img(key.icon, (35,35))
            bg.alpha_composite(icon, (10,14))
            name = await pill.create_image_with_text(key.name, 22, 115)
            bg.alpha_composite(name, (49, int(32 - (name.height /2))))
            
            font = await pill.get_font(22)
            d = ImageDraw.Draw(bg_val)
            text_val = key.get_value()
            x = int(font.getlength(text_val) / 2)
            d.text((45 - x, 0), text_val, font=font, fill= self.white_color)
            bg.alpha_composite(bg_val,(0,57))

            d = ImageDraw.Draw(bg)
            font = await pill.get_font(13)

            add = key.get_value(add = True)
            base = key.get_value(base = True)

            d.text((98, 60), str(base), font=font, fill=(255,255,255,255))
            x = int(font.getlength(f"+{add}"))
            d.text((164 - x, 71), f"+{add}", font=font, fill=self.color)

            self.stats.alpha_composite(bg, (xx,y))

            xx += 180
            if i in [3,7]:
                xx = 0
                y += 102

    async def create_sets(self):
        filtered_data = {
            key: {**value, 'count': 2 if value['count'] == 3 else value['count']}
            for key, value in self.sets.items() if value['count'] != 1
        }
        self.sets = []
        sets_background = await _of.sets_background
        sets_collor = await _of.sets_collor
        for key in filtered_data:
            bg = sets_background.copy()
            icon_disc = await pill.get_download_img(URL_ASSETS + filtered_data[key]["icon"], (152,152))
            color = await pill.get_colors(icon_disc.convert("RGBA"), 15, common=True, radius=5, quality=800)
            bg_color = await pill.recolor_image(sets_collor, color[:3])
            bg.alpha_composite(bg_color)
            bg.alpha_composite(await _of.sets_count)
            font = await pill.get_font(27)
            d = ImageDraw.Draw(bg)
            d.text((30, 15),f"{filtered_data[key]['count']}X", font=font, fill=(255,255,255,255))
            font = await pill.get_font(24)
            white_color = (255,255,255,255) if pill.is_white_visible(color) else (32,32,32,32)
            d.text((82, 18),filtered_data[key]['name'], font=font, fill=white_color)

            self.sets.append(bg)

    async def create_nickname(self):
        self.nickname = Image.new("RGBA", (400,72), (0,0,0,0))
        
        name = await pill.create_image_with_text(self.player.profile.nickname, 32, stroke_width=1, stroke_fill= (0,0,0,255), max_width= 250)
        name_c = await pill.recolor_image(name, self.color[:3])

        uid = f"UID: {self.player.profile.uid}"
        if self.hide:
            uid = f"UID: Hide"
        uid = await pill.create_image_with_text(uid, 25,stroke_width=1, stroke_fill= (0,0,0,255), max_width= 250)
        uid_c = await pill.recolor_image(uid, self.color[:3])

        self.nickname.alpha_composite(name_c, (6,6))
        #self.nickname.alpha_composite(name_b, (2,6))
        self.nickname.alpha_composite(name, (4,4))

        self.nickname.alpha_composite(uid_c, (5,40))
        #self.nickname.alpha_composite(uid_b, (2,40))
        self.nickname.alpha_composite(uid, (4,38))

    async def build(self):
        self.background.alpha_composite(self.name, (559,16))
        self.background.alpha_composite(self.skill, (622,184))
        self.background.alpha_composite(self.weapon, (663,395))
        self.background.alpha_composite(self.cinema, (434,25))
        self.background.alpha_composite(self.stats, (1165,3))
        self.background.alpha_composite(self.nickname, (0,724))
        x = 1194
        y = 323
        for _, key in enumerate(self.disc):
            self.background.alpha_composite(key, (x,y))
            x += 243
            if _ == 2:
                x = 1194
                y = 555

        position = {
            1: [(102,71)], 
            2: [(57,18), (146,95)],
            3: [(60,0), (203,69), (0,126)],
        }.get(len(self.sets))

        sets = Image.new("RGBA", (547,195), (0,0,0,0))
        for i, key in enumerate(self.sets):
            sets.alpha_composite(key, position[i])
            pass
        
        self.background.alpha_composite(sets, (541,586))

    async def start(self) -> ZZZCard:
        await self.create_background()
        await self.create_litetal()
        task = [
            self.create_name(),
            self.create_skill(),
            self.create_weapon(),
            self.create_cinema(),
            self.create_stats(),
            self.create_nickname(),
        ]

        await asyncio.gather(*task)

        self.disc = []
        self.sets = {}
        for key in self.data.equippe:
            self.disc.append(await self.create_disc(key.equipment))
            if not key.equipment.sets.id in self.sets:
                self.sets[key.equipment.sets.id] = {"count": 1, "name": key.equipment.sets.name, "icon": key.equipment.sets.icon}
            else:
                self.sets[key.equipment.sets.id]["count"] += 1

        await self.create_sets()

        await self.build()
        
        return ZZZCard(
            id = self.data.id,
            name = self.data.name,
            color = self.color,
            icon = self.data.icon.circle_icon,
            card = self.background
        )