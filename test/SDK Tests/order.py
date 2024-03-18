import upstox_client
from upstox_client.rest import ApiException
import const_file
configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token
# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "MARKET", "BUY", 0, 0.0, False)
# api_version = '2.0'
# try:
#     api_response = api_instance.place_order(body, api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->place_order: %s\n" % e)

# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 20.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 20.1, False)
# api_version = '2.0'
# try:
#     api_response = api_instance.place_order(body, api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->place_order: %s\n" % e)

# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# body = upstox_client.ModifyOrderRequest(2, "DAY", 0, "231222010275930", "MARKET", 0, 0)
# api_version = '2.0'  # str | API Version Header
#
# try:
#     # Modify order
#     api_response = api_instance.modify_order(body, api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->modify_order: %s\n" % e)

#
# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# order_id = '240318010654488'
# api_version = '2.0'
#
# try:
#     # Cancel order
#     api_response = api_instance.cancel_order(order_id, api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->cancel_order: %s\n" % e)

# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# api_version = '2.0'
# try:
#     # Get order book
#     api_response = api_instance.get_order_book(api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->get_order_book: %s\n" % e)


# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# api_version = '2.0'
# order_id = '240318010654488'
#
# try:
#     api_response = api_instance.get_order_details(api_version, order_id=order_id)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->get_order_details: %s\n" % e)

# api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
# api_version = '2.0'
#
# try:
#     # Get trades
#     api_response = api_instance.get_trade_history(api_version)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling OrderApi->get_trade_history: %s\n" % e)
#

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = '240318010654488'
api_version = '2.0'

try:
    # Get trades for order
    api_response = api_instance.get_trades_by_order(order_id, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trades_by_order: %s\n" % e)

