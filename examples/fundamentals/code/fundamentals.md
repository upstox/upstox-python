## Get Company Profile

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_company_profile('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_company_profile: %s\n" % e)
```

## Get Key Ratios

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_key_ratios('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_key_ratios: %s\n" % e)
```

## Get Balance Sheet

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_balance_sheet('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_balance_sheet: %s\n" % e)
```

## Get Income Statement

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_income_statement('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_income_statement: %s\n" % e)
```

## Get Cash Flow

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_cash_flow('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_cash_flow: %s\n" % e)
```

## Get Competitors

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_competitors('NSE_EQ|INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_competitors: %s\n" % e)
```

## Get Corporate Actions

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_corporate_actions('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_corporate_actions: %s\n" % e)
```

## Get Share Holdings

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_share_holdings('INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_share_holdings: %s\n" % e)
```
