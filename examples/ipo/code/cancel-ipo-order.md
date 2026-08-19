## Cancel an IPO order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# `order_id` is returned by apply_for_ipo or get_ipo_orders
order_id = '{ipo_order_id}'

try:
    api_response = api_instance.cancel_ipo_order(order_id)
    print(api_response)
    print('cancelled order id:', api_response.data.order_id)
    print('status:', api_response.data.status)
except ApiException as e:
    print("Exception when calling IpoApi->cancel_ipo_order: %s\n" % e)
```

## Apply, then cancel the same IPO order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

body = upstox_client.IpoApplyRequest(
    id='{ipo_slug_id}',
    upi='{your_upi_id}',
    category='IND',
    bids=[
        upstox_client.IpoBidRequest(quantity=10, price=150.0)
    ]
)

try:
    apply_response = api_instance.apply_for_ipo(body)
    order_id = apply_response.data.order_id
    print('applied, order id:', order_id)

    cancel_response = api_instance.cancel_ipo_order(order_id)
    print('cancelled:', cancel_response.data.status)
except ApiException as e:
    print("Exception when calling IpoApi ipo order write ops: %s\n" % e)
```

> Note: cancellation is only accepted while the IPO bidding window is still
> open. Once the issue closes, the order can no longer be withdrawn — check
> `bidding_end_date` from get_ipo_details before cancelling.
