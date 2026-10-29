## Get US market status

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsMarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_us_market_status()
    print(api_response.data)
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_market_status: %s\n" % e)
```

## Get US market holidays for the year

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsMarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_us_holidays()
    for holiday in api_response.data:
        print(holiday._date, holiday.description, holiday.holiday_type)
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_holidays: %s\n" % e)
```

## Get US market holiday on a date

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsMarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    # Empty list when the date is not a holiday
    api_response = api_instance.get_us_holiday('2026-11-26')
    print(api_response.data)
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_holiday: %s\n" % e)
```

## Get US market timings on a date

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsMarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    # Regular and overnight sessions; empty list when the market is closed
    api_response = api_instance.get_us_exchange_timings('2026-11-27')
    print(api_response.data)
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_exchange_timings: %s\n" % e)
```
