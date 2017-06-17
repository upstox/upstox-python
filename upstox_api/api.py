import json, os, pycurl, future
from collections import OrderedDict
from io import BytesIO
from upstox_api.utils import *
import websocket, threading
import logging
from datetime import date

# compatible import
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# master contracts by token
master_contracts_by_token = dict()

# master contracts by symbol
master_contracts_by_symbol = dict()


class Session:
    """Session object to create and authenticate a session"""

    # account and session variables
    api_key = None
    api_secret = None
    redirect_uri = None
    code = None

    # dictionary object to hold settings
    config = None

    def __init__(self, api_key):
        self.api_key = api_key
        with open(os.path.join(os.path.dirname(__file__), 'service_config.json')) as data_file:
            self.config = json.load(data_file)

    def set_api_secret(self, api_secret):
        self.api_secret = api_secret

    def set_redirect_uri(self, redirect_uri):
        self.redirect_uri = redirect_uri

    def set_code(self, code):
        self.code = code

    def get_login_url(self):
        """ login to this url and retrieve authorization code. api_key
            and redirect_uri have to be set
        """
        if self.api_key is None:
            raise (TypeError, 'Value api_key cannot be None. Please go to the Developer Console to get this value')
        if self.redirect_uri is None:
            raise (TypeError, 'Value redirect_uri cannot be None. Please go to the Developer Console to get this value')

        params = {'apiKey' : self.api_key, 'redirect_uri' : self.redirect_uri, 'response_type' : 'code'}

        return self.config['host'] + self.config['routes']['authorize'] + '?' + urlencode(params);

    def retrieve_access_token(self):
        """ once you have the authorization code, you can call this function to get
            the access_token. The access_token gives you full access to the API and is
            valid throughout the day
        """
        if self.api_key is None:
            raise (TypeError, 'Value api_key cannot be None. Please go to the Developer Console to get this value')
        if self.redirect_uri is None:
            raise (TypeError, 'Value redirect_uri cannot be None. Please go to the Developer Console to get this value')
        if self.api_secret is None:
            raise (TypeError, 'Value api_secret cannot be None. Please go to the Developer Console to get this value')
        if self.code is None:
            raise (TypeError, 'Value code cannot be None. Please visit the login URL to generate a code')

        params = {'code': self.code, 'redirect_uri': self.redirect_uri, 'grant_type': 'authorization_code'}

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.config['host'] + self.config['routes']['accessToken'])
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(pycurl.USERPWD, self.api_key + ':' + self.api_secret)
        c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json", "x-api-key: " + self.api_key])
        c.setopt(pycurl.POSTFIELDS, json.dumps(params))
        c.perform()
        c.close()

        data = buffer.getvalue().decode('iso-8859-1')
        # Body is a byte string.
        # We have to know the encoding in order to print it to a text file
        # such as standard output.
        body = json.loads(data)
        if 'access_token' not in body:
            raise SystemError(body);
        return body['access_token']


class Upstox:

    api_key = None
    access_token = None

    # dictionary object to hold settings
    config = None
    enabled_exchanges = None
    products_enabled = None
    websocket = None

    on_order_update = None
    on_trade_update = None
    on_quote_update = None
    on_error = None
    on_disconnect = None

    def _on_message (self, ws, message):
        if isinstance(message, str):
            parsed_message = json.loads(message)

            if is_status_2xx(parsed_message['code']):
                # valid 200 status message
                message = parsed_message['message']
                data = parsed_message['data']

                if message.lower() == 'order_update':
                    order_update = {
                        'quantity' : data['quantity'],
                        'exchange_order_id': data['exchange_order_id'],
                        'order_type': OrderType.parse(data['order_type']),
                        'status' : data['status'],
                        'transaction_type' : TransactionType.parse(data['transaction_type']),
                        'exchange' : data['exchange'],
                        'trigger_price' : data['trigger_price'],
                        'symbol' : data['symbol'],
                        'traded_quantity' : data['traded_quantity'],
                        'is_amo' : data['is_amo'],
                        'product' : ProductType.parse(data['product']),
                        'order_request_id' : data['order_request_id'],
                        'duration' : DurationType.parse(data['valid_date']),
                        'price' : data['price'],
                        'time_in_micro' : data['time_in_micro'],
                        'parent_order_id' : data['parent_order_id'],
                        'order_id' : data['order_id'],
                        'message' : data['message'],
                        'exchange_time' : data['exchange_time'],
                        'disclosed_quantity' : data['disclosed_quantity'],
                        'token' : data['token'],
                        'average_price' : data['average_price'],
                        'instrument' : None
                    }
                    try:
                        instrument = self.get_instrument_by_token(data['exchange'], data['token'])
                        order_update['instrument'] = instrument
                    except ValueError:
                        pass
                    if self.on_order_update:
                        self.on_order_update(order_update)
                elif message.lower() == 'fill_report':
                    # {'data': {'exchange_time': '16-Jun-2017 12:41:20', 'token': 45578, 'traded_quantity': 40,
                    # 'order_id': '170616000000084', 'order_type': 'M', 'traded_price': 22998.45, 'trade_id': '1600',
                    # 'transaction_type': 'S', 'exchange_order_id': '1000000000005143',
                    # 'exchange': 'NSE_FO', 'product': 'I', 'time_in_micro': '0', 'symbol': 'BANKNIFTY17JUNFUT'},
                    # 'timestamp': '2017-06-16T12:41:20+05:30', 'status': 'OK', 'code': 200, 'message': 'fill_report'}

                    trade_update = {
                        'exchange_time': data['exchange_time'],
                        'token': data['token'],
                        'traded_quantity': data['traded_quantity'],
                        'order_id': data['order_id'],
                        'order_type': OrderType.parse(data['order_type']),
                        'traded_price': data['traded_price'],
                        'trade_id': data['trade_id'],
                        'transaction_type': TransactionType.parse(data['transaction_type']),
                        'exchange_order_id': data['exchange_order_id'],
                        'exchange': data['exchange'],
                        'product': ProductType.parse(data['product']),
                        'time_in_micro': data['time_in_micro'],
                        'symbol': data['symbol'],
                        'instrument': None
                    }
                    try:
                        instrument = self.get_instrument_by_token(data['exchange'], data['token'])
                        trade_update['instrument'] = instrument
                    except ValueError:
                        pass
                    if self.on_trade_update:
                        self.on_trade_update(trade_update)
                else:
                    print("Unknown message: %s" % parsed_message)

        if isinstance(message, bytes):
            data = message.decode()
            quotes = data.split(';')

            ltp_quote_fields = ["timestamp", "exchange", "symbol", "ltp", "close"]
            full_quote_fields = ["timestamp", "exchange", "symbol", "ltp", "close", "open", "high", "low", "vtt",
                                 "atp", "oi", "spot_price", "total_buy_qty", "total_sell_qty", "lower_circuit",
                                 "upper_circuit", "yearly_low", "yearly_high"]

            for quote in quotes:
                obj = dict()
                quote_object = None
                fields = quote.split(',')
                for index, field in enumerate(fields):
                    if field == 'NaN' or field == '':
                        fields[index] = None

                # check if LTP subscription
                if len(fields) == 5:
                    quote_object = dict(zip(ltp_quote_fields, fields))

                # check if full quote subscription
                elif len(fields) == 48:
                    quote_object = dict(zip(full_quote_fields, fields[:17]))
                    quote_object["bids"] = []
                    quote_object["asks"] = []
                    i = 18
                    j = 32
                    for h in range(1, 6):
                        quote_object["bids"].append({"orders" : fields[i], "quantity" : fields[i + 1], "price" : fields[i + 2]})
                        quote_object["asks"].append({"orders" : fields[j], "quantity" : fields[j + 1], "price" : fields[j + 2]})
                        i += 3
                        j += 3

                # append instrument object
                quote_object["instrument"] = self.get_instrument_by_symbol(fields[1], fields[2])


                if quote_object is None:
                    logging.warning('Quote object was not mapped to any subscription. Length: %s, Values: %s' % (str(len(fields)), str(fields)))
                    continue
                elif self.on_quote_update:
                    self.on_quote_update(quote_object)

    def _on_error (self, ws, error):
        if self.on_error:
            self.on_error(ws, error)

    def _on_close (self, ws):
        if self.on_disconnect:
            self.on_disconnect(ws)

    def __init__(self, api_key, access_token):
        """ logs in and gets enabled exchanges and products for user """
        self.api_key = api_key
        self.access_token = access_token
        with open(os.path.join(os.path.dirname(__file__), 'service_config.json')) as data_file:
            self.config = json.load(data_file)
        profile = self.api_call_helper('profile', PyCurlVerbs.GET, None, None)

        self.enabled_exchanges = [x.lower() for x in profile['exchanges_enabled']]
        self.enabled_products = [x.lower() for x in profile['products_enabled']]
        self.ws_thread = None

    def start_websocket(self, run_in_background = False):

        url = self.config['socketEndpoint'].format(api_key=self.api_key, access_token=self.access_token)
        self.websocket = websocket.WebSocketApp(url, on_message = self._on_message,
                              on_error = self._on_error,
                              on_close = self._on_close)
        if run_in_background is True:
            self.ws_thread = threading.Thread(target=self.websocket.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
        else:
            self.websocket.run_forever()

    def set_on_order_update(self, event_handler):
        self.on_order_update = event_handler

    def set_on_quote_update(self, event_handler):
        self.on_quote_update = event_handler

    def set_on_trade_update(self, event_handler):
        self.on_trade_update = event_handler

    def set_on_disconnect(self, event_handler):
        self.on_disconnect = event_handler

    def set_on_error(self, event_handler):
        self.on_error = event_handler

    def get_profile(self):
        return self.api_call_helper('profile', PyCurlVerbs.GET, None, None)

    def get_balance(self):
        return self.api_call_helper('balance', PyCurlVerbs.GET, None, None)

    def get_holdings(self):
        return self.api_call_helper('holdings', PyCurlVerbs.GET, None, None)

    def get_positions(self):
        return self.api_call_helper('positions', PyCurlVerbs.GET, None, None)

    def get_order_history(self, order_id=None):
        """ leave order_id as None to get all entire order history """
        if order_id is None:
            order_history = self.api_call_helper('getOrders', PyCurlVerbs.GET, None, None);
        else:
            order_history = self.api_call_helper('getOrdersInfo', PyCurlVerbs.GET, {'order_id' : order_id}, None);

        for order in order_history:
            try:
                instrument = self.get_instrument_by_token(order['exchange'], order['token'])
                order['instrument'] = instrument
            except ValueError:
                pass

        return order_history;

    def get_trades(self, order_id):
        """ get all trades of a particular order """
        if not isinstance(order_id, int):
            raise TypeError("Required parameter order_id not of type int")

        return self.api_call_helper('tradesInfo', PyCurlVerbs.GET, {'order_id' : order_id}, None)

    def logout(self):
        return self.api_call_helper('logout', PyCurlVerbs.GET, None, None)

    def get_exchanges(self):
        return self.enabled_exchanges

    def get_live_feed(self, instrument, live_feed_type):
        """ get the current feed of an instrument """

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(live_feed_type, LiveFeedType):
            raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

        return self.api_call_helper('liveFeed', PyCurlVerbs.GET, {'exchange': instrument.exchange,
                                                                       'symbol' : instrument.symbol,
                                                                       'type' : live_feed_type.value}
                                         , None)

    def get_ohlc(self, instrument, interval, start_date, end_date, download_as_csv = False):
        """ get OHLC for an instrument """

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(interval, OHLCInterval):
            raise TypeError("Required parameter interval not of type OHLCInterval")

        if not isinstance(start_date, date):
            raise TypeError("Required parameter start_date not of type date")

        if not isinstance(end_date, date):
            raise TypeError("Required parameter end_date not of type date")

        output_format = 'json'

        if download_as_csv is True:
            output_format = 'csv'

        ohlc = self.api_call_helper('OHLC', PyCurlVerbs.GET, {'exchange': instrument.exchange,
                                                                'symbol' : instrument.symbol,
                                                                'interval' : interval.value,
                                                                'start_date' : start_date.strftime('%d-%m-%Y'),
                                                                'end_date': end_date.strftime('%d-%m-%Y'),
                                                                'format' : output_format
                                                                 }, None
                                                                )
        return ohlc;

    def place_order(self, transaction_type, instrument, quantity, order_type,
                    product_type, price = None, trigger_price = None,
                    disclosed_quantity = None, duration = None, stop_loss = None,
                    square_off = None, trailing_ticks = None):
        """ placing an order, many fields are optional and are not required
            for all order types
        """
        if not isinstance(transaction_type, TransactionType):
            raise TypeError("Required parameter transaction_type not of type TransactionType")

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(quantity, int):
            raise TypeError("Required parameter quantity not of type int")

        if not isinstance(order_type, OrderType):
            raise TypeError("Required parameter order_type not of type OrderType")

        if not isinstance(product_type, ProductType):
            raise TypeError("Required parameter product_type not of type ProductType")

        # construct order object after all required parameters are met
        order = {'transaction_type': transaction_type.value, 'exchange': instrument.exchange,
                 'symbol': instrument.symbol,
                 'quantity': quantity, 'order_type': order_type.value, 'product': product_type.value}

        if price is not None and not isinstance(price, float):
            raise TypeError("Optional parameter price not of type float")
        elif price is not None:
            order['price'] = price

        if trigger_price is not None and not isinstance(trigger_price, float):
            raise TypeError("Optional parameter trigger_price not of type float")
        elif trigger_price is not None:
            order['trigger_price'] = trigger_price

        if disclosed_quantity is not None and not isinstance(disclosed_quantity, int):
            raise TypeError("Optional parameter disclosed_quantity not of type int")
        elif disclosed_quantity is not None:
            order['disclosed_quantity'] = disclosed_quantity

        if duration is not None and not isinstance(duration, DurationType):
            raise TypeError("Optional duration product_type not of type DurationType")
        elif duration is not None:
            order['duration'] = duration.value

        if stop_loss is not None and not isinstance(stop_loss, float):
            raise TypeError("Optional parameter stop_loss not of type float")
        elif stop_loss is not None:
            order['stoploss'] = stop_loss

        if square_off is not None and not isinstance(square_off, float):
            raise TypeError("Optional parameter square_off not of type float")
        elif square_off is not None:
            order['squareoff'] = square_off

        if trailing_ticks is not None and not isinstance(trailing_ticks, int):
            raise TypeError("Optional parameter trailing_ticks not of type int")
        elif trailing_ticks is not None:
            order['trailing_ticks'] = trailing_ticks

        if product_type is ProductType.CoverOrder:
            if not isinstance(trigger_price, float):
                raise TypeError("Required parameter trigger_price not of type float")

        if product_type is ProductType.OneCancelsOther:
            if not isinstance(stop_loss, float):
                raise TypeError("Required parameter stop_loss not of type float")

            if not isinstance(square_off, float):
                raise TypeError("Required parameter square_off not of type float")

        return self.api_call_helper('placeOrder', PyCurlVerbs.POST, None, order)

    def modify_order(self, order_id, quantity = None, order_type = None, price = None,
                     trigger_price = None, disclosed_quantity = None, duration = None):
        """ modify an order, only order id is required, rest are optional, use only when
            when you want to change that attribute
        """
        if not isinstance(order_id, int):
            raise TypeError("Required parameter order_id not of type int")

        # construct order object with order id
        order = {'order_id': order_id}

        if quantity is not None and not isinstance(quantity, int):
            raise TypeError("Optional parameter quantity not of type int")
        elif quantity is not None:
            order['quantity'] = quantity

        if order_type is not None and not isinstance(order_type, OrderType):
            raise TypeError("Optional duration order_type not of type OrderType")
        elif order_type is not None:
            order['order_type'] = order_type.value

        if price is not None and not isinstance(price, float):
            raise TypeError("Optional parameter price not of type float")
        elif price is not None:
            order['price'] = price

        if trigger_price is not None and not isinstance(trigger_price, float):
            raise TypeError("Optional parameter trigger_price not of type float")
        elif trigger_price is not None:
            order['trigger_price'] = trigger_price

        if disclosed_quantity is not None and not isinstance(disclosed_quantity, int):
            raise TypeError("Optional parameter disclosed_quantity not of type int")
        elif disclosed_quantity is not None:
            order['disclosed_quantity'] = disclosed_quantity

        if duration is not None and not isinstance(duration, DurationType):
            raise TypeError("Optional duration product_type not of type DurationType")
        elif duration is not None:
            order['duration'] = duration.value

        return self.api_call_helper('modifyOrder', PyCurlVerbs.PUT, {'order_id' : order_id}, order)

    def cancel_order(self, order_id):

        if not isinstance(order_id, int):
            raise TypeError("Required parameter order_id not of type int")

        return self.api_call_helper('cancelOrder', PyCurlVerbs.DELETE, {'order_id' : order_id}, None)

    def subscribe(self, instrument, live_feed_type):
        """ get the current feed of an instrument """

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(live_feed_type, LiveFeedType):
            raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

        return self.api_call_helper('liveFeedSubscribe', PyCurlVerbs.GET, {'exchange': instrument.exchange,
                                                                       'symbol' : instrument.symbol,
                                                                       'type' : live_feed_type.value}
                                          , None);

    def get_instrument_by_symbol(self, exchange, symbol):
        # get instrument given exchange and symbol
        global master_contracts_by_symbol

        exchange = exchange.lower()
        symbol = symbol.lower()
        # check if master contract exists
        if exchange not in master_contracts_by_symbol:
            return None

        master_contract = master_contracts_by_symbol[exchange]

        if symbol not in master_contract:
            return None
        return master_contract[symbol]

    def search_instruments(self, exchange, symbol):
        # search instrument given exchange and symbol
        global master_contracts_by_token

        exchange = exchange.lower()
        symbol = symbol.lower()

        matches = []

        # check if master contract exists
        if exchange not in master_contracts_by_token:
            return None

        master_contract = master_contracts_by_token[exchange]

        for contract in master_contract:
            if symbol in master_contract[contract].symbol:
                matches.append(master_contract[contract])

        return matches

    def get_instrument_by_token(self, exchange, token):
        # get instrument given exchange and token
        global master_contracts_by_token

        exchange = exchange.lower()

        # check if master contract exists
        if exchange not in master_contracts_by_token:
            return None

        master_contract = master_contracts_by_token[exchange]

        if token not in master_contract:
            return None
        return master_contract[token]

    def get_master_contract(self, exchange):
        """ returns all the tradable contracts of an exchange
            placed in an OrderedDict and the key is the token
        """
        global master_contracts_by_token
        exchange = exchange.lower()
        if exchange in master_contracts_by_token:
            return master_contracts_by_token[exchange]

        if exchange not in self.enabled_exchanges:
            logging.warning('Invalid exchange value provided: [%s]' % (exchange))
            raise ValueError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

        logging.debug('Downloading master contracts for exchange: %s' % (exchange))
        body = self.api_call_helper('masterContract', PyCurlVerbs.GET, {'exchange' : exchange}, None)
        count = 0
        master_contract_by_token = OrderedDict()
        master_contract_by_symbol = OrderedDict()
        for line in body:
            count += 1
            if count == 1:
                continue
            item = line.split(',')

            # convert token
            if item[1] is not '':
                item[1] = int(item[1])

            # convert parent token
            if item[2] is not '':
                item[2] = int(item[2])
            else:
                item[2] = None;

            # convert symbol to upper
            item[3] = item[3].lower()

            # convert closing price to float
            if item[5] is not '':
                item[5] = float(item[5])
            else:
                item[5] = None;

            # convert expiry to none if it's non-existent
            if item[6] is '':
                item[6] = None;

            # convert strike price to float
            if item[7] is not '' and item[7] is not '0':
                item[7] = float(item[7])
            else:
                item[7] = None;

            # convert tick size to int
            if item[8] is not '':
                item[8] = float(item[8])
            else:
                item[8] = None;

            # convert lot size to int
            if item[9] is not '':
                item[9] = int(item[9])
            else:
                item[9] = None

            # convert instrument_type to none if it's non-existent
            if item[10] is '':
                item[10] = None;

            # convert isin to none if it's non-existent
            if item[11] is '':
                item[11] = None;

            instrument = Instrument(item[0], item[1], item[2], item[3], item[4],
                                    item[5], item[6], item[7], item[8], item[9],
                                    item[10], item[11])

            token = item[1]
            symbol = item[3]
            master_contract_by_token[token] = instrument
            master_contract_by_symbol[symbol] = instrument
        master_contracts_by_token[exchange] = master_contract_by_token
        master_contracts_by_symbol[exchange] = master_contract_by_symbol
        logging.debug('Downloading master contracts for exchange: %s... done' % (exchange))
        return master_contracts_by_token[exchange]

    def api_call_helper(self, name, http_method, params, data):
        # helper formats the url and reads error codes nicely
        url = self.config['host'] + self.config['routes'][name]

        if params is not None:
            url = url.format(**params)

        value = self.api_call(url, http_method, data)

        api_call = json.loads(value)

        if 'code' not in api_call:
            raise ValueError(api_call);

        if is_status_2xx(api_call['code']):
            # success
            return api_call["data"];
        elif api_call['code'] == 400:
            raise ValueError(api_call['error']['reason'])
        elif api_call['code'] == 500:
            raise SystemError(api_call['error']['reason'])
        elif api_call['code'] == 503:
            raise urllib.error.HTTPError()
        else:
            raise SystemError(api_call)

        return

    def api_call(self, url, http_method, data):
        # makes a rest call
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json", "x-api-key: " + self.api_key, \
                                     "authorization: Bearer " + self.access_token])

        if http_method is PyCurlVerbs.POST:
            if data is not None:
                c.setopt(pycurl.POSTFIELDS, json.dumps(data))
        elif http_method is PyCurlVerbs.DELETE:
            c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
        elif http_method is PyCurlVerbs.PUT:
            c.setopt(pycurl.CUSTOMREQUEST, "PUT")
            if data is not None:
                c.setopt(pycurl.POSTFIELDS, json.dumps(data))
        c.perform()
        c.close()

        body = buffer.getvalue()
        # Body is a byte string.
        # We have to know the encoding in order to print it to a text file
        # such as standard output.
        return body.decode('iso-8859-1')