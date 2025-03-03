import upstox_client
import data_token

from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))



entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="ABOVE", trigger_price=7)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=9)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=5)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttModifyOrderRequest(type="MULTIPLE", gtt_order_id="GTT-C2503030018840", rules=rules, quantity=2)
try:
    api_response = api_instance.modify_gtt_order(body=body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)