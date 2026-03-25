## Get margin details for equity delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instruments = [upstox_client.Instrument(instrument_key="NSE_EQ|INE528G01035",quantity=5,product="D",transaction_type="BUY")]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    print(api_response)
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)

```

## Get margin details for future delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instruments = [upstox_client.Instrument(instrument_key="NSE_FO|35000",quantity=5,product="D",transaction_type="BUY")]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    print(api_response)
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)

```

## Get margin details for option delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instruments = [upstox_client.Instrument(instrument_key="NSE_FO|54524",quantity=5,product="D",transaction_type="BUY")]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    print(api_response)
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)

```

## Get margin details for MCX delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instruments = [upstox_client.Instrument(instrument_key="MCX_FO|435356",quantity=5,product="D",transaction_type="BUY")]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    print(api_response)
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)

```

## Get margin details for currency delivery orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instruments = [upstox_client.Instrument(instrument_key="NCD_FO|15758",quantity=5,product="D",transaction_type="BUY")]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    print(api_response)
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)

```
