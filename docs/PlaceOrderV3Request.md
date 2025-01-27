# PlaceOrderV3Request

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quantity** | **int** | Quantity with which the order is to be placed | 
**product** | **str** | Signifies if the order was either Intraday, Delivery, CO or OCO | 
**validity** | **str** | It can be one of the following - DAY(default), IOC | 
**price** | **float** | Price at which the order will be placed | 
**tag** | **str** |  | [optional] 
**slice** | **bool** |  | [optional] 
**instrument_token** | **str** | Key of the instrument | 
**order_type** | **str** | Type of order. It can be one of the following MARKET refers to market order LIMIT refers to Limit Order SL refers to Stop Loss Limit SL-M refers to Stop Loss Market | 
**transaction_type** | **str** | Indicates whether its a buy or sell order | 
**disclosed_quantity** | **int** | The quantity that should be disclosed in the market depth | 
**trigger_price** | **float** | If the order is a stop loss order then the trigger price to be set is mentioned here | 
**is_amo** | **bool** | Signifies if the order is an After Market Order | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

