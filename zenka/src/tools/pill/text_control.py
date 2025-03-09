# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import json
from PIL import ImageFont,Image,ImageDraw
from .. import cache, git

_caches = cache.Cache.get_cache()

async def get_font(size):
    return ImageFont.truetype(git.font, size)

async def get_text_size_frame(text,font_size,frame_width):    
    font = await get_font(font_size)

    while font.getlength(text) > frame_width:
        font_size -= 1
        font = await get_font(font_size)
    return font,font.getlength(text)


async def create_image_with_text(text: str, font_size: int, max_width: int =336, color: tuple =(255, 255, 255, 255), stroke_width: int = 0, stroke_fill: tuple = None, alg="Left"):
    cache_key = json.dumps((text, font_size, max_width, color, alg), sort_keys=True)
    if cache_key in _caches:
        return _caches[cache_key]
    
    font = await get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    img = Image.new('RGBA', (min(width, max_width) + 10, height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color, stroke_width = stroke_width, stroke_fill= stroke_fill)
        y_text += text_height + 5
        
    _caches[cache_key] = img
    
    return img