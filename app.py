# from models.item import Item
#
#
# url = "https://www.johnlewis.com/2018-apple-ipad-pro-12-9-inch-a12x-bionic-ios-wi-fi-cellular-1tb/space-grey/p3834587"
# tag_name = "p"
# query = {"class": "price price--large"}  # this is Dict Type
#
# ipad = Item(url, tag_name, query)
# ipad.save_to_mongo()
#
# items_loaded = Item.all()
# print(items_loaded)
# print(items_loaded[0].load_price())
#
# from models.alert import Alert
#
# alert = Alert("47d1a49aec374d678fc68bfa9cee4055", 2000)
# alert.save_to_mongo()
# import json
from flask import Flask, render_template
# from views.items import item_blueprint
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


# app.register_blueprint(item_blueprint, url_prefix="/items (No Longer Required)")
# 1st step to create items (No Longer Required) => register in app.py
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")


# if __name__ == "__main__":
#     app.run(debug=True)
