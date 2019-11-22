from Common.common import nested_get


class RulesEngine:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __get_org_field(self, org_info: dict, if_statement_dict: dict):
        field_key = if_statement_dict['field'].split('.')
        field = nested_get(org_info, field_key)
        return field

    def range_rule_handler(
            self,
            org_info: dict,
            if_statement_dict: dict,
    ) -> bool:
        min_ = if_statement_dict['min']
        max_ = if_statement_dict['max']

        field = self.__get_org_field(org_info, if_statement_dict)

        if min_ <= field <= max_:
            return True

        return False

    def comparison_rule_handler(
            self,
            org_info: dict,
            if_statement_dict: dict,
    ) -> bool:
        field = self.__get_org_field(org_info, if_statement_dict)
        value = if_statement_dict['value']

        if if_statement_dict['cond'] == 'less_then':
            return field < value
        elif if_statement_dict['cond'] == 'greater_then':
            return field > value
        elif if_statement_dict['cond'] == 'less_then_on_equal_to':
            return field <= value
        elif if_statement_dict['cond'] == 'greater_then_on_equal_to':
            return field >= value
        elif if_statement_dict['cond'] == 'equal':
            return field == value
        else:
            return field != value

    def if_statement_handler(self, org_info: dict, if_statement_dict: dict):
        if if_statement_dict['cond'] == 'range':
            return self.range_rule_handler(org_info, if_statement_dict)

        elif if_statement_dict['cond'] in [
            'less_then', 'greater_then',
            'less_then_on_equal_to', 'greater_then_on_equal_to',
            'equal', 'not_equal'
        ]:
            return self.comparison_rule_handler(org_info, if_statement_dict)

    async def apply_rule(self, org_info: dict, rule: dict) -> dict:
        if_statement_dict = rule.get('if', {})
        field = self.__get_org_field(org_info, if_statement_dict)

        if field is not None:
            if_check = self.if_statement_handler(org_info, if_statement_dict)

            if if_check:
                then_statement_dict = rule.get('then', {})
                return then_statement_dict

            else:
                else_statement_dict = rule.get('else', {})
                return else_statement_dict

        else:
            return rule.get('not_found', {})

    async def apply_rules(self, org_info: dict, condition: dict) -> dict:
        rules = condition.keys()
        for rule in rules:
            result_dict = await self.apply_rule(org_info, condition[rule])
            if result_dict.get('type', None) == 'result':
                return result_dict
            elif result_dict.get('type', None) == 'rule':
                continue
