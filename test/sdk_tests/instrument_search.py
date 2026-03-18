import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.InstrumentsApi(upstox_client.ApiClient(configuration))

# Basic search with just query
try:
    api_response = api_instance.search_instrument("Nifty 50")
    
    if api_response.status != "success":
        print("error in search_instrument basic query")
except ApiException as e:
    print("Exception when calling InstrumentsApi->search_instrument: %s\n" % e)

# Search with exchange filter
try:
    api_response = api_instance.search_instrument("Reliance", exchanges="NSE")
   
    if api_response.status != "success":
        print("error in search_instrument with exchange filter")
except ApiException as e:
    print("Exception when calling InstrumentsApi->search_instrument with exchange: %s\n" % e)

# Search with segment filter
try:
    api_response = api_instance.search_instrument("TCS", segments="EQ")
    
    if api_response.status != "success":
        print("error in search_instrument with segment filter")
except ApiException as e:
    print("Exception when calling InstrumentsApi->search_instrument with segment: %s\n" % e)

# Search with instrument type filter
try:
    api_response = api_instance.search_instrument("Nifty", instrument_types="INDEX")
    
    if api_response.status != "success":
        print("error in search_instrument with instrument type filter")
except ApiException as e:
    print("Exception when calling InstrumentsApi->search_instrument with instrument_types: %s\n" % e)

# Search with pagination
try:
    api_response = api_instance.search_instrument("HDFC", page_number=1, records=5)
    
    if api_response.status != "success":
        print("error in search_instrument with pagination")
except ApiException as e:
    print("Exception when calling InstrumentsApi->search_instrument with pagination: %s\n" % e)
