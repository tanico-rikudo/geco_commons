from pymongo import MongoClient
from pymongo import DESCENDING, ASCENDING
import configparser
import logging
import logging.config
import ast
import urllib.parse

#TODO: Optimize. 
# filterTimeBeginWith: Allow to multiple dates...
MongoHandlerConditionMolts = {
    "filterTimeBeginWith": "{{'time':{{'$regex':'^{0}'}}}}",
    "filterSymbol": "{{'symbol':'{0}'}}",
    "filterTimeBetween": "{{ 'time' : {{ '$gte' : '{0}', '$lte' : '{1}' }} }}"
}


class MongoUtil:

    def __init__(self, mongoHandler, logger):
        self.dao = mongoHandler
        self._logger = logger

    def delete_at_date(self, table, date=None, symbol=None):
        _filter = {}
        if date is not None:
            filter_date = ast.literal_eval(MongoHandlerConditionMolts.get("filterTimeBeginWith").format(date))
            _filter.update(filter_date)
        if symbol is not None:
            filter_symbol = ast.literal_eval(MongoHandlerConditionMolts.get("filterSymbol").format(symbol))
            _filter.update(filter_symbol)
        self.dao.delete(table, filter=_filter)

    def find_at_date(self, table, date=None, symbol=None):
        _filter = {}
        if date is not None:
            filter_date = ast.literal_eval(MongoHandlerConditionMolts.get("filterTimeBeginWith").format(date))
            _filter.update(filter_date)
        if symbol is not None:
            filter_symbol = ast.literal_eval(MongoHandlerConditionMolts.get("filterSymbol").format(symbol))
            _filter.update(filter_symbol)
        return self.dao.find(table, filter=_filter)
    
    def find_between_dates(self, table, sd=None, ed=None, symbol=None):
        _filter = {}
        # Note: not allow only sd
        if (sd is not None)or(ed is not None):
            filter_date = ast.literal_eval(MongoHandlerConditionMolts.get("filterTimeBetween").format(sd, ed))
            _filter.update(filter_date)
        if symbol is not None:
            filter_symbol = ast.literal_eval(MongoHandlerConditionMolts.get("filterSymbol").format(symbol))
            _filter.update(filter_symbol)
        return self.dao.find(table, filter=_filter)


class MongoHandler:

    def __init__(self, config, table_name):
        self.host = config.get('MONGODB_HOST')
        self.port = config.get('MONGODB_PORT')
        self.db_name = config.get('MONGODB_NAME')
        self.db_user = config.get('MONGODB_USERNAME')
        self.db_pw = config.get('MONGODB_PASSWORD')

        self.connect_url = f"mongodb://{self.db_user}:{self.db_pw}@{self.host}:{self.port}/?authSource={self.db_name}"
        self.client = MongoClient(self.connect_url)
        self.table_name = table_name
        self.db = self.client[self.db_name]

    def use_table(self, table_name=None):
        table_name = self.table_name if table_name is None else table_name
        if not table_name in self.db.list_collection_names():
            self.db.create_collection(table_name,
                                      storageEngine={'wiredTiger': {'configString': 'block_compressor=snappy'}})
        table = self.db[table_name]
        return table

    def insert_one(self, json, table_name=None):
        return self.use_table(table_name).insert_one(json)

    def insert_many(self, json_list, table_name=None):
        return self.use_table(table_name).insert_many(json_list)

    def delete(self, table_name=None, filter=None):
        return self.use_table(table_name).delete_many(filter=filter)

    def find(self, table_name=None, projection=None, filter=None, sort=None):
        return self.use_table(table_name).find(projection=projection, filter=filter, sort=sort)

    def close(self):
        self.client.close()

    def start_session(self):
        self.session = self.client.start_session()
        self.session.start_transaction()
        return session

    def end_session(self):
        self.session.end_session()
        self.session = None

    def test():
        try:
            # self.db[self.DB_NAME].update_one(, session=s)
            pass
        except Exception:
            self.abort_transaction()
        else:
            self.commit_transaction()
