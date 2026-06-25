import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.IpoApi(upstox_client.ApiClient(configuration))

# Get IPO listing (no filters)
try:
    api_response = api_instance.get_ipo_listing()
    if api_response.status != "success":
        print("error in IpoApi->get_ipo_listing")
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_listing: %s\n" % e)

# Get IPO listing with filters and pagination
try:
    api_response = api_instance.get_ipo_listing(status="open", issue_type="regular", page_number=1, records=20)
    if api_response.status != "success":
        print("error in IpoApi->get_ipo_listing with filters")
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_listing with filters: %s\n" % e)

# Get IPO details by id (in real usage, pass a slug id from get_ipo_listing)
try:
    api_response = api_instance.get_ipo_details("sample-ipo-slug")
    if api_response.status != "success":
        print("error in IpoApi->get_ipo_details")
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_details: %s\n" % e)

# Model instantiation tests
ipo_listing_data = upstox_client.IpoListingData(symbol="XYZ", status="open")
if ipo_listing_data.symbol != "XYZ":
    print("error: IpoListingData fields not set correctly")

ipo_meta_data = upstox_client.IpoMetaData(page=upstox_client.Pagination(page_number=1))
if ipo_meta_data.page.page_number != 1:
    print("error: IpoMetaData fields not set correctly")

ipo_listing_response = upstox_client.IpoListingResponse(status="success", data=[ipo_listing_data], meta_data=ipo_meta_data)
if ipo_listing_response.status != "success":
    print("error: IpoListingResponse status field not set correctly")

ipo_timeline = upstox_client.IpoTimeline(listing_date="2026-07-01")
if ipo_timeline.listing_date != "2026-07-01":
    print("error: IpoTimeline fields not set correctly")

ipo_registrar_info = upstox_client.IpoRegistrarInfo(name="Registrar Co")
if ipo_registrar_info.name != "Registrar Co":
    print("error: IpoRegistrarInfo fields not set correctly")

ipo_details_data = upstox_client.IpoDetailsData(id="abc", symbol="XYZ", lot_size=10, timeline=ipo_timeline, registrar_info=ipo_registrar_info)
if ipo_details_data.lot_size != 10:
    print("error: IpoDetailsData fields not set correctly")

ipo_details_response = upstox_client.IpoDetailsResponse(status="success", data=ipo_details_data)
if ipo_details_response.status != "success":
    print("error: IpoDetailsResponse status field not set correctly")
