import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.WebsocketApi(upstox_client.ApiClient(configuration))

res = api_instance.get_portfolio_stream_feed_authorize("2.0",order_update=True,holding_update=True,position_update=True)
print("\n\n")
print(res.data.authorized_redirect_uri)