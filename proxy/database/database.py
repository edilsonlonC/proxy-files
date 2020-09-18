import pymongo
import os 
import pprint
host = os.getenv('HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
print(host,port)


def database():
    client = pymongo.MongoClient(host,int(port))
    db = client[db_name]
    return db


