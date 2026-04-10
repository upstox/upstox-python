import upstox_client
import data_token
from upstox_client.rest import ApiException
import json

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

# GET v3/user/get-funds-and-margin
try:
    api_response = api_instance.get_user_fund_margin_v3()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin_v3: %s\n" % e)

# GET v2/user/ip
try:
    api_response = api_instance.get_user_ips()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_ips: %s\n" % e)

# PUT v2/user/ip
body = upstox_client.UpdateUserIpRequest(primary_ip="1.2.3.4")
try:
    api_response = api_instance.update_user_ip(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->update_user_ip: %s\n" % e)

# GET v2/user/kill-switch
try:
    api_response = api_instance.get_kill_switch()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_kill_switch: %s\n" % e)

# POST v2/user/kill-switch
body = [upstox_client.KillSwitchSegmentUpdateRequest(segment="NSE_EQ", action="DISABLE"), upstox_client.KillSwitchSegmentUpdateRequest(segment="NSE_FO", action="DISABLE")]
try:
    print(body)
    api_response = api_instance.update_kill_switch(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->update_kill_switch: %s\n" % e)
