## Get IPO listing

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_ipo_listing()
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_listing: %s\n" % e)
```

## Get IPO listing with filters and pagination

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

try:
    # status: open | closed | listed | upcoming
    # issue_type: regular | sme
    api_response = api_instance.get_ipo_listing(
        status='open',
        issue_type='regular',
        page_number=1,
        records=20
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_listing: %s\n" % e)
```

## Get IPO details by id

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# `id` is the IPO slug id returned by get_ipo_listing
ipo_id = '{ipo_slug_id}'

try:
    api_response = api_instance.get_ipo_details(ipo_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_details: %s\n" % e)
```
