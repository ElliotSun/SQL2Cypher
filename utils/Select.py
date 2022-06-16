from utils.AbsSQL import AbsSQL


class Select(AbsSQL):

    def handle_sql(self, data):
        """
        handle select form
        :param data: list or dict data
        :return:
        """
        if type(data) == dict:
            if type(data['value']) == dict:
                if 'count' in data['value'].keys():
                    if type(data['value']['count']) == dict:
                        count_expression = data['value']['count']
                        if 'distinct' in count_expression.keys():
                            self.cypher += self.get_clause_pattern('count(distinct {})').format(
                                count_expression['distinct']['value'])
                    elif type(data['value']['count']) == str:
                        if data['value']['count'] == '*':
                            self.cypher += ' count(n) '

                elif 'distinct' in data['value'].keys():
                    self.cypher += " DISTINCT"
                    if type(data['value']['distinct']) == dict:
                        self.cypher += self.get_clause_pattern(" {} ").format(data['value']['distinct']['value'])
                    else:
                        self.cypher += ",".join(self.get_clause_pattern(" {} ").format(item['value'])
                                                for item in data['value']['distinct'])
                else:
                    self.cypher += ",".join(
                        self.get_clause_pattern(" {}{} ").format(str(key).upper(), str(value).replace('.*', ''))
                        for key, value in data['value'].items())
            else:
                self.cypher += self.get_clause_pattern(" {} ").format(str(data['value']).replace('.*', ''))
        elif type(data) == list:
            for item in data:
                if type(item['value']) == dict:
                    keys = item['value'].keys()
                    if 'count' in keys:
                        if type(item['value']['count']) == dict:
                            count_expression = item['value']['count']
                            if 'distinct' in count_expression.keys():
                                item['value'] = self.get_clause_pattern('count(distinct {})').format(count_expression['distinct'])
                        item['value'] = self.get_clause_pattern('count({})').format(item['value']['count']).replace('.*', '')
                    if 'sum' in keys:
                        item['value'] = self.get_clause_pattern('sum({})').format(item['value']['sum'])
                    if 'avg' in keys:
                        item['value'] = self.get_clause_pattern('avg({})').format(item['value']['avg'])
                    if 'min' in keys:
                        item['value'] = self.get_clause_pattern('min({})').format(item['value']['min'])
                    if 'max' in keys:
                        item['value'] = self.get_clause_pattern('max({})').format(item['value']['max'])
                else:
                    item['value'] = self.get_clause_pattern('{}').format(item['value'])
            values = [x['value'] for x in data]
            self.cypher += ", ".join(values)
