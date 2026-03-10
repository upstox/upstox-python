## Get data with a 1-minute interval 

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "minutes", "1", "2025-01-02", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a 3-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "minutes", "3", "2025-01-02", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a 15-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "minutes", "15", "2025-01-04", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a 1-hour interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "hours", "1", "2025-02-01", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a 4-hour interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "hours", "4", "2025-02-01", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a daily interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "days", "1", "2025-03-01", "2025-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a weekly interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "weeks", "1", "2025-01-01", "2024-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```

## Get data with a monthly interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE848E01016", "months", "1", "2025-01-01", "2010-01-01")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_historical_candle_data1: %s\n" % e)
```
