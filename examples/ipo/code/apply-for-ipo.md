## Apply for an IPO

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# `id` is the IPO slug id returned by get_ipo_listing
# `category`: IND (Individual) | HNI (High Net-worth Individual)
# `bids`: at least one bid, maximum of 3
body = upstox_client.IpoApplyRequest(
    id='{ipo_slug_id}',
    upi='{your_upi_id}',
    category='IND',
    bids=[
        upstox_client.IpoBidRequest(quantity=10, price=150.0)
    ]
)

try:
    api_response = api_instance.apply_for_ipo(body)
    print(api_response)
    print('IPO order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling IpoApi->apply_for_ipo: %s\n" % e)
```

## Apply for an IPO with multiple bids

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# Up to 3 bids may be submitted in a single application.
# Use the cut-off price / lot size from get_ipo_details to build valid bids.
body = upstox_client.IpoApplyRequest(
    id='{ipo_slug_id}',
    upi='{your_upi_id}',
    category='HNI',
    bids=[
        upstox_client.IpoBidRequest(quantity=10, price=150.0),
        upstox_client.IpoBidRequest(quantity=20, price=155.0),
        upstox_client.IpoBidRequest(quantity=30, price=160.0)
    ]
)

try:
    api_response = api_instance.apply_for_ipo(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->apply_for_ipo: %s\n" % e)
```

> Note: after a successful application, approve the UPI mandate request in your
> UPI app to block the funds. Until the mandate is approved, the order remains
> pending.
