import upstox_client
import data_token
from upstox_client.rest import ApiException
import json


configuration = upstox_client.Configuration(sandbox=True)
configuration.access_token = data_token.sandbox_access_token
api_version = '2.0'



instruments = [
    upstox_client.Instrument(instrument_key="NSE_EQ|INE528G01035", quantity=12, product="D", transaction_type="BUY"),
    upstox_client.Instrument(instrument_key="NSE_EQ|INE002A01018", quantity=1, product="D", transaction_type="BUY")
]

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 12.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 0.0,
                                       False)
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("exception in place order: ", e)

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest(2, "DAY", 0, "250121112512866", "MARKET", 0, 0)
api_version = '2.0'  # str | API Version Header

try:
    # Modify order
    api_response = api_instance.modify_order(body, api_version)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify order giving wrong response")

# order details
order_id = '240925010636040'

body = [
    upstox_client.MultiOrderRequest(1, "I", "DAY", 0, "kg_python_sdk", False, "NSE_EQ|INE669E01016", "MARKET", "BUY",
                                    0, 0, True, "1"),
    upstox_client.MultiOrderRequest(1, "D", "DAY", 8.9, "kg_python_sdk1", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "2")
]

try:
    api_response = api_instance.place_multi_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)

# try:
#     api_response = api_instance.get_order_status(order_id="250121112521183")
# except ApiException as e:
#     json_string = e.body.decode('utf-8')
#     data_dict = json.loads(json_string)
#     if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
#         print("order details giving wrong response")

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = '2501211126016789'
api_version = '2.0'

try:
    # Cancel order
    api_response = api_instance.cancel_order(order_id, api_version)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel order giving wrong response")

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
# try:
#     # Get order book
#     api_response = api_instance.get_order_book(api_version)
#     if api_response.status != "success":
#         print("get order book giving invalid data")
# except ApiException as e:
#     print("Exception when calling OrderApi->get_order_book: %s\n" % e)
# except ValueError as e:
#     print(e)

order_id = '25012112309073'

# try:
#     api_response = api_instance.get_order_details(api_version, order_id=order_id)
# except ApiException as e:
#     json_string = e.body.decode('utf-8')
#     data_dict = json.loads(json_string)
#     if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
#         print("get order details giving wrong response")

api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderV3Request(quantity=1, product="D",validity="DAY", price=9.12, tag="string", instrument_token="NSE_EQ|INE669E01016", order_type="LIMIT",transaction_type="BUY", disclosed_quantity=0, trigger_price=0.0, is_amo=True, slice=True)

try:
    api_response = api_instance.place_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)

body = upstox_client.ModifyOrderRequest(3, "DAY", 9.12, "250120010373947", "LIMIT", 0, 0)

try:
    api_response = api_instance.modify_order(body)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify order giving wrong response")


try:
    # Cancel order
    api_response = api_instance.cancel_order(order_id)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel order giving wrong response")