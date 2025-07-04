import upstox_client
import data_token

from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))



entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="IMMEDIATE", trigger_price=60)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=90)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=50, trailing_gap=3)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttPlaceOrderRequest(type="MULTIPLE", instrument_token="NSE_EQ|INE584A01023", product="MTF", quantity=1, rules=rules, transaction_type="BUY")
try:
    api_response = api_instance.place_gtt_order(body=body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)