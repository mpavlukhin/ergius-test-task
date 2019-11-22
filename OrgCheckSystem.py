import json

from Rules.RulesEngine import RulesEngine
from Server.MockedServer import MockedServer


class OrgCheckSystem:
    def __init__(self, *args, **kwargs):
        self.Server = MockedServer()
        self.RulesEngine = RulesEngine()

    async def check(self):
        org_info = await self.Server.get_org_info()
        cond = await self.Server.get_cond()

        org_info_dict = json.loads(org_info)
        cond_dict = json.loads(cond)

        check_result = (
            await self.RulesEngine.apply_rules(org_info_dict, cond_dict)
        )
        return check_result
