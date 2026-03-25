## Get brokerage details for equity delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = 'NSE_EQ|INE669E01016'
quantity = 10
product = 'D'
transaction_type = 'BUY'
price = 13.4 

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)

```

## Get brokerage details for equity intraday orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = 'NSE_EQ|INE669E01016'
quantity = 10
product = 'I'
transaction_type = 'BUY'
price = 13.4

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)

```

## Get brokerage details for equity futures and options delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = 'NSE_FO|35271'
quantity = 10
product = 'D'
transaction_type = 'BUY'
price = 1333.4

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)

```

## Get brokerage details for equity futures and options intraday orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = 'NSE_FO|35271'
quantity = 10
product = 'I'
transaction_type = 'BUY'
price = 1333.4

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
```
