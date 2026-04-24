import json

import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

# Get mutual fund holdings
try:
    api_response = api_instance.get_mutual_fund_holdings()
    if api_response.status != "success":
        print("error in get_mutual_fund_holdings")
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_holdings: %s\n" % e)

# Get mutual fund orders (last 7 days)
try:
    api_response = api_instance.get_mutual_fund_orders()
    if api_response.status != "success":
        print("error in get_mutual_fund_orders")
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_orders: %s\n" % e)

# Get mutual fund orders with filters and pagination
try:
    api_response = api_instance.get_mutual_fund_orders(
        status="complete", transaction_type="BUY", page_number=1, records=10
    )
    if api_response.status != "success":
        print("error in get_mutual_fund_orders with filters")
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_orders (filtered): %s\n" % e)

# Get single mutual fund order (replace order_id with a real id when exercising manually)
try:
    api_response = api_instance.get_mutual_fund_order(order_id="MF-ORDER-001")
    if api_response.status != "success":
        print("error in get_mutual_fund_order")
except ApiException as e:
    json_string = e.body.decode("utf-8")
    data_dict = json.loads(json_string)
    if data_dict.get("errors")[0].get("errorCode") not in ["UDAPI100010", "UDAPI100050"]:
        print("get_mutual_fund_order giving wrong error response")

# Get mutual fund SIPs
try:
    api_response = api_instance.get_mutual_fund_sips()
    if api_response.status != "success":
        print("error in get_mutual_fund_sips")
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_sips: %s\n" % e)

# Get mutual fund SIPs with pagination
try:
    api_response = api_instance.get_mutual_fund_sips(page_number=1, records=10)
    if api_response.status != "success":
        print("error in get_mutual_fund_sips with pagination")
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_sips (paginated): %s\n" % e)

# Model instantiation tests
mf_holding = upstox_client.MutualFundHoldingData(
    quantity=10.5, average_price=100.25, last_price=105.0
)
if mf_holding.quantity != 10.5:
    print("error: MutualFundHoldingData quantity field not set correctly")
if mf_holding.average_price != 100.25:
    print("error: MutualFundHoldingData average_price field not set correctly")
if mf_holding.last_price != 105.0:
    print("error: MutualFundHoldingData last_price field not set correctly")

pagination = upstox_client.Pagination(page_number=1, records=10)
mf_meta = upstox_client.MutualFundMetaData(page=pagination)
if mf_meta.page.page_number != 1:
    print("error: MutualFundMetaData page.page_number not set correctly")

mf_holdings_resp = upstox_client.GetMutualFundHoldingsResponse(
    status="success", data=[mf_holding]
)
if mf_holdings_resp.status != "success":
    print("error: GetMutualFundHoldingsResponse status field not set correctly")

mf_order = upstox_client.MutualFundOrderData()
mf_sip = upstox_client.MutualFundSipData()
mf_orders_resp = upstox_client.GetMutualFundOrdersResponse()
mf_order_details_resp = upstox_client.GetMutualFundOrderDetailsResponse()
mf_sips_resp = upstox_client.GetMutualFundSipsResponse()
