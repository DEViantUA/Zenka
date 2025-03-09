import asyncio
from zenka import zenka, ZZZError, CacheConfig, Lang

config = zenka.Config(
    font = None, #str - Path You font
    save = False, #bool - Auto Save Cards
    asset_save = False, #bool - Save Assets
    hide_uid = Falde, #bool - Hide UID
    cache = CacheConfig(150, 300), #CacheConfig - Setting Cash
    proxy = None, #str - proxy IP
    color = {"1151": (255, 10, 55, 255)} #dict - set user color to character
)

character_id = [1151, "1121"]
character_art = {"1121": "https://raw.githubusercontent.com/DEViantUA/Zenka/refs/heads/main/readme/test_img.webp"}

async def main(uid: int) -> zenka.ZenkaGenerator:
    try:
        async with zenka.Client(lang = Lang.EN, config = config,
                                character_art = character_art,
                                character_id = character_id
                                ) as client:
            data = await client.card(uid)
        print(data)
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")

    return data

uid = 1500004451

asyncio.run(main(uid))
