from utils.AbsSQL import AbsSQL


class OrderBy(AbsSQL):

    def handle_sql(self, data):
        """
        handle order by
        :param data: list or dict which need to be order
        :return:
            A string
        """
        self.check_data(data)

        # means only one order by
        if type(data) == dict:
            if 'sort' not in data.keys():
                data['sort'] = ''
            if type(data['value']) == str:
                self.cypher += self.get_clause_pattern(" {} {}").format(data['value'], data['sort'].upper())
            if type(data['value']) == dict:
                keys = data['value'].keys()
                if 'count' in keys:
                    self.cypher += self.get_clause_pattern(" count({}) {}").format(data['value']['count'], data['sort'].upper())
                if 'sum' in keys:
                    self.cypher += self.get_clause_pattern(" sum({}) {}").format(data['value']['sum'], data['sort'].upper())
                if 'avg' in keys:
                    self.cypher += self.get_clause_pattern(" avg({}) {}").format(data['value']['avg'], data['sort'].upper())
        else:
            self.cypher += ",".join(self.get_clause_pattern(" {} {}").format(order['value'], order['sort'].upper()) for order in data)
