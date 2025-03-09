import asyncio
from zenka import zenka, ZZZError, ZZZProfileCard


async def main(uid: int) -> ZZZProfileCard:
    try:
        async with zenka.Client() as client:
            data = await client.profile(uid)
        print(data)
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")

    return data

uid = 1500004451

asyncio.run(main(uid))
