from models.model import Model
from typing import Dict
from dataclasses import dataclass, field
import uuid
import re


@dataclass(eq=False)
class Store(Model):
    # collection = "stores"
    #
    # def __init__(self, name: str, url_prefix: str, tag_name: str, query: Dict, _id: str = None):
    #     super().__init__()  # Call to super class __init__ missing - fix
    #     self.name = name
    #     self.url_prefix = url_prefix
    #     self.tag_name = tag_name
    #     self.query = query
    #     self._id = _id or uuid.uuid4().hex

    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":  # Store.get_by_name("John Lewis")
        return cls.find_one_by("name", store_name)  # self.name (name) by store_name

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":  # Store.get_by_url_prefix('https://www.johnlewis.com')
        url_regex = {"$regex": "^{}".format(url_prefix)}
        # $regex is MongoDB expression for 1 of many query methods. ^ = start with
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like "https://www.johnlewis.com/item/sdfa9081049120.html"
        :param url: The item's URL
        :return: a Store
        """
        pattern = re.compile(r"(https?://.*?/)")  # r"(****)" => BRACKETS () is ESSENTIAL~!
        # \/ is not required in Python, JS is required. RE is used to convert string to specific data type
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
