# OrderBookData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exchange** | **str** | Exchange to which the order is associated | [optional] 
**product** | **str** | Shows if the order was either Intraday, Delivery, CoverOrder or OneCancelsOther | [optional] 
**price** | **float** | Price at which the order was placed | [optional] 
**quantity** | **int** | Quantity with which the order was placed | [optional] 
**status** | **str** | Indicates the current status of the order. Valid order status’ are outlined in the table below | [optional] 
**guid** | **str** |  | [optional] 
**tag** | **str** | Tag to uniquely identify an order | [optional] 
**instrument_token** | **str** | Identifier issued by Upstox used for subscribing to live market quotes | [optional] 
**placed_by** | **str** | Uniquely identifies the user | [optional] 
**tradingsymbol** | **str** | Shows the trading symbol of the instrument | [optional] 
**order_type** | **str** | Type of order. It can be one of the following MARKET refers to market order&lt;br&gt;LIMIT refers to Limit Order&lt;br&gt;SL refers to Stop Loss Limit&lt;br&gt;SL-M refers to Stop loss market | [optional] 
**validity** | **str** | Order validity (DAY- Day and IOC- Immediate or Cancel (IOC) order) | [optional] 
**trigger_price** | **float** | If the order was a stop loss order then the trigger price set is mentioned here | [optional] 
**disclosed_quantity** | **int** | The quantity that should be disclosed in the market depth | [optional] 
**transaction_type** | **str** | Indicates whether the order was a buy or sell order | [optional] 
**average_price** | **float** | Average price at which the qty got traded | [optional] 
**filled_quantity** | **int** | The total quantity traded from this particular order | [optional] 
**pending_quantity** | **int** | Pending quantity to be filled | [optional] 
**status_message** | **str** | Indicates the reason when any order is rejected, not modified or cancelled | [optional] 
**status_message_raw** | **str** | Description of the order&#x27;s status as received from RMS | [optional] 
**exchange_order_id** | **str** | Unique order ID assigned by the exchange for the order placed | [optional] 
**parent_order_id** | **str** | In case the order is part of the second or third leg of a CO or OCO, the parent order ID is indicated here | [optional] 
**order_id** | **str** | Unique order ID assigned internally for the order placed | [optional] 
**variety** | **str** | Order complexity | [optional] 
**order_timestamp** | **str** | User readable timestamp at which the order was placed | [optional] 
**exchange_timestamp** | **str** | User readable time at which the order was placed or updated | [optional] 
**is_amo** | **bool** | Signifies if the order is an After Market Order | [optional] 
**order_request_id** | **str** | Apart from 1st order it shows the count of how many requests were sent | [optional] 
**order_ref_id** | **str** | The order reference ID for which the order must be modified | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

