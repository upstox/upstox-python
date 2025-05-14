# upstox_client.TradeProfitAndLossApi

All URIs are relative to *https://api.upstox.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_profit_and_loss_charges**](TradeProfitAndLossApi.md#get_profit_and_loss_charges) | **GET** /trade/profit-loss/charges | Get profit and loss on trades
[**get_trade_wise_profit_and_loss_data**](TradeProfitAndLossApi.md#get_trade_wise_profit_and_loss_data) | **GET** /trade/profit-loss/data | Get Trade-wise Profit and Loss Report Data
[**get_trade_wise_profit_and_loss_meta_data**](TradeProfitAndLossApi.md#get_trade_wise_profit_and_loss_meta_data) | **GET** /trade/profit-loss/metadata | Get profit and loss meta data on trades

# **get_profit_and_loss_charges**
> GetProfitAndLossChargesResponse get_profit_and_loss_charges(segment, financial_year, api_version, from_date=from_date, to_date=to_date)

Get profit and loss on trades

This API gives the charges incurred by users for their trades

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
api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'segment_example' # str | Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives
financial_year = 'financial_year_example' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
api_version = 'api_version_example' # str | API Version Header
from_date = 'from_date_example' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = 'to_date_example' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get profit and loss on trades
    api_response = api_instance.get_profit_and_loss_charges(segment, financial_year, api_version, from_date=from_date, to_date=to_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_profit_and_loss_charges: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment** | **str**| Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives | 
 **financial_year** | **str**| Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122 | 
 **api_version** | **str**| API Version Header | 
 **from_date** | **str**| Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 
 **to_date** | **str**| Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 

### Return type

[**GetProfitAndLossChargesResponse**](GetProfitAndLossChargesResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_wise_profit_and_loss_data**
> GetTradeWiseProfitAndLossDataResponse get_trade_wise_profit_and_loss_data(segment, financial_year, page_number, page_size, api_version, from_date=from_date, to_date=to_date)

Get Trade-wise Profit and Loss Report Data

This API gives the data of the realised Profit and Loss report requested by a user

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
api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'segment_example' # str | Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives
financial_year = 'financial_year_example' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
page_number = 56 # int | Page Number, the pages are starting from 1
page_size = 56 # int | Page size for pagination. The maximum page size value is obtained from P and L report metadata API.
api_version = 'api_version_example' # str | API Version Header
from_date = 'from_date_example' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = 'to_date_example' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_trade_wise_profit_and_loss_data(segment, financial_year, page_number, page_size, api_version, from_date=from_date, to_date=to_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment** | **str**| Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives | 
 **financial_year** | **str**| Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122 | 
 **page_number** | **int**| Page Number, the pages are starting from 1 | 
 **page_size** | **int**| Page size for pagination. The maximum page size value is obtained from P and L report metadata API. | 
 **api_version** | **str**| API Version Header | 
 **from_date** | **str**| Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 
 **to_date** | **str**| Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 

### Return type

[**GetTradeWiseProfitAndLossDataResponse**](GetTradeWiseProfitAndLossDataResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trade_wise_profit_and_loss_meta_data**
> GetTradeWiseProfitAndLossMetaDataResponse get_trade_wise_profit_and_loss_meta_data(segment, financial_year, api_version, from_date=from_date, to_date=to_date)

Get profit and loss meta data on trades

This API gives the data of the realised Profit and Loss report requested by a user

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
api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'segment_example' # str | Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives
financial_year = 'financial_year_example' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
api_version = 'api_version_example' # str | API Version Header
from_date = 'from_date_example' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = 'to_date_example' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get profit and loss meta data on trades
    api_response = api_instance.get_trade_wise_profit_and_loss_meta_data(segment, financial_year, api_version, from_date=from_date, to_date=to_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_meta_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **segment** | **str**| Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives | 
 **financial_year** | **str**| Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122 | 
 **api_version** | **str**| API Version Header | 
 **from_date** | **str**| Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 
 **to_date** | **str**| Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format | [optional] 

### Return type

[**GetTradeWiseProfitAndLossMetaDataResponse**](GetTradeWiseProfitAndLossMetaDataResponse.md)

### Authorization

[OAUTH2](../README.md#OAUTH2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

