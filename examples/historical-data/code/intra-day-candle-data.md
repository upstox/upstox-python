## Get intraday candle data with a 1-minute interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
try:

    api_response = api_instance.get_intra_day_candle_data(instrument_key,interval,api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

```

## Get intraday candle data with a 30-minute interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '30minute'
try:

    api_response = api_instance.get_intra_day_candle_data(instrument_key,interval,api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

```
