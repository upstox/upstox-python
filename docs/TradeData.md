# TradeData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exchange** | **str** | Exchange to which the order is associated | [optional] 
**product** | **str** | Shows if the order was either Intraday, Delivery, CO or OCO | [optional] 
**tradingsymbol** | **str** | Shows the trading symbol which could be a combination of symbol name, instrument, expiry date etc | [optional] 
**instrument_token** | **str** | Identifier issued by Upstox used for subscribing to live market quotes | [optional] 
**order_type** | **str** | Type of order. It can be one of the following MARKET refers to market order&lt;br&gt;LIMIT refers to Limit Order&lt;br&gt;SL refers to Stop Loss Limit&lt;br&gt;SL-M refers to Stop loss market | [optional] 
**transaction_type** | **str** | Indicates whether the order was a buy or sell order | [optional] 
**quantity** | **int** | The total quantity traded from this particular order | [optional] 
**exchange_order_id** | **str** | Unique order ID assigned by the exchange for the order placed | [optional] 
**order_id** | **str** | Unique order ID assigned internally for the order placed | [optional] 
**exchange_timestamp** | **str** | User readable time at when the trade occurred | [optional] 
**average_price** | **float** | Price at which the traded quantity is traded | [optional] 
**trade_id** | **str** | Trade ID generated from exchange towards traded transaction | [optional] 
**order_ref_id** | **str** | The order reference ID for which the order must be modified | [optional] 
**order_timestamp** | **str** | User readable timestamp at which the order was placed | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

