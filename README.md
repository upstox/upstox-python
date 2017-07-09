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
* `websocket_client`
* `requests` 

The modules can also be installed using `pip`

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
u.get_master_contract('BSE_EQ') # get contracts for NSE EQ
u.get_master_contract('NSE_FO') # get contracts for NSE FO
```

### Search for symbols
Symbols can be retrieved in multiple ways. Once you have the master contract loaded for an exchange, you can search for an instrument in many ways.

Search for a single instrument by it's name:
```python
tatasteel_nse_eq = u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL')
reliance_nse_eq = u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE')
ongc_bse_eq = u.get_instrument_by_symbol('BSE_EQ', 'ONGC')
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
Start getting live feed via socket
```python
def event_handler_quote_update(message):
    print("Quote Update: %s" % str(message))

u.set_on_quote_update(event_handler_quote_update)

u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
u.subscribe(u.get_instrument_by_symbol('BSE_EQ', 'RELIANCE'), LiveFeedType.LTP)

u.start_websocket(True)
```

#### Unsubscribe to a live feed
Unsubscribe to an existing live feed
```python
u.unsubscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
u.unsubscribe(u.get_instrument_by_symbol('BSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
```

### Place an order
Place limit, market, SL, SL-M, AMO, OCO/BO, CO orders

```python
# Limit and Market on Intraday
u.place_order(TransactionType.Buy, u.get_instrument_by_symbol('NCD_FO', 'USDINR17JUNFUT'), 1, OrderType.Limit, ProductType.Intraday, 65.0)
u.place_order(TransactionType.Sell, u.get_instrument_by_symbol('NCD_FO', 'USDINR17JUNFUT'), 1, OrderType.Market, ProductType.Intraday, 0.0)

# CO
u.place_order(TransactionType.Buy, u.get_instrument_by_symbol('NSE_FO', 'BANKNIFTY17JUN15FUT'), 40, OrderType.Limit, ProductType.CoverOrder, 23001.0, 22995.00, None, DurationType.DAY)

# OCO
u.place_order(TransactionType.Sell, u.get_instrument_by_symbol('NSE_FO', 'BANKNIFTY17JUN15FUT'), 40, OrderType.Limit, ProductType.OneCancelsOther, 23001.0, None, None, DurationType.DAY, 10.0, 10.0)
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