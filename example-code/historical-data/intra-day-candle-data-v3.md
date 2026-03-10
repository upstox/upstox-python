## Get data with a 1-minute interval 

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "minutes", "1")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 3-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "minutes", "3")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 5-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "minutes", "5")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 15-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "minutes", "15")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 30-minute interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "minutes", "30")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 1-hour interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "hours", "1")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get data with a 2-hour interval

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "hours", "2")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```

## Get current day data

```python
import upstox_client
apiInstance = upstox_client.HistoryV3Api()
try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE848E01016", "days", "1")
    print(response)
except Exception as e:
    print("Exception when calling HistoryV3Api->get_intra_day_candle_data: %s\n" % e)
```
