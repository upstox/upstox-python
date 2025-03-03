# GttPlaceOrderRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Type of GTT order. It can be one of the following: SINGLE refers to a single-leg GTT order MULTIPLE refers to a multi-leg GTT order | 
**quantity** | **int** | Quantity with which the order is to be placed | 
**product** | **str** | Signifies if the order was either Intraday, Delivery, CO or OCO | 
**rules** | [**list[GttRule]**](GttRule.md) | List of rules defining the conditions for each leg in the GTT order | 
**instrument_token** | **str** | Key of the instrument | 
**transaction_type** | **str** | Indicates whether its a buy or sell order | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

