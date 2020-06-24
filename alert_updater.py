from models.alert import Alert
# from dotenv import load_dotenv  # dotenv has to manually loaded as it is not supported by flask
#
# load_dotenv()

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()
    # alert.json()

if not alerts:
    print("No alerts have been created. Add an item and an alert to begin!")