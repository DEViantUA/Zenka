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
