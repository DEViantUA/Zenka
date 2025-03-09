import random
from PIL import Image, ImageDraw
from ..model.base import Translator
from ..model.api import Character, PlayerData
from ..tools.git import ImageCache
from ..tools import pill
from ..model.generator import ZZZProfileCard
from ..model.base import URL_ASSETS, DEFAULT_AVATAR
from ..model.assets import get_agent_icon, hex_to_rgba

_of = ImageCache()

class StyleOneProfile:
    def __init__(self, data: Character, player: PlayerData, lang: Translator, color: tuple = None, hide: bool = False):
        self.data = data
        self.player = player
        self.lang = lang        
        self.hide = hide
        if color:
            self.color = color
        else:
            if player.profile.title:
                self.color = hex_to_rgba(player.profile.title.color.accent)
            else:
                self.color = (235, 174, 89, 255)

        _of.set_mapping(2)

    async def create_medal(self):
        self.medal = []
        font = await pill.get_font(23)
        medal_icon = await _of.medal
        for key in self.player.medal_list:
            medal = medal_icon.copy()
            icon = await pill.get_download_img(URL_ASSETS + key.icon, (84,73))
            medal.alpha_composite(icon)
            d = ImageDraw.Draw(medal)
            x = int(font.getlength(str(key.value)) / 2)
            d.text((107-x, 20), str(key.value), font=font, fill=self.color)

            self.medal.append(medal)

    async def create_background(self):
        self.background = await _of.main_background
        self.background = self.background.copy()
        background = await pill.recolor_image(await _of.background, self.color[:3])

        self.background.alpha_composite(background)
        self.background.alpha_composite(await _of.cinema, (160,296))
        self.background.alpha_composite(await _of.cinema_frame, (160,296))
        self.background.alpha_composite(await _of.texture_avatar, (37,81))

        frame_icon = await _of.frame_icon
        frame_icon = await pill.recolor_image(frame_icon, self.color[:3])
        
        if self.player.profile.icon:
            icon = await pill.get_download_img(URL_ASSETS + self.player.profile.icon, (179,179))
        else:
            icon = await pill.get_download_img(DEFAULT_AVATAR, (179,179))
        self.background.alpha_composite(icon, (58,72))
        self.background.alpha_composite(frame_icon, (56,71))
        self.background.alpha_composite(await _of.frame_avatar, (198,93))

        level = await _of.lvl_b
        lvl_c = await _of.lvl_c
        lvl_c = await pill.recolor_image(lvl_c, self.color[:3])
        level = level.copy()
        level.alpha_composite(await _of.lvl_w)
        level.alpha_composite(lvl_c)
        
        font = await pill.get_font(20)
        d = ImageDraw.Draw(level)
        text_lvl = f"LVL: {self.player.profile.level}"
        x = int(font.getlength(text_lvl) / 2)
        d.text((40 - x, 10), text_lvl, font=font, fill=(33,33,33,255))

        uid_c = await _of.uid_c
        uid_c = await pill.recolor_image(uid_c, self.color[:3])
        uid = await _of.uid_b
        uid_c.alpha_composite(await _of.uid_w)
        uid_c.alpha_composite(uid)

        d = ImageDraw.Draw(uid_c)
        text_uid = f"Agent: {self.player.profile.uid}"
        if self.hide:
            text_uid = f"Agent: Hide"
        x = int(font.getlength(text_uid) / 2)
        d.text((118 - x, 10), text_uid, font=font, fill=self.color)

        self.background.alpha_composite(level, (42,64))
        self.background.alpha_composite(uid_c, (215,32))

        medal_x = 592
        for key in self.medal:
            self.background.alpha_composite(key, (medal_x,95))
            medal_x += 154


        font = await pill.get_font(25)
        d = ImageDraw.Draw(self.background)
        text_desc = self.player.desc
        d.text((274, 200), text_desc, font=font, fill=self.color)

        font = await pill.get_font(35)
        d.text((263, 89), self.player.profile.nickname, font=font, fill=(0,0,0,255))
        d.text((265, 87), self.player.profile.nickname, font=font, fill=(255,255,255,255))

        line = Image.new("RGBA", (1,99), (0,0,0,255))
        self.background.alpha_composite(line, (569,85))
        if self.player.profile.title:
            title = await pill.create_image_with_text(self.player.profile.title.name, 25, 292, (30,30,30,255))
            self.background.alpha_composite(title, (265, int(162 - (title.height/2))))

    async def create_character(self):
        active_position = [
            (-5,134), (40,306), (85,476),
            (208,-36), (253,134), (298,306),
            (474,-36), (519,134), (564,306),
            (744,-36), (786,134), (834,306),
        ]

        mask = await _of.mask
        font = await pill.get_font(23)
        cards = []
        cards_no_lvl = []

        for key in self.player.characters:
            charter_icon = Image.new("RGBA", (143,179), (0,0,0,0))
            charter_icon_mask = Image.new("RGBA", (143,179), (0,0,0,0))

            icon = get_agent_icon(key.id)
            icon = await pill.get_download_img(icon.image, (524,524))

            charter_icon_mask.alpha_composite(icon, (-177,-53))
            charter_icon_mask.alpha_composite(await _of.shadow_charter)
            charter_icon.paste(charter_icon_mask, (0,0), mask.convert("L"))
            cards_no_lvl.append(charter_icon.copy())


            d = ImageDraw.Draw(charter_icon)
            lvl = f"LVL: {key.level}"
            d.text((36, 130), lvl, font=font, fill=(0,0,0,255))
            d.text((38, 130), lvl, font=font, fill=(255,255,255,255))

            cards.append(charter_icon)

        self.charter_icon_total = Image.new("RGBA", (914,622), (0,0,0,0))

        use_position = [
            (-51,-36), (-5,134), (40,306), (85,476),
            (208,-36), (253,134), (298,306), (343,476),
            (474,-36), (519,134), (564,306), (609,476), 
            (744,-36), (786,134), (834,306), (879,476),
        ]
        for key in cards:
            position = random.choice(active_position)
            self.charter_icon_total.alpha_composite(key, position)
            active_position.remove(position)
            use_position.remove(position)

        for position in use_position:
            card = random.choice(cards_no_lvl)
            card = card.convert("LA").convert("RGBA")
            card = await pill.apply_opacity(card, 0.2)
            self.charter_icon_total.alpha_composite(card, position)

    async def start(self) -> ZZZProfileCard:
        await self.create_medal()
        await self.create_background()
        await self.create_character()
        self.background.alpha_composite(self.charter_icon_total, (160,296))

        return ZZZProfileCard(
            color = self.color,
            card = self.background
        )