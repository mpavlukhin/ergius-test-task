from Common.common import nested_get


class RulesEngine:
    def __init__(self, *args, **kwargs) -> None:
        pass

    async def apply_rules(self, org_info: dict, condition: dict) -> dict:
        rules = condition.keys()
        for rule in rules:
            result_dict = await self.__apply_rule(org_info, condition[rule])
            if result_dict.get('type', None) == 'result':
                return result_dict
            elif result_dict.get('type', None) == 'rule':
                continue

    def __get_org_field(self, org_info: dict, if_statement_dict: dict):
        field_key = if_statement_dict.get('field', '').split('.')
        field = nested_get(org_info, field_key)
        return field

    def __range_rule_handler(
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

    def __comparison_rule_handler(
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

    def __if_statement_handler(self, org_info: dict, if_statement_dict: dict):
        if if_statement_dict.get('cond', None) == 'range':
            return self.__range_rule_handler(org_info, if_statement_dict)

        elif if_statement_dict.get('cond', None) in [
            'less_then', 'greater_then',
            'less_then_on_equal_to', 'greater_then_on_equal_to',
            'equal', 'not_equal'
        ]:
            return self.__comparison_rule_handler(org_info, if_statement_dict)

    async def __apply_rule(self, org_info: dict, rule: dict) -> dict:
        if_statement_dict = rule.get('if', {})
        field = self.__get_org_field(org_info, if_statement_dict)

        if field is not None:
            if_check = self.__if_statement_handler(org_info, if_statement_dict)

            if if_check:
                then_statement_dict = rule.get('then', {})
                return then_statement_dict

            else:
                else_statement_dict = rule.get('else', {})
                return else_statement_dict

        else:
            return rule.get('not_found', {})
