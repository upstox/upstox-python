import upstox_client
from upstox_client.rest import ApiException
import const_file

configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin
    api_response = api_instance.get_profile(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)

try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)
