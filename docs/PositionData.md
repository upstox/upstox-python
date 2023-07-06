# PositionData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exchange** | **str** | Exchange to which the order is associated | [optional] 
**multiplier** | **float** | The quantity/lot size multiplier used for calculating P&amp;Ls | [optional] 
**value** | **float** | Net value of the position | [optional] 
**pnl** | **float** | Profit and loss - net returns on the position | [optional] 
**product** | **str** | Shows if the order was either Intraday, Delivery, CO or OCO | [optional] 
**instrument_token** | **str** | Key issued by Upstox for the instrument | [optional] 
**average_price** | **float** | Average price at which the net position quantity was acquired | [optional] 
**buy_value** | **float** | Net value of the bought quantities | [optional] 
**overnight_quantity** | **int** | Quantity held previously and carried forward over night | [optional] 
**day_buy_value** | **float** | Amount at which the quantity is bought during the day | [optional] 
**day_buy_price** | **float** | Average price at which the day qty was bought. Default is empty string | [optional] 
**overnight_buy_amount** | **float** | Amount at which the quantity was bought in the previous session | [optional] 
**overnight_buy_quantity** | **int** | Quantity bought in the previous session | [optional] 
**day_buy_quantity** | **int** | Quantity bought during the day | [optional] 
**day_sell_value** | **float** | Amount at which the quantity is sold during the day | [optional] 
**day_sell_price** | **float** | Average price at which the day quantity was sold | [optional] 
**overnight_sell_amount** | **float** | Amount at which the quantity was sold in the previous session | [optional] 
**overnight_sell_quantity** | **int** | Quantity sold short in the previous session | [optional] 
**day_sell_quantity** | **int** | Quantity sold during the day | [optional] 
**quantity** | **int** | Quantity left after nullifying Day and CF buy quantity towards Day and CF sell quantity | [optional] 
**last_price** | **float** | Last traded market price of the instrument | [optional] 
**unrealised** | **float** | Day PnL generated against open positions | [optional] 
**realised** | **float** | Day PnL generated against closed positions | [optional] 
**sell_value** | **float** | Net value of the sold quantities | [optional] 
**tradingsymbol** | **str** | Shows the trading symbol of the instrument | [optional] 
**close_price** | **float** | Closing price of the instrument from the last trading day | [optional] 
**buy_price** | **float** | Average price at which quantities were bought | [optional] 
**sell_price** | **float** | Average price at which quantities were sold | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

