# GttModifyOrderRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Type of GTT order. It can be one of the following: SINGLE refers to a single-leg GTT order MULTIPLE refers to a multi-leg GTT order | 
**quantity** | **int** | Quantity with which the order is to be placed | 
**rules** | [**list[GttRule]**](GttRule.md) | List of rules defining the conditions for each leg in the GTT order | 
**gtt_order_id** | **str** | Unique identifier of the GTT order to be modified | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

