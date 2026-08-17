## Get IPO order details by order id

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# `order_id` is returned by apply_for_ipo or get_ipo_orders
order_id = '{ipo_order_id}'

try:
    api_response = api_instance.get_ipo_order_by_id(order_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_order_by_id: %s\n" % e)
```

## Read the order and payment status of an IPO order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

order_id = '{ipo_order_id}'

try:
    api_response = api_instance.get_ipo_order_by_id(order_id)
    order = api_response.data
    print('symbol:         ', order.symbol)
    print('exchange:       ', order.exchange)
    print('order status:   ', order.order_status)
    print('payment status: ', order.payment_status)
    print('units allotted: ', order.units_allotted)
    for bid in order.bids or []:
        print('   bid:', bid['quantity'], '@', bid['price'], '=', bid['amount'])
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_order_by_id: %s\n" % e)
```

## Look up the most recent IPO order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    orders = api_instance.get_ipo_orders(page_number=1, records=1)
    if orders.data:
        order_id = orders.data[0]['order_id']
        api_response = api_instance.get_ipo_order_by_id(order_id)
        print(api_response)
    else:
        print('no IPO orders found')
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_order_by_id: %s\n" % e)
```
