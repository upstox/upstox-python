# swagger_client.ChargeApi

All URIs are relative to *https://api-v2.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_brokerage**](ChargeApi.md#get_brokerage) | **GET** /charges/brokerage | Brokerage details

# **get_brokerage**
> GetBrokerageResponse get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)

Brokerage details

Compute Brokerage Charges

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
api_instance = swagger_client.ChargeApi(swagger_client.ApiClient(configuration))
instrument_token = 'instrument_token_example' # str | Key of the instrument
quantity = 56 # int | Quantity with which the order is to be placed
product = 'product_example' # str | Product with which the order is to be placed
transaction_type = 'transaction_type_example' # str | Indicates whether its a BUY or SELL order
price = 3.4 # float | Price with which the order is to be placed
api_version = 'api_version_example' # str | API Version Header

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instrument_token** | **str**| Key of the instrument | 
 **quantity** | **int**| Quantity with which the order is to be placed | 
 **product** | **str**| Product with which the order is to be placed | 
 **transaction_type** | **str**| Indicates whether its a BUY or SELL order | 
 **price** | **float**| Price with which the order is to be placed | 
 **api_version** | **str**| API Version Header | 

### Return type

[**GetBrokerageResponse**](GetBrokerageResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

