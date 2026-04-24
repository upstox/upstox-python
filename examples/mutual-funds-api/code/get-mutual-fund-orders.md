## Get all mutual fund orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_orders()
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_orders: %s\n" % e)
```

## Get mutual fund orders with filters

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_orders(
        status='complete',
        transaction_type='BUY'
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_orders: %s\n" % e)
```

## Get mutual fund orders with pagination

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_orders(
        page_number=1,
        records=10
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_orders: %s\n" % e)
```
