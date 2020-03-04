import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database as db
from src.models.stores.store import Store

class Item(object):

    def __init__(self,name,url,price=None,_id=None):
        self.name = name
        self.url = url
        store = Store.getByURL(self.url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {} >".format(self.name,self.url)

    def load_price(self):
        #Amazon : <span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">$799.00</span>
        #element =  soup.find("span",{"class":"a-size-medium a-color-price priceBlockBuyingPriceString"})

        request_page = requests.get(self.url)
        content = request_page.content
        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name,self.query)
        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())

        return self.price

    @classmethod
    def getById(cls,item_id):
        return cls(**db.find_one(ItemConstants.Collection, {'_id': item_id}))

    def save_database(self):
        db.insert(ItemConstants.Collection,self.json())

    def update_record(self):
        db.update(ItemConstants.Collection,{'_id': self._id},self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id": self._id,
            "price": self.price
        }


