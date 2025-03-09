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
