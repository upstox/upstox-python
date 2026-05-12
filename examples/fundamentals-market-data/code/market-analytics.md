## Get OI Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_oi_data(
        instrument_key='NSE_INDEX|Nifty 50',
        expiry='2026-05-29',
        _date='2026-05-12'
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_oi_data: %s\n" % e)
```

## Get Change in OI Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_change_oi_data(
        instrument_key='NSE_INDEX|Nifty 50',
        expiry='2026-05-29',
        _date='2026-05-12',
        interval=5
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_change_oi_data: %s\n" % e)
```

## Get PCR Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_pcr_data(
        instrument_key='NSE_INDEX|Nifty 50',
        expiry='2026-05-29',
        _date='2026-05-12',
        bucket_interval=30
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_pcr_data: %s\n" % e)
```

## Get Max Pain Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_max_pain_data(
        instrument_key='NSE_INDEX|Nifty 50',
        expiry='2026-05-29',
        _date='2026-05-12',
        bucket_interval=30
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_max_pain_data: %s\n" % e)
```

## Get FII Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_fii_data(
        data_type='NSE_EQ|CASH',
        interval='1D'
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_fii_data: %s\n" % e)
```

## Get FII Data with Date Filter

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_fii_data(
        data_type='NSE_FO|INDEX_FUTURES',
        interval='1M',
        _from='2026-01-01'
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_fii_data: %s\n" % e)
```

## Get DII Data

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_dii_data(
        data_type='NSE_EQ|CASH',
        interval='1D'
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_dii_data: %s\n" % e)
```
