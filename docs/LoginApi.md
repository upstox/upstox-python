# upstox_client.LoginApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authorize**](LoginApi.md#authorize) | **GET** /login/authorization/dialog | Authorize API
[**logout**](LoginApi.md#logout) | **DELETE** /logout | Logout
[**token**](LoginApi.md#token) | **POST** /login/authorization/token | Get token API

# **authorize**
> authorize(client_id, redirect_uri, api_version, state=state, scope=scope)

Authorize API

This provides details on the login endpoint.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.LoginApi()
client_id = 'client_id_example' # str | 
redirect_uri = 'redirect_uri_example' # str | 
api_version = 'api_version_example' # str | API Version Header
state = 'state_example' # str |  (optional)
scope = 'scope_example' # str |  (optional)

try:
    # Authorize API
    api_instance.authorize(client_id, redirect_uri, api_version, state=state, scope=scope)
except ApiException as e:
    print("Exception when calling LoginApi->authorize: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**|  | 
 **redirect_uri** | **str**|  | 
 **api_version** | **str**| API Version Header | 
 **state** | **str**|  | [optional] 
 **scope** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout**
> LogoutResponse logout(api_version)

Logout

Logout

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = upstox_client.LoginApi(upstox_client.ApiClient(configuration))
api_version = 'api_version_example' # str | API Version Header

try:
    # Logout
    api_response = api_instance.logout(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->logout: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 

### Return type

[**LogoutResponse**](LogoutResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **token**
> TokenResponse token(api_version, code=code, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, grant_type=grant_type)

Get token API

This API provides the functionality to obtain opaque token from authorization_code exchange and also provides the user’s profile in the same response.

### Example
```python
from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = upstox_client.LoginApi()
api_version = 'api_version_example' # str | API Version Header
code = 'code_example' # str |  (optional)
client_id = 'client_id_example' # str |  (optional)
client_secret = 'client_secret_example' # str |  (optional)
redirect_uri = 'redirect_uri_example' # str |  (optional)
grant_type = 'grant_type_example' # str |  (optional)

try:
    # Get token API
    api_response = api_instance.token(api_version, code=code, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, grant_type=grant_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_version** | **str**| API Version Header | 
 **code** | **str**|  | [optional] 
 **client_id** | **str**|  | [optional] 
 **client_secret** | **str**|  | [optional] 
 **redirect_uri** | **str**|  | [optional] 
 **grant_type** | **str**|  | [optional] 

### Return type

[**TokenResponse**](TokenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

