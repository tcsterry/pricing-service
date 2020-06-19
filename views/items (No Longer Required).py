from flask import request, render_template, Blueprint
from models.item import Item
import json

item_blueprint = Blueprint('items (No Longer Required)', __name__)


@item_blueprint.route('/')
def index():  # 3rd step => 2 end points, this is first => show items (No Longer Required)
    items = Item.all()
    return render_template('items (No Longer Required)/index.html', items=items)


@item_blueprint.route('/new', methods=['GET', 'POST'])
def new_item():  # 2nd step to create items (No Longer Required) => Define blueprint
    if request.method == 'POST':
        url = request.form['url']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Item(url, tag_name, query).save_to_mongo()

    return render_template('items (No Longer Required)/new_item.html')  # 4th step => 2nd end point, take in data or show template
