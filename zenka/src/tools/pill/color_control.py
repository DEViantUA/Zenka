# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import colorsys
from PIL import Image
from .. import cache 

_caches = cache.Cache.get_cache()

def is_white_visible(background_color: tuple, threshold: float = 4.5) -> bool:
    def relative_luminance(rgb):
        def transform(c):
            c /= 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = rgb
        return 0.2126 * transform(r) + 0.7152 * transform(g) + 0.0722 * transform(b)

    # Яркость белого цвета
    luminance_white = relative_luminance((255, 255, 255))
    # Яркость фона
    luminance_bg = relative_luminance(background_color)
    
    # Рассчет коэффициента контраста
    contrast_ratio = (luminance_white + 0.05) / (luminance_bg + 0.05)

    return contrast_ratio >= threshold
async def apply_opacity(image, opacity=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image

def brightness(color):
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

async def light_levell(pixel_color: tuple):
    cache_key = pixel_color
    if cache_key in _caches:
        return _caches[cache_key]

    luminance = brightness(pixel_color)
    _caches[cache_key] = luminance
    return luminance

async def is_white_text_readable(pixel_color: tuple, threshold=200):
    bg_brightness = await light_levell(pixel_color)
    white_brightness = 255

    contrast = abs(white_brightness - bg_brightness)
    return contrast >= threshold 


async def light_level(pixel_color: tuple):
    cache_key = pixel_color
    if cache_key in _caches:
        return _caches[cache_key]
    
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3])) 
    _caches[cache_key] = l
    return l

def color_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

async def replace_color(image, old_color, new_color, radius=100):
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            current_color = pixels[x, y][:3]
            if color_distance(current_color, old_color) <= radius:
                pixels[x, y] = (*new_color, pixels[x, y][3])
    
    return image


async def recolor_image(image, target_color, light = False) -> Image.Image:
    if light:
        ll = await light_level(target_color)
        if ll < 45:
            target_color = await get_light_pixel_color(target_color,up = True)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    image = image.copy()

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if a != 0:
                pixels[i, j] = target_color + (a,)
    if light:
        return image, target_color
    return image

async def get_light_pixel_color(pixel_color, up = False):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    if up:
        l = min(max(0.6, l), 0.9)
    else:
        l = min(max(0.3, l), 0.8)
    return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
  
async def _get_dark_pixel_color(pixel_color):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    l = min(max(0.8, l), 0.2)
    a = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    
    return  a




