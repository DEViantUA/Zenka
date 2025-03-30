import asyncio
from zenka import zenka, ZZZError, CacheConfig, Lang

async def main(uid: int) -> zenka.ZenkaGenerator:
    try:
        async with zenka.Client() as client:
            data = await client.teams(uid)
            await data.build([1091,1381,1171,1251], True)
        print(data)
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")
        return

    return data

uid = 1500001997

asyncio.run(main(uid))
