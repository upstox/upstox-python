## Get historical candle data with a 1-minute interval 

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
to_date = '2023-11-13'
from_date = '2023-11-12'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get data with a 30-minute interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '30minute'
to_date = '2023-11-13'
from_date = '2023-11-12'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get data with a daily interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'day'
to_date = '2023-11-13'
from_date = '2023-11-12'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get data with a weekly interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'week'
to_date = '2023-11-13'
from_date = '2023-10-13'
try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get data with a monthly interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'month'
to_date = '2023-11-13'
from_date = '2022-10-13'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date,from_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get historical candle data with a 1-minute interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
to_date = '2023-11-13'
try:
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

```

## Get data with a 30-minute interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '30minute'
to_date = '2023-11-13'
try:
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```

## Get data with a daily interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'day'
to_date = '2023-11-13'
try:
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

```

## Get data with a weekly interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'week'
to_date = '2023-11-13'
try:
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

```

## Get data with a monthly interval

```python
import upstox_client
from upstox_client.rest import ApiException

api_version = '2.0'

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = 'month'
to_date = '2023-11-13'
try:
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
```
