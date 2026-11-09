## Get US funds

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksFundsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_us_funds()
    print('available to trade (USD):', api_response.data.available_to_trade)
    print('exchange rate:', api_response.data.exchange_rate)
except ApiException as e:
    print("Exception when calling UsStocksFundsApi->get_us_funds: %s\n" % e)
```

## Get US holdings

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksPortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_us_holdings()
    for holding in api_response.data:
        print(holding.trading_symbol, holding.quantity, holding.pnl)
except ApiException as e:
    print("Exception when calling UsStocksPortfolioApi->get_us_holdings: %s\n" % e)
```
