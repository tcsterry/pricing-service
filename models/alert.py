import uuid
from typing import Dict
from dataclasses import dataclass, field
from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from models.user import User


@dataclass(eq=False)  # eq=False => Disable compare function
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    # init=False => Will not be included in init, so cannot be modified
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # def __init__(self, item_id: str, price_limit: float, _id: str = None):
    #     super().__init__()  # If it is a Superclass, dataclass will call it automatically.
    #     self.item_id = item_id
    #     self.item = Item.get_by_id(item_id)
    #     self.price_limit = price_limit
    #     self._id = _id or uuid.uuid4().hex

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        # Reason for this method is to call self.item_id right after Dataclass declaration in init method
        # as it does not allow usage of self.item_id immediately after declaration.
        # So this method is called right after init declaration.
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(
                f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}."
            )
            Mailgun.send_mail(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Check your item out <a href="{self.item.url}">here</a>.</p>',
                # f'Notification for {self.name}',  # Title
                # f'Your alert {self.name} has reached a price under {self.price_limit}. '  # In normal Text
                # f'The latest price is {self.item.price}. '
                # f'Go to this address to check your item: {self.item.url}.',
                # f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p>'  # In HTML text
                # f'<p>The latest price is {self.item.price}.</p>'
                # f'<p>Click <a href="{self.item.url}">here</a> to purchase your item.</p>'
            )
