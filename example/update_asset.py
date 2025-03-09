import asyncio
from zenka import zenka, ZZZError

async def main():
    try:
        async with zenka.Client() as client:
            await client.update_asset()
    except ZZZError as e:
        print(f"Code:{e.code} Message: {e.text}")

asyncio.run(main())
