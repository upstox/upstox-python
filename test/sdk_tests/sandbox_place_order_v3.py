import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration(sandbox=True)
configuration.access_token = 'SANDBOX_ACCESS_TOKEN'

api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderV3Request(quantity=1, product="D",validity="DAY", price=9.12, tag="string", instrument_token="NSE_EQ|INE669E01016", order_type="LIMIT",transaction_type="BUY", disclosed_quantity=0, trigger_price=0.0, is_amo=True, slice=True)

try:
    api_response = api_instance.place_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)