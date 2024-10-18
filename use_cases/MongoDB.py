from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class MongoDB:
    def __init__(self, collection: str) -> None:
        self.collection = collection
        self.client = MongoClient(host=getenv('DB_HOST'), port=int(getenv('DB_PORT')))
        self.database = self.client.get_database(name=getenv('DB_NAME'))

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, content):
        self._collection = "default" if not content else content

    @property
    def _collection_(self):
        return self.database.get_collection(name=self.collection)

    def insert_one(self, data: dict):
        self._collection_.insert_one(data)

    def insert_many(self, data: list):
        self._collection_.insert_many(data)

    def update_one(self, filter: dict, update: dict):
        self._collection_.update_one(filter=filter, update={"$set": update})

    def update_many(self, filter: dict, update: dict):
        self._collection_.update_many(filter=filter, update=update)

    def consult(self, filter: dict):
        return self._collection_.find(filter=filter) if not filter.__eq__({}) else (data for data in self._collection_.find())

    def consult_one(self, filter: dict):
        return self._collection_.find_one(filter=filter)
    
    def delete_many(self, filter:dict):
        self._collection_.delete_many(filter)
