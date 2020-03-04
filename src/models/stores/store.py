import uuid
from src.common.database import Database as db
import src.models.stores.constrants as StoreConstants
import src.models.items.constants as ItemConstants
import src.models.stores.errors as StoreErrors

class Store(object):
    def __init__(self,name,url_prefix,tag_name,query,_id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def getById(cls,_id):
        return cls(**db.find_one(StoreConstants.Collection, {'_id': _id}))

    @classmethod
    def getByName(cls,store_name):
        return cls(**db.find_one(StoreConstants.Collection, {'name': store_name}))

    @classmethod
    def getByUrl_prefix(cls,url_prefix):
        return cls(**db.find_one(StoreConstants.Collection, {'url_prefix': {'$regex': '{}'.format(url_prefix)}}))

    @classmethod
    def getByURL(cls,url):
        for i in range(0,len(url) + 1):
            try:
                store = cls.getByUrl_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL PREFIX USED TO FIND THE STORE DIDN'T GIVE US ANY RESULTS.")

    def save_database(self):
        db.insert(StoreConstants.Collection,self.json())

    @classmethod
    def all(cls):
        return [cls(**store) for store in db.find(StoreConstants.Collection,{})]

    def update_record(self):
        db.update(StoreConstants.Collection,{'_id': self._id},self.json())

    def delete_record(self):
        db.remove(StoreConstants.Collection,{'_id': self._id})
