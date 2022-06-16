from utils.AbsSQL import AbsSQL
from utils.Operator import Operator


class Where(AbsSQL):
    def __init__(self, cypher):
        self.op = Operator()
        super().__init__(cypher)

    def handle_sql(self, data):
        for key in data:
            if str(key).lower() == 'and':
                # handle and case
                self.cypher += self.handle_and_or_case(data[key])
            elif str(key).lower() == 'or':
                # handle or case
                self.cypher += self.handle_and_or_case(data[key], keyword='OR')
            elif str(key).lower() == 'in':
                # handle in case
                self.cypher += self.handle_in_case(data[key])
            else:
                self.cypher += self.generate_condition(key, data[key])

    def generate_condition(self, key, value):
        ope = self.op.get_operator(key)
        # value is a list type
        values = []
        find_literal = False
        for v in value:
            if type(v) != dict:
                values.append(v)
            else:
                if 'literal' in v.keys():
                    values.append(v['literal'])
                    find_literal = True
                elif 'sum' in v.keys():
                    values.append('sum({})'.format(v['sum']))
                elif 'avg' in v.keys():
                    values.append('avg({})'.format(v['avg']))
                elif 'count' in v.keys():
                    values.append('count({})'.format(v['count']))
        if not find_literal:
            find_literal = all(isinstance(item, str) for item in values)
        result = self.get_clause_pattern(" {} {} {} ").format(values[0], ope, values[1]) if not find_literal \
            else self.get_clause_pattern(" {} {} '{}' ").format(values[0], ope, values[1])
        return result

    def handle_and_or_case(self, data, keyword="AND"):
        """
        handle and case for the where condition
        :param data: list
        :param operators: the operations, eg: >, <, >=, <=, =, !=
        :param keyword: AND, OR
        :return:
            A string of query language
        """
        result = ""
        for case in data:
            if result != "":
                result += keyword
            for key, value in case.items():
                # get the operation first
                result += self.generate_condition(key, value)
        return result

    def handle_in_case(self, data):
        """
        handle in case in where conditions
        eg: {'in': ['p.ProductName', {'literal': ['a', 'b']}]}
        ['p.ProductName', [1, 2]]}
        when index = 0, it is a keyword
        :param data: dict type data
        :return:
            A string
        """
        values = []
        result = "{} IN [".format(data[0])
        is_literal = False
        for i in range(1, len(data)):
            if type(data[i]) != dict:
                values = [i for i in data[i]]
            else:
                is_literal = True
                values = [i for i in data[i]['literal']]

        if is_literal:
            result += ", ".join("'{}'".format(i) for i in values)
        else:
            result += ", ".join(str(i) for i in values)

        return result + "] "
