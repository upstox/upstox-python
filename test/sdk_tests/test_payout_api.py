import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

# Get payout history (read-only)
try:
    api_response = api_instance.get_payout_history()
    if api_response.status != "success":
        print("error in UserApi->get_payout_history")
except ApiException as e:
    print("Exception when calling UserApi->get_payout_history: %s\n" % e)

# Get payout modes (read-only)
try:
    api_response = api_instance.get_payout_modes()
    if api_response.status != "success":
        print("error in UserApi->get_payout_modes")
except ApiException as e:
    print("Exception when calling UserApi->get_payout_modes: %s\n" % e)

# Initiate/Modify/Cancel payout move real funds. Disabled by default; set
# RUN_DESTRUCTIVE_PAYOUT_TESTS = True to exercise them against a real account.
RUN_DESTRUCTIVE_PAYOUT_TESTS = False
if RUN_DESTRUCTIVE_PAYOUT_TESTS:
    try:
        body = upstox_client.InitiatePayoutRequest(mode="IMPS", amount=1.0)
        api_response = api_instance.initiate_payout(body)
        transaction_id = api_response.data.transaction_id

        modify_body = upstox_client.ModifyPayoutRequest(amount=2.0)
        api_response = api_instance.modify_payout(modify_body, transaction_id)

        api_response = api_instance.cancel_payout(transaction_id)
        if api_response.status != "success":
            print("error in UserApi payout initiate/modify/cancel cycle")
    except ApiException as e:
        print("Exception when calling UserApi payout write ops: %s\n" % e)

# Model instantiation tests
initiate_payout_request = upstox_client.InitiatePayoutRequest(mode="IMPS", amount=500.0)
if initiate_payout_request.amount != 500.0:
    print("error: InitiatePayoutRequest fields not set correctly")

modify_payout_request = upstox_client.ModifyPayoutRequest(amount=750.0)
if modify_payout_request.amount != 750.0:
    print("error: ModifyPayoutRequest fields not set correctly")

payout_details = upstox_client.PayoutDetails(status="SUCCESS", transaction_id="T1", amount=500.0)
if payout_details.transaction_id != "T1":
    print("error: PayoutDetails fields not set correctly")

payout_details_response = upstox_client.PayoutDetailsResponse(status="success", data=payout_details)
if payout_details_response.status != "success":
    print("error: PayoutDetailsResponse status field not set correctly")

payout_modes_data = upstox_client.PayoutModesData()
if payout_modes_data is None:
    print("error: PayoutModesData instantiation failed")

payout_modes_response = upstox_client.PayoutModesResponse(status="success", data=payout_modes_data)
if payout_modes_response.status != "success":
    print("error: PayoutModesResponse status field not set correctly")
