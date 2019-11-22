import aiohttp
import asyncio


from OrgCheckSystem import OrgCheckSystem


async def main():
    async with aiohttp.ClientSession() as session:
        org_system_system = OrgCheckSystem()
        await org_system_system.check()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())