## Get smartlist options

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    # asset_type: INDEX | STOCK | COMMODITY
    # category: TOP_TRADED, MOST_ACTIVE, OI_GAINERS, OI_LOSERS, PRICE_GAINERS,
    #           PRICE_LOSERS, IV_GAINERS, IV_LOSERS, UNDER_5000, UNDER_10000
    api_response = api_instance.get_smartlist_options(
        asset_type='INDEX',
        category='TOP_TRADED',
        page_number=1,
        page_size=50
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_options: %s\n" % e)
```

## Get smartlist futures

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    # asset_type: INDEX | STOCK | COMMODITY
    # category: TOP_TRADED, MOST_ACTIVE, OI_GAINERS, OI_LOSERS, PRICE_GAINERS,
    #           PRICE_LOSERS, PREMIUM, DISCOUNT
    api_response = api_instance.get_smartlist_futures(
        asset_type='STOCK',
        category='MOST_ACTIVE',
        page_number=1,
        page_size=50
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_futures: %s\n" % e)
```

## Get smartlist MTF

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))

try:
    # MTF (Margin Trade Funding) stocks, enriched with live LTP
    api_response = api_instance.get_smartlist_mtf(page_number=1, page_size=50)
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_mtf: %s\n" % e)
```
