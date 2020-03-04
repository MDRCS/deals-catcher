import uuid
import requests
from datetime import datetime,timedelta

from src.models.items.item import Item
import src.models.alerts.constants as AlertConstants
from src.common.database import Database as db

class Alert(object):

    def __init__(self,user_email,price_limit,item_id,active=True,last_checked=None,_id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.getById(item_id)
        self.last_checked = datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email,self.item.name,self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.MAILGUN_API_URL,
            auth=("api", AlertConstants.MAILGUN_API_KEY),
            data={"from": AlertConstants.FROM,
                  "to": self.user_email,
                  "subject": "PRICE LIMIT REACHED FOR {}".format(self.item.name),
                  "text": "WE HAVE FUN A DEAL! ({}). to navigate to alert visit {}".format(self.item.url, "http://pricing.mdrahali.com/alerts/{}".format(self._id))})

    @classmethod
    def find_needing_update(cls,minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.utcnow() - timedelta(minutes=minutes_since_update)
        return [cls(**alert) for alert in db.find(AlertConstants.Collection,
                                                  {'last_checked':
                                                       {'$lte': last_updated_limit},
                                                   'active': True
                                                   })]


    def save_database(self):
        db.insert(AlertConstants.Collection,self.json())

    def update_record(self,query):
        db.update(AlertConstants.Collection,query,self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.utcnow()
        self.item.update_record()
        self.update_record({'_id': self._id})
        return self.item.price

    def send_ifprice_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def getByEmail(cls,email):
        return [cls(**alert) for alert in db.find(AlertConstants.Collection,{'user_email': email})]

    @classmethod
    def getById(cls,_id):
        return cls(**db.find_one(AlertConstants.Collection,{'_id': _id}))

    def deactivate(self):
        self.active = False
        self.update_record({'_id': self._id})

    def activate(self):
        self.active = True
        self.update_record({'_id': self._id})

    def delete(self):
        db.remove(AlertConstants.Collection, {'_id': self._id})
