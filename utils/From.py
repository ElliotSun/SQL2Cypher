import json
import os
import pickle
from typing import List

from utils.AbsSQL import AbsSQL
from conf.config import Config
from pathlib import Path


class From(AbsSQL):

    def handle_sql(self, data, db_id):
        """
        handle the from data, because it includes many from values
        :param data: dict data or list
        :return:
             a string contain the match data
        """
        self.check_data(data)
        candidates = self.get_label_name_candidates(db_id)
        if type(data) == dict:
            self.cypher += "({}:{}) ".format(data['name'], self.get_label_in_correct_case(candidates, data['value']))
        elif type(data) == list:
            pass
        elif type(data) == str:
            self.cypher += "(n:{}) ".format(self.get_label_in_correct_case(candidates, data))

    def load_relation(self, db_id):
        filepath = Path(Config.spider_folder + "/consolidated_relations.json")
        try:
            files = open(filepath, "rb")
            data = json.load(files)
            if type(data) is list:
                return next(r for r in data if r['db_id'] == db_id)
        except FileNotFoundError:
            raise FileNotFoundError("You haven not converted the database into cypher yet.")

    def handle_left_join(self, data):
        pass

    def get_label_name_candidates(self, db_id) -> List[str]:
        filepath = Path(Config.spider_folder + "/database/" + db_id + "/csv")
        csv_file_names = []
        for (root, dirs, file) in os.walk(filepath):
            for f in file:
                if '.csv' in f:
                    csv_file_names.append(f.split('.')[0])
        return csv_file_names

    # Cypher is case-sensitive for labels
    def get_label_in_correct_case(self, candidates: List[str], table_name: str):
        label = next((name for name in candidates if table_name.upper() == name.upper()))
        return label

    def handle_join(self, data, db_id):
        """
        handle the join relation
        :param db_id:
        :param data: the from data, should be the whole from data
        :return: the string
        """
        candidates = self.get_label_name_candidates(db_id)
        tables = []
        for t in data['from']:
            if 'join' not in t:
                tables.append(t['value'].lower())
            else:
                tables.append(t['join']['value'].lower())

        relation = self.load_relation(db_id)
        print(relation)
        for r in relation['db_relationships']:
            key = str(list(r.keys())[0])
            if key.lower() in tables:
                if str(r[key]['to']).lower() in tables:
                    self.cypher += " ({}:{})-[:{}]->({}:{}) ".format(key.lower(), self.get_label_in_correct_case(candidates, key),
                                                                     r[key]['relation'], str(r[key]['to'].lower()),
                                                                     self.get_label_in_correct_case(candidates, r[key]['to']))
                elif 'mapping' in r[key].keys() and str(r[key]['mapping']).lower() in tables:
                    self.cypher += " ({}:{})-[:{}]->({}:{}) ".format(key.lower(), self.get_label_in_correct_case(candidates, key),
                                                                     r[key]['relation'], str(r[key]['to'].lower()),
                                                                     self.get_label_in_correct_case(candidates, r[key]['to']))

            else:
                if str(r[key]['to']).lower() in tables:
                    if 'mapping' in r[key].keys()  and str(r[key]['mapping']).lower() in tables:
                        self.cypher += " ({}:{})-[:{}]->({}:{}) ".format(key.lower(), self.get_label_in_correct_case(candidates, key),
                                                                         r[key]['relation'], str(r[key]['to'].lower()),
                                                                         self.get_label_in_correct_case(candidates, r[key]['to']))
