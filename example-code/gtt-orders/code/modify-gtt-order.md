## Modify Single Leg GTT Order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="ABOVE", trigger_price=7.3)
rules = [entry_rule]

body = upstox_client.GttModifyOrderRequest(
    type="SINGLE", 
    gtt_order_id="GTT-C25270200137952",
    rules=rules,
    quantity=1
)

try:
    api_response = api_instance.modify_gtt_order(body=body)
    print("GTT order response:", api_response)
except ApiException as e:
    print("Exception when calling OrderApi->modify_gtt_order: %s\n" % e)
```

## Modify Multiple Leg GTT Order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="ABOVE", trigger_price=7.3)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=7.64)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=7.1)
rules = [entry_rule, target_rule, stoploss_rule]

body = upstox_client.GttModifyOrderRequest(
    type="MULTIPLE", 
    gtt_order_id="GTT-C25280200137522",
    rules=rules,
    quantity=1
)

try:
    api_response = api_instance.modify_gtt_order(body=body)
    print("GTT order response:", api_response)
except ApiException as e:
    print("Exception when calling OrderApi->modify_gtt_order: %s\n" % e)
```
