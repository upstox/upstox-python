## Get IPO orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_ipo_orders()
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_orders: %s\n" % e)
```

## Get IPO orders with pagination

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_ipo_orders(
        page_number=1,
        records=20
    )
    print(api_response)
    print('page:', api_response.meta_data.page)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_orders: %s\n" % e)
```

## Iterate over IPO orders and their bids

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_ipo_orders(page_number=1, records=50)
    for order in api_response.data or []:
        print(order['order_id'], order['symbol'], order['order_status'], order['payment_status'])
        for bid in order.get('bids') or []:
            print('   bid:', bid['quantity'], '@', bid['price'], '=', bid['amount'])
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_orders: %s\n" % e)
```
