import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
order_id = 'xxxxxxxx'
try:

    # get order details
    api_response = api_instance.get_order_status(order_id=order_id)
    print(api_response)

except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("order details giving wrong response")
        
try: 
    # order history
    api_response = api_instance.get_order_details(order_id=order_id, api_version=api_version)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("order history giving wrong response")

try:
    # Get order book
    api_response = api_instance.get_order_book(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_book: %s\n" % e)


try:
    # Get trades for the day
    api_response = api_instance.get_trade_history(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trade_history: %s\n" % e)



try:
    # Get trades for order
    api_response = api_instance.get_trades_by_order(order_id, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trades_by_order: %s\n" % e)

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_positions(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling position: %s\n" % e)