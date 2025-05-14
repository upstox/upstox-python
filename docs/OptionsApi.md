# swagger_client.OptionsApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_option_contracts**](OptionsApi.md#get_option_contracts) | **GET** /v2/option/contract | Get option contracts
[**get_put_call_option_chain**](OptionsApi.md#get_put_call_option_chain) | **GET** /v2/option/chain | Get option chain

# **get_option_contracts**
> GetOptionContractResponse get_option_contracts(instrument_key, expiry_date=expiry_date)

Get option contracts

This API provides the functionality to retrieve the option contracts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.OptionsApi(swagger_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Instrument key for an underlying symbol
expiry_date = 'expiry_date_example' # str | Expiry date in format: YYYY-mm-dd (optional)

try:
    # Get option contracts
    api_response = api_instance.get_option_contracts(instrument_key, expiry_date=expiry_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptionsApi->get_option_contracts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Instrument key for an underlying symbol | 
 **expiry_date** | **str**| Expiry date in format: YYYY-mm-dd | [optional] 

### Return type

[**GetOptionContractResponse**](GetOptionContractResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_put_call_option_chain**
> GetOptionChainResponse get_put_call_option_chain(instrument_key, expiry_date)

Get option chain

This API provides the functionality to retrieve the option chain

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.OptionsApi(swagger_client.ApiClient(configuration))
instrument_key = 'instrument_key_example' # str | Instrument key for an underlying symbol
expiry_date = 'expiry_date_example' # str | Expiry date in format: YYYY-mm-dd

try:
    # Get option chain
    api_response = api_instance.get_put_call_option_chain(instrument_key, expiry_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptionsApi->get_put_call_option_chain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_key** | **str**| Instrument key for an underlying symbol | 
 **expiry_date** | **str**| Expiry date in format: YYYY-mm-dd | 

### Return type

[**GetOptionChainResponse**](GetOptionChainResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

