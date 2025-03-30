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


class StyleTwo:
    def __init__(self, data: Character, player: PlayerData, lang: Translator, art: str = None, color: tuple = None, hide: bool = False, crop: int = 0):
        self.data = data
        self.player = player
        self.lang = lang
        self.art = art
        self.hide = hide
        self.crop = crop
        
        if color:
            self.color = color
        elif art:
            self.color = None
        else:
            colors = get_color_agent(data.id)
            self.color = colors.mindscape

        _of.set_mapping(3)


    async def create_background(self):
        background = Image.new("RGBA", (457,809), (0,0,0,0))
        image_background = Image.new("RGBA", (457,809), (0,0,0,0))
        text_frame = await _of.text_frame
        background = await _of.background
        mask = await _of.background_mask
        self.charter_bg = await _of.background
        self.charter_bg = self.charter_bg.convert("RGBA").copy()
        if self.art:
            self.art = await pill.get_user_image(self.art)
            user_image = await pill.get_center_size((502,809), self.art)
            if not self.color:
                self.color = await pill.get_colors(user_image.convert("RGBA"), 5, common=True, radius=30, quality=800)
                ll = await pill.light_level(self.color[:3])
                if ll < 45:
                    self.color = await pill.get_light_pixel_color(self.color[:3],up = True)
            image_background.alpha_composite(user_image,(-22,0))

            background.paste(image_background,(0,0), mask.convert("L"))
            self.charter_bg.alpha_composite(background)
        else:
            text_frame = await pill.recolor_image(text_frame, self.color[:3])
            self.charter_bg.alpha_composite(text_frame)
            icon = get_agent_icon(self.data.id)
            user_image = await pill.get_download_img(icon.image, size=(843,879))
            user_image_w = await pill.recolor_image(user_image, (255,255,255))
            user_image_b = await pill.recolor_image(user_image, (0,0,0))

            image_background.alpha_composite(user_image_w, (-186,0))
            image_background.alpha_composite(user_image_b, (-198,0))
            image_background.alpha_composite(user_image, (-193, 0))
            background.paste(image_background,(0,0), mask.convert("L"))
            self.charter_bg.alpha_composite(background)
        
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
        self.name = self.name.resize((191,57))
    
    async def create_skill(self):
        skill = await _of.skill_bg
        self.skill = skill.copy()
        skill_coont = await _of.skill_lvl
        skill_frame = await _of.skill_frame
        skill_frame = await pill.recolor_image(skill_frame, self.color[:3])
        font = await pill.get_font(18)
        last_true_index = next((i for i in reversed(range(len(self.data.cinema))) if self.data.cinema[i]), 0)

        position_skill = [
            (8,0),
            (79,0),
            (150,0),
            (221,0),
            (292,0),
            (363,0),
        ]

        for i, key in enumerate(self.data.skills):
            skill_icon = Image.new("RGBA", (63,70), (0,0,0,0))
            count = skill_coont.copy()
            icon = await get_skill_icon(key.index)
            lvl = key.level
            if last_true_index >= 3 and i != 4:
                lvl += 2
            if last_true_index >= 5 and i != 4:
                lvl += 2
                
            d = ImageDraw.Draw(count)
            x = int(font.getlength(str(lvl)) / 2)
            d.text((13 - x, 0), str(lvl), font=font, fill=self.color)
            
            skill_icon.alpha_composite(icon.resize((59,59)), (2,8))
            skill_icon.alpha_composite(skill_frame)
            skill_icon.alpha_composite(count,(19,0))
            
            self.skill.alpha_composite(skill_icon, position_skill[i])

    async def create_info(self):
        info = await _of.info_bg
        self.info = info.copy()

        icon_literal = None
        for i in range(6):
            icon = await get_core(i)
            icon = icon.resize((51,51))
            if self.data.core_skill-1 >= i:
                icon_literal = await pill.recolor_image(icon, self.color[:3])
        
        if not icon_literal:
            icon = await get_core(0)
            icon_literal = await pill.recolor_image(icon, (103,103,103))

        self.info.alpha_composite(icon_literal.resize((42,42)), (3,97))
        
        icon_const = await pill.recolor_image(await _of.conts_0_lvl, self.color[:3])
        for i in range(6):
            icon = await get_cinema(i)
            if i < self.data.const and self.data.const != 0:
                icon_const = await pill.recolor_image(icon, self.color[:3])

        self.info.alpha_composite(icon_const.resize((42,42)), (3,147))

        element_icon = await pill.get_download_img(self.data.element.icon, size = (42,42))
        self.info.alpha_composite(element_icon, (3,2))
        fraction_icon = await pill.get_download_img(self.data.profession.icon, size = (42,42))
        self.info.alpha_composite(fraction_icon, (3,48))

    async def create_weapon(self):
        weapon = await _of.weapon_bg
        self.weapon = weapon.copy()
        if not self.data.weapon:
            return

        icon = await pill.get_download_img(URL_ASSETS + self.data.weapon.icon, (143,143))
        icon_color = await pill.recolor_image(icon, self.color[:3]) 
        icon_w = await pill.recolor_image(icon, (255,255,255))

        self.weapon.alpha_composite(icon_w, (168,9))
        self.weapon.alpha_composite(icon_color, (176,0))
        self.weapon.alpha_composite(icon, (172,3))

        rarity = await get_rarity(self.data.weapon.rarity)
        self.weapon.alpha_composite(rarity.convert("RGBA").resize((35,35)), (269,100))

        lvl_bg = await _of.levl
        lvl_bg = lvl_bg.copy()

        font = await pill.get_font(24)
        d = ImageDraw.Draw(lvl_bg)
        text_lvl = f"LVL: {self.data.weapon.level}"
        x = int(font.getlength(text_lvl) / 2)
        d.text((47 - x, 3), text_lvl, font=font, fill=self.color)
        x = int(font.getlength(text_lvl) / 2)
        d.text((43 - x, 0), text_lvl, font=font, fill=(255,255,255,255), stroke_width=2, stroke_fill=(0,0,0,255))
        self.weapon.alpha_composite(lvl_bg, (315,76))

        font = await pill.get_font(22)
        up_bg = await _of.up
        up_bg = up_bg.copy()
        d = ImageDraw.Draw(up_bg)
        text_up = f"R{self.data.weapon.cons}"
        x = int(font.getlength(text_up) / 2)
        d.text((17 - x, 3), text_up, font=font, fill=(37,37,37,255))
        self.weapon.alpha_composite(up_bg, (411,76))


        icon_main = await pill.get_download_img(self.data.weapon.main.icon, size=(30,30))
        icon_sub = await pill.get_download_img(self.data.weapon.sub.icon, size=(30,30))
        font = await pill.get_font(23)
        d = ImageDraw.Draw(self.weapon)

        self.weapon.alpha_composite(icon_main, (315,41))
        self.weapon.alpha_composite(icon_sub, (407,41))

        d.text((349, 39), str(self.data.weapon.main.value), font=font, fill=(255,255,255,255))
        formatted_percentage = self.data.weapon.sub.get_value()
        d.text((442, 39), str(formatted_percentage), font=font, fill=(255,255,255,255))


        name_main = await pill.create_image_with_text(self.data.weapon.name, 25, stroke_width=2, stroke_fill= (0,0,0,255), max_width= 159)
        name = await pill.create_image_with_text(self.data.weapon.name, 25, max_width= 159) 
        name = await pill.recolor_image(name, self.color[:3]) 
        xyz = 63
        x = 14
        if name_main.size[1] > 60:
            xyz = 42
            x = 40
        self.weapon.alpha_composite(name, (x,xyz))
        self.weapon.alpha_composite(name_main, (x-2,xyz-2))

    async def create_stats(self):
        stats = await _of.stats_bg
        self.stats = stats.copy()
        position_text_x = 158
        position_text_y = 13

        position_icon_x = 68
        position_icon_y = 12

        line = Image.new("RGBA", (2,204), self.color)
        self.stats.alpha_composite(line, (164,13))

        font = await pill.get_font(20)
        d = ImageDraw.Draw(self.stats)
        
        for i, key in enumerate(self.data.stats):
            icon = await pill.get_download_img(key.icon, (25,25))
            self.stats.alpha_composite(icon, (position_icon_x,position_icon_y))
            text_val = key.get_value()
            x = int(font.getlength(text_val))
            d.text((position_text_x - x, position_text_y), text_val, font=font, fill= (255,255,255,255))

            position_icon_y += 36
            position_text_y += 36

            if i == 5:
                position_text_x = 261
                position_text_y = 13

                position_icon_x = 171
                position_icon_y = 12

    async def create_disc(self, data: Equipment):
        echo_background = Image.new("RGBA", (710,85), (0,0,0,0))
        
        background_disk = await _of.disk_bg
        background_disk = background_disk.copy()
        icon_disc = await pill.get_download_img(URL_ASSETS + data.icon, (74,74))
        color = await pill.get_colors(icon_disc.convert("RGBA"), 15, common=True, radius=5, quality=800)

        background_disk.alpha_composite(icon_disc, (5,5))
        rarity = await get_rarity(data.rarity)
        rank_leve = await _of.rank_leve
        color_rank = await get_rank_color(data.rarity)
        rank_leve = await pill.recolor_image(rank_leve,color_rank)
        background_disk.alpha_composite(rank_leve.resize((93,100)), (1,1))
        background_disk.alpha_composite(rarity.copy().convert("RGBA").resize((22,22)), (0,5))

        lvl_bg = await _of.lvl_disk
        lvl_bg = lvl_bg.copy()
        lvl_frame = await _of.frame_disk_lvl
        lvl_frame = await pill.recolor_image(lvl_frame,color_rank)
        font = await pill.get_font(16)
        d = ImageDraw.Draw(lvl_bg)
        x = int(font.getlength(f"+{data.level}") / 2)
        d.text((20-x, 0), f"+{data.level}", font=font, fill=self.color)
        lvl_bg.alpha_composite(lvl_frame)
        background_disk.alpha_composite(lvl_bg, (14,61))

        echo_background.alpha_composite(background_disk, (0,0))


        stats_frame = Image.new("RGBA", (224,71),(0,0,0,0))

        main_bg_disk_stat = await _of.main_bg_disk_stat
        main_bg_disk_stat = main_bg_disk_stat.copy()
        main_bg_disk_stat = await pill.recolor_image(main_bg_disk_stat, color[:3])
        texture_disk_main = await _of.texture_disk_main
        main_bg_disk_stat.alpha_composite(texture_disk_main)

        sub_bg_disk_stat = await _of.sub_bg_disk_stat
        sub_bg_disk_stat = sub_bg_disk_stat.copy()

        stats_frame.alpha_composite(sub_bg_disk_stat)
        stats_frame.alpha_composite(main_bg_disk_stat)

        d = ImageDraw.Draw(stats_frame)
        icon_main = await pill.get_download_img(data.main[0].icon, (25,25))
        color_main = (255,255,255,255) if pill.is_white_visible(color[:3]) else (26,26,26,255)
        icon_main = await pill.recolor_image(icon_main, color_main[:3])

        stats_frame.alpha_composite(icon_main,(54,11))
        value = str(data.main[0].get_value())
        font = await pill.get_font(21)
        x = int(font.getlength(value))
        d.text((79-x, 43), value, font=font, fill=color_main)


        position = [
            (89,4),
            (103,37),
            (154,4),
            (167,37),
        ]
        ll = await pill.light_level(color[:3])
        if ll < 45:
            color = await pill.get_light_pixel_color(color[:3],up = True)

        rolls_line =  Image.new("RGBA", (7,2), color)
        font = await pill.get_font(14)
        for i, key in enumerate(data.sub):
            sub_bg = Image.new("RGBA", (55,21), (0,0,0,0))
            sub_icon = await pill.get_download_img(key.icon, (17,17))
            sub_bg.alpha_composite(sub_icon)
            value = str(key.get_value())
            d = ImageDraw.Draw(sub_bg)
            d.text((21, 0), value, font=font, fill=(255,255,255,255))
            x = 2
            for _ in range(key.rolls-1):
                sub_bg.alpha_composite(rolls_line, (x, 19))
                x += 15
            stats_frame.alpha_composite(sub_bg, position[i])

        echo_background.alpha_composite(stats_frame, (486,7))

        return echo_background


    async def build(self):
        self.background = Image.new("RGBA", (710,923), (0,0,0,0))

        y = 57
        for key in self.disc:
            self.background.alpha_composite(key, (0,y))
            y += 86
            
        self.background.alpha_composite(self.skill,(61,0))
        self.background.alpha_composite(self.info,(0,578))
        self.background.alpha_composite(self.stats,(443,573))
        self.background.alpha_composite(self.charter_bg,(47,44))
        self.background.alpha_composite(self.name, (56,741))
        self.background.alpha_composite(self.weapon, (23,772))

    
    async def start(self) -> ZZZCard:
        await self.create_background()

        task = [
            self.create_name(),
            self.create_skill(),
            self.create_info(),
            self.create_weapon(),
            self.create_stats(),
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

        await self.build()

        return ZZZCard(
            id = self.data.id,
            name = self.data.name,
            color = self.color,
            icon = self.data.icon.circle_icon,
            card = self.background,
        )
        