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
