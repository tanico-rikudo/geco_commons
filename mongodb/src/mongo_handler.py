from pymongo import MongoClient
import configparser
import logging
import logging.config

class MongoHandler:
    def __init__(self,config,db_name):
        self.host = config.get('host')
        self.clint = MongoClient(self.host,)
        self.db_name = db_name
        self.db = self.clint[self.db_name]

    def insert_one(self, json, db=None):
        return self.db[self.db_name].insert_one(json)

    def insert_many(self, json_list):
        return self.db[self.db_name].insert_many(json_list)

    def delete_all(self):
        self.db[self.db_name].delete_many({})
        return 

    def find(self, query={}):
        return self.db[self.db_name].find(query)

    def start_session(self):
        self.session = self.client.start_session()
        self.session.start_transaction()
        return session

    def end_session(self):
        self.session.end_session()
        self.session = None


    def test():
        try:
            # self.db[self.db_name].update_one(, session=s)
            pass
        except Exception:
            self.abort_transaction()
        else:
            self.commit_transaction()
