# Python SDK for Upstox API

The official Python library for communicating with the Upstox APIs.

Upstox Python library provides an easy to use wrapper over the HTTPs APIs.

The HTTP calls have been converted to methods and JSON responses are wrapped into Python-compatible objects.

Websocket connections are handled automatically with the library

## Installation

This module is installed via pip:

	pip install upstox

### Prerequisites
    Python 2.x or 3.x

## Getting started with API

### Overview

There are two classes in the library: Session, and Upstox. The Session class is used to retrieve an access token from the server. An access token is valid for 24 hours.
With an access token, you can instantiate an Upstox object. Ideally you only need to create a Session object once every day. After you have the access token, you can store it
separately for re-use.

### REST Documentation
The original REST API that this SDK is based on is available online.
   [Upstox API REST documentation](https://upstox.com/developer/api/v1/docs/)

## Using the API

### Get an access token
1. Import Upstox
```python
import upstox
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
```

### Get master contracts
Getting master contracts allow you to search for instruments by symbol name and place orders.
Master contracts are stored as an OrderedDict by token number and by symbol name. Whenever you get a trade update, order update, or quote update, the library will check if master contracts are loaded. If they are, it will attach the instrument object directly to the update.

```python
u.get_master_contract('NSE_EQ') # get contracts for NSE EQ
u.get_master_contract('NSE_FO') # get contracts for NSE FO
tatasteel_eq = u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL') # search by symbol name
reliance_eq = u.get_instrument_by_token('NSE_EQ', 2885) # search by exchange token
```

### Subscribe to feeds
Once you have master contracts loaded, you can easily subscribe to quote updates. You can either subscribe for a full quote update or an LTP quote update.

```python
u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
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
```python
u.start_websocket (True)
```