# MarketQuoteSymbol

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ohlc** | [**Ohlc**](Ohlc.md) |  | [optional] 
**depth** | [**DepthMap**](DepthMap.md) |  | [optional] 
**timestamp** | **str** | Time in milliseconds at which the feeds was updated | [optional] 
**instrument_token** | **str** | Key issued by Upstox for the instrument | [optional] 
**symbol** | **str** | Shows the trading symbol of the instrument | [optional] 
**last_price** | **float** | The last traded price of symbol | [optional] 
**volume** | **int** | The volume traded today on symbol | [optional] 
**average_price** | **float** | Average price | [optional] 
**oi** | **float** | Total number of outstanding contracts held by market participants exchange-wide (only F&amp;O) | [optional] 
**net_change** | **float** | The absolute change from yesterday&#x27;s close to last traded price | [optional] 
**total_buy_quantity** | **float** | The total number of bid quantity available for trading | [optional] 
**total_sell_quantity** | **float** | The total number of ask quantity available for trading | [optional] 
**lower_circuit_limit** | **float** | The lower circuit of symbol | [optional] 
**upper_circuit_limit** | **float** | The upper circuit of symbol | [optional] 
**last_trade_time** | **str** | Time in milliseconds at which last trade happened | [optional] 
**oi_day_high** | **float** |  | [optional] 
**oi_day_low** | **float** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

