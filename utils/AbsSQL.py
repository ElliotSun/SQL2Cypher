from abc import ABC, abstractmethod


class AbsSQL(ABC):
    def __init__(self, cypher):
        self.cypher = cypher
        self.add_dumb_prefix = False
        super().__init__()

    def get_cypher(self):
        return self.cypher + " "

    def set_dumb_prefix(self, need_prefix: bool):
        self.add_dumb_prefix = need_prefix

    def get_clause_pattern(self, pattern):
        if self.add_dumb_prefix:
            index = pattern.index('{')
            return pattern[:index] + 'n.' + pattern[index:]
        else:
            return pattern

    @staticmethod
    def check_data(data):
        if data is None:
            raise ValueError("Incorrect data")

    @abstractmethod
    def handle_sql(self, data):
        pass
