from utils.OrderBy import OrderBy
from utils.Select import Select
from utils.From import From
from utils.Where import Where
from utils.Limit import Limit
import re


class SQLParser:
    def __init__(self):
        self.cypher = ""
        self.Orderby = OrderBy("ORDER BY ")
        self.Select = Select("RETURN ")
        self.From = From("MATCH ")
        self.Where = Where("WHERE ")
        self.Limit = Limit("LIMIT ")
        self.add_dumb_prefix = False

    def generate_cypher(self, data, sql, db_id):
        if "from" in data:
            if 'join' in sql.lower():
                self.From.handle_join(data, db_id)
                self.cypher += self.From.get_cypher()
            else:
                if type(data['from']) == str:
                    self.add_dumb_prefix = True
                self.From.handle_sql(data['from'], db_id)
                self.cypher += self.From.get_cypher()

        if "where" in data:
            self.Where.set_dumb_prefix(self.add_dumb_prefix)
            self.Where.handle_sql(data['where'])
            self.cypher += self.Where.get_cypher()

        if "select" in data:
            self.Select.set_dumb_prefix(self.add_dumb_prefix)
            self.Select.handle_sql(data['select'])
            self.cypher += self.Select.get_cypher()

        if 'orderby' in data:
            self.Orderby.set_dumb_prefix(self.add_dumb_prefix)
            self.Orderby.handle_sql(data['orderby'])
            self.cypher += self.Orderby.get_cypher()

        if 'limit' in data:
            self.Limit.handle_sql(data['limit'])
            self.cypher += self.Limit.get_cypher()

        # use regex to clean up final query
        regex_pattern = '(\w+:\w+)' # pattern to replace count(n) if multiple table
        matches = re.findall(regex_pattern, self.cypher)
        print(matches)
        if len(matches) > 1:
            prefix = matches[0].split(':')[0]
            self.cypher = self.cypher.replace('count(n)', 'count({})'.format(prefix))

    def get_cypher(self):
        return self.cypher + ";"
