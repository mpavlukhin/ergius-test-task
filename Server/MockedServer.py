import asyncio
import os
import random

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
ORG_FILE_PATH = os.path.join(SCRIPT_PATH, 'data', 'organization.json')
COND_FILE_PATH = os.path.join(SCRIPT_PATH, 'data', 'condition.json')


class MockedServer:
    def __init__(
            self,
            org_file_path: str = ORG_FILE_PATH,
            cond_file_path: str = COND_FILE_PATH,
            *args,
            **kwargs,
    ) -> None:
        self.org_file_path = org_file_path
        self.cond_file_path = cond_file_path

    async def get_org_info(self) -> bytes:
        await asyncio.sleep(random.uniform(0.1, 1))
        return open(self.org_file_path, "rb").read()

    async def get_cond(self) -> bytes:
        await asyncio.sleep(random.uniform(0.1, 1))
        return open(self.cond_file_path, "rb").read()
