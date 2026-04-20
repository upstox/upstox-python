import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

# Get news by instrument_keys category
try:
    api_response = api_instance.get_news("instrument_keys", instrument_keys="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_news with instrument_keys category")
except ApiException as e:
    print("Exception when calling NewsApi->get_news with instrument_keys: %s\n" % e)

# Get news by positions category
try:
    api_response = api_instance.get_news("positions")
    if api_response.status != "success":
        print("error in get_news with positions category")
except ApiException as e:
    print("Exception when calling NewsApi->get_news with positions: %s\n" % e)

# Get news by holdings category
try:
    api_response = api_instance.get_news("holdings")
    if api_response.status != "success":
        print("error in get_news with holdings category")
except ApiException as e:
    print("Exception when calling NewsApi->get_news with holdings: %s\n" % e)

# Get news with pagination
try:
    api_response = api_instance.get_news("instrument_keys", instrument_keys="NSE_EQ|INE669E01016", page_number=1, page_size=5)
    if api_response.status != "success":
        print("error in get_news with pagination")
except ApiException as e:
    print("Exception when calling NewsApi->get_news with pagination: %s\n" % e)

# Model instantiation tests
news_item = upstox_client.NewsItemData(
    heading="Test heading",
    summary="Test summary",
    thumbnail="https://example.com/thumb.jpg",
    article_link="https://example.com/article",
    published_time="2026-04-20T10:00:00Z"
)
if news_item.heading != "Test heading":
    print("error: NewsItemData heading field not set correctly")
if news_item.summary != "Test summary":
    print("error: NewsItemData summary field not set correctly")
if news_item.article_link != "https://example.com/article":
    print("error: NewsItemData article_link field not set correctly")

news_response = upstox_client.GetNewsResponse(
    status="success",
    data=[news_item]
)
if news_response.status != "success":
    print("error: GetNewsResponse status field not set correctly")

news_meta = upstox_client.NewsResponseMetaData()
news_page = upstox_client.NewsResponsePageData()
