## Get full market quote

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For a single instrument
    response = apiInstance.get_full_market_quote_v3(instrument_key="NSE_EQ|INE848E01016")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3: %s\n" % e)
```

## Get full market quote for multiple instrument keys

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For multiple instruments (up to 500 in one call)
    response = apiInstance.get_full_market_quote_v3(
        instrument_key="NSE_EQ|INE848E01016,NSE_EQ|INE669E01016")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3: %s\n" % e)
```

## Read fields from the full market quote response

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_full_market_quote_v3(instrument_key="NSE_EQ|INE848E01016")

    # response.data is a dict keyed by "<exchange>:<trading_symbol>"
    for key, quote in response.data.items():
        print(key)
        print("  symbol                :", quote.symbol)
        print("  instrument_token      :", quote.instrument_token)
        print("  last_price            :", quote.last_price)
        print("  volume                :", quote.volume)
        print("  average_price         :", quote.average_price)
        print("  net_change            :", quote.net_change)
        print("  prev_close_price      :", quote.prev_close_price)
        print("  lower_circuit_limit   :", quote.lower_circuit_limit)
        print("  upper_circuit_limit   :", quote.upper_circuit_limit)
        print("  year_high / year_low  :", quote.year_high, "/", quote.year_low)
        print("  oi / previous_oi      :", quote.oi, "/", quote.previous_oi)
        print("  cas_eligible          :", quote.cas_eligible)

        # Nested OHLC snapshot
        print("  ohlc                  :", quote.ohlc.open, quote.ohlc.high,
              quote.ohlc.low, quote.ohlc.close)

        # Nested market depth (top 5 bids and asks)
        for level in quote.depth.buy:
            print("  bid:", level.price, level.quantity, level.orders)
        for level in quote.depth.sell:
            print("  ask:", level.price, level.quantity, level.orders)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3: %s\n" % e)
```
