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

# Get IPO orders (read-only)
try:
    api_response = api_instance.get_ipo_orders()
    if api_response.status != "success":
        print("error in IpoApi->get_ipo_orders")
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_orders: %s\n" % e)

# Get IPO order by id (in real usage, pass an order id from get_ipo_orders)
try:
    api_response = api_instance.get_ipo_order_by_id("sample-ipo-order-id")
    if api_response.status != "success":
        print("error in IpoApi->get_ipo_order_by_id")
except ApiException as e:
    print("Exception when calling IpoApi->get_ipo_order_by_id: %s\n" % e)

# apply_for_ipo/cancel_ipo_order place and withdraw a real IPO application and
# block funds via the UPI mandate. Disabled by default; set
# RUN_DESTRUCTIVE_IPO_TESTS = True to exercise them against a real account.
RUN_DESTRUCTIVE_IPO_TESTS = False
if RUN_DESTRUCTIVE_IPO_TESTS:
    try:
        # Apply for IPO — id/upi/category/bids are all required, max 3 bids
        body = upstox_client.IpoApplyRequest(
            id="sample-ipo-slug",
            upi="someone@upi",
            category="IND",
            bids=[upstox_client.IpoBidRequest(quantity=10, price=150.0)]
        )
        api_response = api_instance.apply_for_ipo(body)
        ipo_order_id = api_response.data.order_id

        # Cancel IPO order
        api_response = api_instance.cancel_ipo_order(ipo_order_id)
        print("ipo apply/cancel cycle:", api_response.status)
    except ApiException as e:
        print("Exception when calling IpoApi ipo order write ops: %s\n" % e)

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

# Model instantiation tests — IPO orders

ipo_investor_type = upstox_client.IpoInvestorType(category="IND", description="Individual Investor")
if ipo_investor_type.category != "IND":
    print("error: IpoInvestorType fields not set correctly")

# investors is a typed list on both IpoDetailsData and IpoListingData
ipo_details_data_with_investors = upstox_client.IpoDetailsData(id="abc", investors=[ipo_investor_type])
if ipo_details_data_with_investors.investors[0].category != "IND":
    print("error: IpoDetailsData investors field not set correctly")

ipo_listing_data_with_investors = upstox_client.IpoListingData(symbol="XYZ", investors=[ipo_investor_type])
if ipo_listing_data_with_investors.investors[0].description != "Individual Investor":
    print("error: IpoListingData investors field not set correctly")

ipo_bid_request = upstox_client.IpoBidRequest(quantity=10, price=150.5)
if ipo_bid_request.quantity != 10 or ipo_bid_request.price != 150.5:
    print("error: IpoBidRequest fields not set correctly")

ipo_apply_request = upstox_client.IpoApplyRequest(id="sample-ipo-slug", upi="someone@upi", category="IND", bids=[ipo_bid_request])
if ipo_apply_request.upi != "someone@upi" or len(ipo_apply_request.bids) != 1:
    print("error: IpoApplyRequest fields not set correctly")

ipo_apply_data = upstox_client.IpoApplyData(order_id="O1")
if ipo_apply_data.order_id != "O1":
    print("error: IpoApplyData fields not set correctly")

ipo_apply_response = upstox_client.IpoApplyResponse(status="success", data=ipo_apply_data)
if ipo_apply_response.status != "success":
    print("error: IpoApplyResponse status field not set correctly")

ipo_order_bid = upstox_client.IpoOrderBid(quantity=10, price=150.5, amount=1505.0, message="accepted")
if ipo_order_bid.amount != 1505.0:
    print("error: IpoOrderBid fields not set correctly")

ipo_order_data = upstox_client.IpoOrderData(id="abc", symbol="XYZ", exchange="NSE", order_id="O1", order_status="COMPLETE", category="IND", issue_type="regular", units_allotted=10, bids=[ipo_order_bid])
if ipo_order_data.order_id != "O1" or ipo_order_data.units_allotted != 10:
    print("error: IpoOrderData fields not set correctly")

ipo_order_response = upstox_client.IpoOrderResponse(status="success", data=[ipo_order_data], meta_data=ipo_meta_data)
if ipo_order_response.status != "success":
    print("error: IpoOrderResponse status field not set correctly")

ipo_order_detail_response = upstox_client.IpoOrderDetailResponse(status="success", data=ipo_order_data)
if ipo_order_detail_response.data.symbol != "XYZ":
    print("error: IpoOrderDetailResponse fields not set correctly")

ipo_cancel_data = upstox_client.IpoCancelData(order_id="O1", status="CANCELLED")
if ipo_cancel_data.status != "CANCELLED":
    print("error: IpoCancelData fields not set correctly")

ipo_cancel_response = upstox_client.IpoCancelResponse(status="success", data=ipo_cancel_data)
if ipo_cancel_response.data.order_id != "O1":
    print("error: IpoCancelResponse fields not set correctly")
