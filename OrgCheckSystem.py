import json

from Server.MockedServer import MockedServer


class OrgCheckSystem:
    def __init__(self, *args, **kwargs):
        self.Server = MockedServer()
        self.RulesEngine = None

    async def check(self):
        org_info = await self.Server.get_org_info()
        cond = await self.Server.get_cond()

        org_info_dict = json.loads(org_info)
        cond_dict = json.loads(cond)

        print(org_info_dict, cond_dict, sep='\n')
