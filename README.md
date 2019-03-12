
# Python SDK for Upstox API

The official Python library for communicating with the Upstox APIs.

Upstox Python library provides an easy to use wrapper over the HTTPs APIs.

The HTTP calls have been converted to methods and JSON responses are wrapped into Python-compatible objects.

Websocket connections are handled automatically with the library

## Installation

This module is installed via pip:

```
pip install upstox
```

To force upgrade existing installations:
```
pip uninstall upstox
pip --no-cache-dir install --upgrade upstox
```

### Prerequisites

Python 2.x or 3.x

Also, you need the following modules:

* `future`
* `websocket_client (version 0.40.0)`
* `requests` 

The modules can also be installed using `pip`
The specific version of websocket_client is needed for proper functioning of live feed.
To install version 0.40.0 of websocket client use pip as follows:
`pip install websocket_client=0.40.0`

## Getting started with API

### Overview
There are two classes in the library: Session, and Upstox. The Session class is used to retrieve an access token from the server. An access token is valid for 24 hours.
With an access token, you can instantiate an Upstox object. Ideally you only need to create a Session object once every day. After you have the access token, you can store it
separately for re-use.

### REST Documentation
The original REST API that this SDK is based on is available online.
   [Upstox API REST documentation](https://upstox.com/developer/api/v1/docs/)

### Sample Program
An interactive Python program to test your connectivity and show functionality is available on [Gist](https://gist.github.com/svishi/ba0ee4e08f1e2364addfe76c5b2ef7d7).

## Using the API

### Get an access token
1. Import Upstox
```python
from upstox_api.api import *
```

2. Create a Session object with your `api_key`, `redirect_uri` and `api_secret`
```python
s = Session ('your_api_key')
s.set_redirect_uri ('your_redirect_uri')
s.set_api_secret ('your_api_secret')
```

3. Get the login URL so you can login with your Upstox UCC ID and password.
```python
print (s.get_login_url())
## this will return a URL such as https://api.upstox.com/index/dialog/authorize?apiKey={your_api_key}&redirect_uri={your_redirect_uri}&response_type=code
```

4. Login to the URL and set the code returned by the login response in your Session object
```python
s.set_code ('your_code_from_login_response')
```

5. Retrieve your access token
```python
access_token = s.retrieve_access_token()
print ('Received access_token: %s' % access_token)
```

### Establish a session
1. Once you have your `access_token`, you can create an Upstox object with your `access_token` and `api_key`.
```python
u = Upstox ('your_api_key', access_token)
```

2. You can run commands here to check your connectivity
```python
print (u.get_balance()) # get balance / margin limits
print (u.get_profile()) # get profile
print (u.get_holdings()) # get holdings
print (u.get_positions()) # get positions
```

### Get master contracts
Getting master contracts allow you to search for instruments by symbol name and place orders.
Master contracts are stored as an OrderedDict by token number and by symbol name. Whenever you get a trade update, order update, or quote update, the library will check if master contracts are loaded. If they are, it will attach the instrument object directly to the update.

```python
u.get_master_contract('NSE_EQ') # get contracts for NSE EQ
u.get_master_contract('NSE_FO') # get contracts for NSE FO
u.get_master_contract('NSE_INDEX') # get contracts for NSE INDEX
u.get_master_contract('BSE_EQ') # get contracts for BSE EQ
u.get_master_contract('BCD_FO') # get contracts for BCD FO
u.get_master_contract('BSE_INDEX') # get contracts for BSE INDEX
u.get_master_contract('MCX_INDEX') # get contracts for MCX INDEX
u.get_master_contract('MCX_FO') # get contracts for MCX FO
```

### Search for symbols
Symbols can be retrieved in multiple ways. Once you have the master contract loaded for an exchange, you can search for an instrument in many ways.

Search for a single instrument by it's name:
```python
tatasteel_nse_eq = u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL')
reliance_nse_eq = u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE')
ongc_bse_eq = u.get_instrument_by_symbol('BSE_EQ', 'ONGC')
mcxagri_mcx_index = u.get_instrument_by_symbol('MCX_INDEX', 'MCXAGRI')
india_vix_nse_index = u.get_instrument_by_symbol('NSE_INDEX', 'INDIA_VIX')
sensex_nse_index = u.get_instrument_by_symbol('BSE_INDEX', 'SENSEX')
```

Search for a single instrument by it's token number (generally useful only for BSE Equities):
```python
ongc_bse_eq = u.get_instrument_by_token('BSE_EQ', 500312)
reliance_bse_eq = u.get_instrument_by_token('BSE_EQ', 500325)
acc_nse_eq = u.get_instrument_by_token('NSE_EQ', 22)
```

Search for multiple instruments by matching the name
```python
all_tata_companies_on_bse = u.search_instruments('BSE_EQ', 'tata')
```

#### Instrument object
Instruments are represented by instrument objects. These are named-tuples that are created by the `get_master_contract` function. They are used when placing an order and searching for an instrument. The structure of an instrument tuple is as follows:
```python
Instrument = namedtuple('Instrument', ['exchange', 'token', 'parent_token', 'symbol',
                                       'name', 'closing_price', 'expiry', 'strike_price',
                                       'tick_size', 'lot_size', 'instrument_type', 'isin'])
```

All instruments have the fields mentioned above. Wherever a field is not applicable for an instrument (for example, equity instruments don't have strike prices), that value will be `None`

### Quote update
Once you have master contracts loaded, you can easily subscribe to quote updates.

#### Two types of feed data available
You can either subscribe for a full quote update or an LTP quote update. Using the `LiveFeedType` object, you can specify whether you want the full feed (`LiveFeedType.Full`) or just the LTP feed (`LiveFeedType.LTP`)

#### Get current market price
```python
u.get_live_feed(u.get_instrument_by_symbol('NSE_EQ', 'ACC'), LiveFeedType.Full)
u.get_live_feed(u.get_instrument_by_symbol('BSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
```

#### Subscribe to a live feed
```python
u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
u.subscribe(u.get_instrument_by_symbol('BSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
```
Subscribe to multiple instruments in a single call. Give an array of instruments of same exchange to be subscribed.
Provide additional parameter exchange to define instrument of which exchange you want to subscribe
```python
u.subscribe([u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), u.get_instrument_by_symbol('NSE_EQ', 'ACC')], LiveFeedType.Full, "NSE_EQ")
```

Start getting live feed via socket


```python
def socket_connect():


    u.get_master_contract('NSE_FO')
    print ("Socket connect code executed")

    def event_handler_quote_update(message):
        print("********QUOTE UPDATE****************")
        # print(message)
        print("\n\n")

    u.set_on_quote_update(event_handler_quote_update)

    def event_handler_order_update(message):
        print("********ORDER UPDATE****************")
        print(message)
        print("\n\n")

    u.set_on_order_update(event_handler_order_update)

    def event_handler_trade_update(message):
        print("********TRADE UPDATE****************")
        print(message)
        print("\n\n")

    u.set_on_trade_update(event_handler_trade_update)

    def event_handler_error(err):
        print("********ERROR HANDLER****************")
        print(err)
        print("\n\n")

    u.set_on_error(event_handler_error)

    def event_handler_socket_disconnect():
        print("********SOCKET DISCONNECTED****************")
        print("\n\n")
        # Uncomment For Reconnection Logic
        u.start_websocket(False)

    u.set_on_disconnect(event_handler_socket_disconnect)

    # u.unsubscribe(u.get_instrument_by_symbol('NSE_EQ', 'ONGC'), LiveFeedType.LTP)
    # u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'ONGC'), LiveFeedType.LTP)

    u.start_websocket(False)
```

#### Unsubscribe to a live feed
Unsubscribe to an existing live feed
```python
u.unsubscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
u.unsubscribe(u.get_instrument_by_symbol('BSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
```
Unsubscribe to multiple instruments in a single call. Give an array of instruments of same exchange to be subscribed also provide additional parameter exchange to define instrument of which exchange you want to unsubscribe
```python
u.unsubscribe([u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), u.get_instrument_by_symbol('NSE_EQ', 'ACC')], LiveFeedType.Full, "NSE_EQ")
```

#### Get All Subscribed Symbols
```python
u.get_subscriptions(live_feed_type=LiveFeedType.Full)  # Full
u.get_subscriptions(live_feed_type=LiveFeedType.LTP)  # LTP
u.get_subscriptions() # All
```

### Get historical data
Get historical OHLC data for any symbol
```python
u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), OHLCInterval.Minute_10, datetime.datetime.strptime('01/07/2017', '%d/%m/%Y').date(), datetime.datetime.strptime('07/07/2017', '%d/%m/%Y').date())
```

### Place an order
Place limit, market, SL, SL-M, AMO, OCO/BO, CO orders

```python
print (u.get_profile())
u.get_master_contract('nse_eq') # get contracts for NSE EQ

# TransactionType.Buy, OrderType.Market, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  #transaction_type
              u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  #instrument
              1,  # quantity
              OrderType.Market,  # order_type
              ProductType.Delivery,  # product_type
              0.0,  # price
              None,  # trigger_price
              0,  # disclosed_quantity
              DurationType.DAY, # duration
              None, # stop_loss
              None, # square_off
              None )# trailing_ticks
   )

# TransactionType.Buy, OrderType.Market, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
u.place_order(TransactionType.Buy,  # transaction_type
              u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
              1,  # quantity
              OrderType.Market,  # order_type
              ProductType.Intraday,  # product_type
              0.0,  # price
              None,  # trigger_price
              0,  # disclosed_quantity
              DurationType.DAY,  # duration
              None,  # stop_loss
              None,  # square_off
              None  )# trailing_ticks
)

# TransactionType.Buy, OrderType.Market, ProductType.CoverOrder

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
u.place_order(TransactionType.Buy,  # transaction_type
              u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
              1,  # quantity
              OrderType.Market,  # order_type
              ProductType.CoverOrder,  # product_type
              0.0,  # price
              7.5,  # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
              0,  # disclosed_quantity
              DurationType.DAY,  # duration
              None,  # stop_loss
              None,  # square_off
              None)  # trailing_ticks
)


# TransactionType.Buy, OrderType.Market, ProductType.OneCancelsOther
# OCO Order can't be of type market

# TransactionType.Buy, OrderType.Limit, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%4%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
u.place_order(TransactionType.Buy,  # transaction_type
              u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
              1,  # quantity
              OrderType.Limit,  # order_type
              ProductType.Delivery,  # product_type
              8.0,  # price
              None,  # trigger_price
              0,  # disclosed_quantity
              DurationType.DAY,  # duration
              None,  # stop_loss
              None,  # square_off
              None)  # trailing_ticks
)

# TransactionType.Buy, OrderType.Limit, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%5%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.Limit,  # order_type
                 ProductType.Intraday,  # product_type
                 8.0,  # price
                 None,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks

)


# TransactionType.Buy, OrderType.Limit, ProductType.CoverOrder

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%6%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.Limit,  # order_type
                 ProductType.CoverOrder,  # product_type
                 8.0,  # price
                 8.0,  # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks 20 * 0.05
)


# TransactionType.Buy, OrderType.Limit, ProductType.OneCancelsOther

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%7%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.Limit,  # order_type
                 ProductType.OneCancelsOther,  # product_type
                 8.0,  # price
                 None,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 1.0,  # stop_loss
                 1.0,  # square_off
                 20)  # trailing_ticks 20 * 0.05
)


###############################

# TransactionType.Buy, OrderType.StopLossMarket, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%8%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.StopLossMarket,  # order_type
                 ProductType.Delivery,  # product_type
                 0.0,  # price
                 8.0,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks
)


# TransactionType.Buy, OrderType.StopLossMarket, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%9%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.StopLossMarket,  # order_type
                 ProductType.Intraday,  # product_type
                 0.0,  # price
                 8.0,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks
)



# TransactionType.Buy, OrderType.StopLossMarket, ProductType.CoverOrder
# CO order is of type Limit and And Market Only

# TransactionType.Buy, OrderType.StopLossMarket, ProductType.OneCancelsOther
# CO order is of type Limit and And Market Only

###################################

# TransactionType.Buy, OrderType.StopLossLimit, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%10%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.StopLossLimit,  # order_type
                 ProductType.Delivery,  # product_type
                 8.0,  # price
                 8.0,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks
)


# TransactionType.Buy, OrderType.StopLossLimit, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%11%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.StopLossLimit,  # order_type
                 ProductType.Intraday,  # product_type
                 8.0,  # price
                 8.0,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 None,  # stop_loss
                 None,  # square_off
                 None)  # trailing_ticks
)



# TransactionType.Buy, OrderType.StopLossLimit, ProductType.CoverOrder
# CO order is of type Limit and And Market Only


# TransactionType.Buy, OrderType.StopLossLimit, ProductType.OneCancelsOther

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%12%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   u.place_order(TransactionType.Buy,  # transaction_type
                 u.get_instrument_by_symbol('NSE_EQ', 'UNITECH'),  # instrument
                 1,  # quantity
                 OrderType.StopLossLimit,  # order_type
                 ProductType.OneCancelsOther,  # product_type
                 8.0,  # price
                 8.0,  # trigger_price
                 0,  # disclosed_quantity
                 DurationType.DAY,  # duration
                 1.0,  # stop_loss
                 1.0,  # square_off
                 20)  # trailing_ticks 20 * 0.05
)

```

### Cancel an order

```python
u.cancel_order(170713000075481) # Cancel an open order (Should be an int)
u.cancel_order('170713000075481') #Cancel an open order (Should be a string not an int -- WILL BE DOWNGRADED ON FUTURE VERSIONS)
u.cancel_order([170713000075481,170713000075482]) #Cancel multiple open orders (Order Ids is a list of int)
u.cancel_order('170713000075481,170713000075482') #Cancel multiple open orders (No spaces between various orders --  WILL BE DOWNGRADED ON FUTURE VERSIONS)
u.cancel_all_orders() #Cancel all open orders
```

### Order properties as objects
Order properties such as TransactionType, OrderType, and others have been safely classified as objects so you don't have to write them out as strings

#### TransactionType
Transaction types indicate whether you want to buy or sell. Valid transaction types are of the following:

* `TransactionType.Buy` - buy
* `TransactionType.Sell` - sell

#### OrderType
Order type specifies the type of order you want to send. Valid order types include:

* `OrderType.Market` - Place the order with a market price
* `OrderType.Limit` - Place the order with a limit price (limit price parameter is mandatory)
* `OrderType.StopLossLimit` - Place as a stop loss limit order
* `OrderType.StopLossMarket` - Place as a stop loss market order

#### ProductType
Product types indicate the complexity of the order you want to place. Valid product types are:

* `ProductType.Intraday` - Intraday order that will get squared off before market close
* `ProductType.Delivery` - Delivery order that will be held with you after market close
* `ProductType.CoverOrder` - Cover order
* `ProductType.OneCancelsOther` - One cancels other order. Also known as bracket order

#### DurationType
Duration types specify how long your order will stay on the market. Valid duration types include:

* `DurationType.DAY` - Day order
* `DurationType.IOC` - Immediate or cancel order

### Listen to live events
You can attach handlers to the following market events:

* Quote update
* Trade update
* Order update

Upstox uses the Websocket library to provide real-time updates for these events

1. Before starting the websocket, attach event handlers to the events you want to be notified for
```python
def my_generic_event_handler (event):
    print ("Event: %s" % str(event))

u.set_on_order_update (my_generic_event_handler)
u.set_on_quote_update (my_generic_event_handler)
```

2. Start the websocket library. The first parameter, `run_in_background`, controls whether the socket will run as a daemon or not

To run it in the current thread
```python
u.start_websocket (False)
```


To run it in the background, please ensure that your program doesn't exit. Here's an example of
```python
u.start_websocket (True)
condition = threading.Condition()
condition.acquire()
condition.wait()
```
