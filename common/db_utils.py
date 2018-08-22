from pymongo import MongoClient
from common.config import Conf


class DBUtils():
    # mongo实例
    @staticmethod
    def get_mongo_conn(mongo_config):
        uri = mongo_config['uri']
        return MongoClient(uri)

    # mongo 数据库
    # mongo_str 标识是哪个mongo实例
    # db_str 数据库
    @staticmethod
    def get_mongo_db(mongo_config, db_str):
        return DBUtils.get_mongo_conn(mongo_config)[db_str]

    # mongo collection
    @staticmethod
    def get_mongo_collection(mongo_config, db_str, collection_str):
        return DBUtils.get_mongo_db(mongo_config, db_str)[collection_str]


mongo_mk = DBUtils.get_mongo_conn(Conf.mongo_mk)
mk_db = mongo_mk[Conf.mongo_mk.get('db_name')]
