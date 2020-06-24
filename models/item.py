import uuid
from typing import Dict
import re  # Regular Expressions
import requests
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    # collection = "items (No Longer Required)"
    #
    # def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None):
    #     super().__init__()
    #     self.url = url
    #     self.tag_name = tag_name
    #     self.query = query
    #     self.price = None
    #     self._id = _id or uuid.uuid4().hex
    #
    # def __repr__(self):
    #     return f"<Item {self.url}>"  # <> is not required

    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:  # Signal function to return float
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d+\.\d+)")
        # 123.00 or (\d,\d\d\d\.\d\d) = 1,234.00 / ? = Optional
        # + = At least 1 number / * = any numbers
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_comma = found_price.replace(",", "")
        self.price = float(without_comma)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
