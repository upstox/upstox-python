import upstox_client
from upstox_client.rest import ApiException
import const_file
configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))
body = upstox_client.ConvertPositionRequest(instrument_token= "NSE_EQ|INE528G01035",quantity=1,new_product="I",old_product="D",transaction_type="BUY")
api_version = '2.0'

try:
    # Convert Positions
    api_response = api_instance.convert_positions(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling PortfolioApi->convert_positions: %s\n" % e)

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holdings(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_positions(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
