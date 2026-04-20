import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

# Get news for specific instruments
try:
    api_response = api_instance.get_news(
        category="instrument_keys",
        instrument_keys="NSE_EQ|INE669E01016"
    )
    print("News for instrument_keys:", api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)

# Get news based on user's current positions
try:
    api_response = api_instance.get_news(category="positions")
    print("News for positions:", api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)

# Get news based on user's holdings
try:
    api_response = api_instance.get_news(category="holdings")
    print("News for holdings:", api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)

# Get news with pagination
try:
    api_response = api_instance.get_news(
        category="instrument_keys",
        instrument_keys="NSE_EQ|INE669E01016",
        page_number=1,
        page_size=10
    )
    print("News with pagination:", api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news with pagination: %s\n" % e)
