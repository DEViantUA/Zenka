<p align="center">
 <img src="https://raw.githubusercontent.com/DEViantUA/Zenka/refs/heads/main/readme/banner.png" alt="Баннер"/>
</p>

____

## Zenka
Python module for processing EnkaNetwork API and creating profile cards, character <br><br>
:white_medium_square: [Documentation](https://github.com/DEViantUA/EnkaCard/wiki)<br>
:white_medium_square: [Telegram](https://t.me/enkacardchat)<br>
:white_medium_square: [Generation results](https://github.com/DEViantUA/EnkaCard/wiki/Resultate)<br>



## Installation:
```
pip install zenka
```

## Launch:
``` python
import asyncio
from zenka import zenka, ZZZError


async def main(uid: int) -> zenka.ZenkaGenerator:
    try:
        async with zenka.Client() as client:
            data = await client.card(uid)
        print(data)
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")

    return data

uid = 1500004451

asyncio.run(main(uid))

```

**More Example: [EXAMPLE](https://github.com/DEViantUA/Zenka/tree/main/example)**


## Use API:

``` python
import asyncio
from zenka import zenka, ZZZError, ZenkaApi


async def main(uid: int) -> ZenkaApi:
    try:
        async with zenka.Client() as client:
            data = await client.get_api(uid)
        print(data)
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")

    return data

uid = 1500004451

asyncio.run(main(uid))
```


## Languages Supported
| Languege    |  Code   | Enume        | Languege    |  Code   | Enume        | Languege    |  Code   | Enume        |
|-------------|---------|-------------|-------------|---------|-------------|-------------|---------|-------------|
|  English    |     en  | Lang.EN      |  русский    |     ru  | Lang.RU      |  Chinese    |    chs  | Lang.CN      |
|  Tiếng Việt |     vi  | Lang.VI      |  ไทย        |     th  | Lang.TH      |  Taiwan     |    cht  | Lang.CHT     |
|  português  |     pt  | Lang.PT      | 한국어      |     kr  | Lang.KR      |  deutsch    |     de  | Lang.DE      |
|  日本語      |     jp  | Lang.JP      | 中文        |     zh  | Lang.CN      |  español    |     es  | Lang.ES      |
|  中文        |     zh  | Lang.CN      | Indonesian |     id  | Lang.ID      |  français   |     fr  | Lang.FR      |


