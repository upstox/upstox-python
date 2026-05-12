import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.FundamentalsApi(upstox_client.ApiClient(configuration))
isin = 'INE002A01018'  # Reliance Industries

try:
    api_response = api_instance.get_company_profile(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_company_profile not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_company_profile: %s\n" % e)

try:
    api_response = api_instance.get_balance_sheet(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_balance_sheet not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_balance_sheet: %s\n" % e)

try:
    api_response = api_instance.get_cash_flow(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_cash_flow not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_cash_flow: %s\n" % e)

try:
    api_response = api_instance.get_income_statement(isin)
    print(api_response)
    if api_response.status != "success":
        print("FundamentalsApi->get_income_statement not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_income_statement: %s\n" % e)

try:
    api_response = api_instance.get_key_ratios(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_key_ratios not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_key_ratios: %s\n" % e)

try:
    api_response = api_instance.get_share_holdings(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_share_holdings not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_share_holdings: %s\n" % e)

try:
    api_response = api_instance.get_corporate_actions(isin)
    if api_response.status != "success":
        print("FundamentalsApi->get_corporate_actions not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_corporate_actions: %s\n" % e)

try:
    api_response = api_instance.get_competitors('NSE_EQ|INE002A01018')
    if api_response.status != "success":
        print("FundamentalsApi->get_competitors not returning success")
except ApiException as e:
    print("Exception when calling FundamentalsApi->get_competitors: %s\n" % e)
