
from upstox_api.utils import *

import json
import os
from builtins import int
from collections import OrderedDict
from datetime import date

import requests
import threading
import websocket

import logging
logger = logging.getLogger(__name__)

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

# compatible import
from future.standard_library import install_aliases

install_aliases()

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

        params = {'apiKey': self.api_key, 'redirect_uri': self.redirect_uri, 'response_type': 'code'}

        return self.config['host'] + self.config['routes']['authorize'] + '?' + urlencode(params)

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

        url = self.config['host'] + self.config['routes']['accessToken']
        headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
        r = requests.post(url, auth=(self.api_key, self.api_secret), data=json.dumps(params), headers=headers)
        body = json.loads(r.text)
        if 'access_token' not in body:
            raise SystemError(body);
        return body


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


    def _on_data(self, ws, message, data_type, continue_flag):
        if data_type == websocket.ABNF.OPCODE_TEXT:
            parsed_message = json.loads(message)

            if is_status_2xx(parsed_message['code']):
                # valid 200 status message
                message = parsed_message['message']
                data = parsed_message['data']

                if message.lower() == 'order_update':
                    order_update = {
                        'quantity': int(data['quantity']),
                        'exchange_order_id': data['exchange_order_id'],
                        'order_type': OrderType.parse(data['order_type']),
                        'status': data['status'],
                        'transaction_type': TransactionType.parse(data['transaction_type']),
                        'exchange': data['exchange'],
                        'trigger_price': float(data['trigger_price']),
                        'symbol': data['symbol'],
                        'traded_quantity': int(data['traded_quantity']),
                        'is_amo': data['is_amo'],
                        'product': ProductType.parse(data['product']),
                        'order_request_id': data['order_request_id'],
                        'duration': DurationType.parse(data['valid_date']),
                        'price': float(data['price']),
                        'time_in_micro': data['time_in_micro'],
                        'parent_order_id': data['parent_order_id'],
                        'order_id': data['order_id'],
                        'message': data['message'],
                        'exchange_time': data['exchange_time'],
                        'disclosed_quantity': data['disclosed_quantity'],
                        'token': data['token'],
                        'average_price': float(data['average_price']),
                        'instrument': None
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
                        'traded_quantity': int(data['traded_quantity']),
                        'order_id': data['order_id'],
                        'order_type': OrderType.parse(data['order_type']),
                        'traded_price': float(data['traded_price']),
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

        else:
            data = message.decode()
            quotes = data.split(';')

            ltp_quote_fields = ["timestamp", "exchange", "symbol", "ltp", "close"]
            full_quote_fields = ["timestamp", "exchange", "symbol", "ltp", "close", "open", "high", "low", "vtt",
                                 "atp", "oi", "spot_price", "total_buy_qty", "total_sell_qty", "lower_circuit",
                                 "upper_circuit", "yearly_low", "yearly_high"]
            full_quote_fields_indices = ["timestamp", "exchange", "symbol", "live_ltp", "live_open",
                                         "live_high", "live_low", "live_close", "live_yearly_high",
                                         "live_yearly_low"]

            for quote in quotes:
                quote_object = None
                fields = quote.split(',')
                for index, field in enumerate(fields):
                    if field == 'NaN' or field == '':
                        fields[index] = None

                # convert timestamp to DateTime object
                # fields[0] = datetime.fromtimestamp(float(fields[0])/1000.0)

                # convert LTP and close to floats from string
                try:
                    fields[3] = float(fields[3])
                    fields[4] = float(fields[4])
                except ValueError:
                    pass

                # check if LTP subscription
                if len(fields) == 5:
                    quote_object = dict(zip(ltp_quote_fields, fields))

                # check if full quote subscription for indices
                elif len(fields) == 10:
                    quote_object = dict(zip(full_quote_fields_indices, fields))

                # check if full quote subscription
                elif len(fields) == 49 or len(fields) == 48:

                    # convert other string fields to floats or ints
                    for m in range(5, 12):
                        if fields[m] is not None:
                            fields[m] = float(fields[m])

                    for m in range(12, 14):
                        if fields[m] is not None:
                            fields[m] = int(fields[m])

                    for m in range(14, 18):
                        if fields[m] is not None:
                            fields[m] = float(fields[m])

                    quote_object = dict(zip(full_quote_fields, fields[:18]))
                    # Adding ltt or last traded time which comes as last field in full quote subscription
                    if len(fields) == 49:
                        quote_object["ltt"] = int(fields[48])
                    quote_object["bids"] = []
                    quote_object["asks"] = []
                    i = 18
                    j = 33
                    for h in range(1, 6):
                        quote_object["bids"].append(
                            {"quantity": int(fields[i]), "price": float(fields[i + 1]), "orders": int(fields[i + 2])})
                        quote_object["asks"].append(
                            {"quantity": int(fields[j]), "price": float(fields[j + 1]), "orders": int(fields[j + 2])})

                        i += 3
                        j += 3

                if quote_object is None:
                    logger.warning('Quote object was not mapped to any subscription. Length: %s, Values: %s' % (
                    str(len(fields)), quote))
                    continue
                else:
                    # append instrument object
                    if self.get_instrument_by_symbol(fields[1], fields[2]) is not None:
                        quote_object["instrument"] = self.get_instrument_by_symbol(fields[1], fields[2])

                if self.on_quote_update:
                    self.on_quote_update(quote_object)

    def _on_error(self, ws, error):
        if self.on_error:
            self.on_error(ws, error)

    def _on_close(self, ws):
        if self.on_disconnect:
            self.on_disconnect(ws)

    # def _on_open(self, ws):
    #     if self.on_open:
    #         self.on_open(ws)

    def __init__(self, api_key, access_token):
        """ logs in and gets enabled exchanges and products for user """
        self.api_key = api_key
        self.access_token = access_token
        with open(os.path.join(os.path.dirname(__file__), 'service_config.json')) as data_file:
            self.config = json.load(data_file)
        profile = self.api_call_helper('profile', PyCurlVerbs.GET, None, None)

        self.enabled_exchanges = []
        for x in profile['exchanges_enabled']:
            if x.lower() == 'nse_eq':
                self.enabled_exchanges.append('nse_index')
            if x.lower() == 'bse_eq':
                self.enabled_exchanges.append('bse_index')
            if x.lower() == 'mcx_fo':
                self.enabled_exchanges.append('mcx_index')
            self.enabled_exchanges.append(x.lower())

        self.enabled_products = [x.lower() for x in profile['products_enabled']]
        self.ws_thread = None

    def get_socket_params(self):
        return self.api_call_helper('socketParams', PyCurlVerbs.GET, None, None)

    def start_websocket(self, run_in_background=False):
        socket_params = {}
        try:
            socket_params = self.get_socket_params()
        except requests.exceptions.HTTPError:
            print("Can't Access Socket Params")
        ping_interval = 60
        ping_timeout = 10

        if 'pythonPingInterval' in socket_params.keys():
            ping_interval = socket_params['pythonPingInterval']

        if 'pythonPingTimeout' in socket_params.keys():
            ping_timeout = socket_params['pythonPingTimeout']

        url = self.config['socketEndpoint'].format(api_key=self.api_key, access_token=self.access_token)
        self.websocket = websocket.WebSocketApp(url,
                                                header={'Authorization: Bearer' + self.access_token},
                                                on_data=self._on_data,
                                                on_error=self._on_error,
                                                on_close=self._on_close)
                                                # on_open=self._on_open)
        if run_in_background is True:
            self.ws_thread = threading.Thread(target=self.websocket.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
        else:
            self.websocket.run_forever(ping_interval=ping_interval, ping_timeout=ping_timeout)

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

    # def set_on_open(self, event_handler):
    #     self.on_open = event_handler

    def get_profile(self):
        return self.api_call_helper('profile', PyCurlVerbs.GET, None, None)

    def get_balance(self):
        return self.api_call_helper('balance', PyCurlVerbs.GET, None, None)

    def get_holdings(self):
        return self.api_call_helper('holdings', PyCurlVerbs.GET, None, None)

    def get_positions(self):
        return self.api_call_helper('positions', PyCurlVerbs.GET, None, None)

    def get_trade_book(self):
        """ returns trade_book of a user """
        trade_book = self.api_call_helper('tradeBook', PyCurlVerbs.GET, None, None)

        for trade in trade_book:
            for key in trade:
                if key in Schema.schema_trade_book:
                    trade[key] = Schema.schema_trade_book[key](trade[key])
            try:
                instrument = self.get_instrument_by_token(trade['exchange'], trade['token'])
                trade['instrument'] = instrument
            except ValueError:
                pass

        return trade_book

    def get_order_history(self, order_id=None):
        """ leave order_id as None to get all entire order history """
        if order_id is None:
            order_history = self.api_call_helper('getOrders', PyCurlVerbs.GET, None, None);
        else:
            order_history = self.api_call_helper('getOrdersInfo', PyCurlVerbs.GET, {'order_id': order_id}, None);

        for order in order_history:
            for key in order:
                if key in Schema.schema_order_history:
                    order[key] = Schema.schema_order_history[key](order[key])
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

        return self.api_call_helper('tradesInfo', PyCurlVerbs.GET, {'order_id': order_id}, None)

    def logout(self):
        return self.api_call_helper('logout', PyCurlVerbs.GET, None, None)

    def get_exchanges(self):
        return self.enabled_exchanges

    def get_live_feed(self, instrument, live_feed_type):
        """ get the current feed of an instrument """

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if LiveFeedType.parse(live_feed_type) is None:
            raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

        return self.api_call_helper('liveFeed', PyCurlVerbs.GET, {'exchange': instrument.exchange,
                                                                  'symbol': instrument.symbol,
                                                                  'type': live_feed_type}
                                    , None)

    def get_subscriptions(self, **kwargs):
        """ get the current feed of an instrument """

        live_feed_type = kwargs.get("live_feed_type", "ALL")

        if live_feed_type != "ALL" and LiveFeedType.parse(live_feed_type) is None:
            raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

        return self.api_call_helper('getSubscriptions', PyCurlVerbs.GET, {'type': live_feed_type}
                                    , None)

    def get_ohlc(self, instrument, interval, start_date, end_date, download_as_csv=False):
        """ get OHLC for an instrument """

        if OHLCInterval.parseNew(interval) is None:
            raise TypeError("Required parameter interval not of type OHLCInterval")
        
        interval = OHLCInterval.parseNew(interval)

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(start_date, date):
            raise TypeError("Required parameter start_date not of type date")

        if not isinstance(end_date, date):
            raise TypeError("Required parameter end_date not of type date")

        output_format = 'json'

        if download_as_csv is True:
            output_format = 'csv'

        ohlc = self.api_call_helper('OHLC', PyCurlVerbs.GET, {'exchange': instrument.exchange,
                                                              'symbol': instrument.symbol,
                                                              'interval': interval,
                                                              'start_date': start_date.strftime('%d-%m-%Y'),
                                                              'end_date': end_date.strftime('%d-%m-%Y'),
                                                              'format': output_format
                                                              }, None
                                    )

        return ohlc;

    def place_order(self, transaction_type, instrument, quantity, order_type,
                    product_type, price=None, trigger_price=None,
                    disclosed_quantity=None, duration=None, stop_loss=None,
                    square_off=None, trailing_ticks=None):
        """ placing an order, many fields are optional and are not required
            for all order types
        """
        if TransactionType.parse(transaction_type) is None:
            raise TypeError("Required parameter transaction_type not of type TransactionType")

        if not isinstance(instrument, Instrument):
            raise TypeError("Required parameter instrument not of type Instrument")

        if not isinstance(quantity, int):
            raise TypeError("Required parameter quantity not of type int")

        if OrderType.parse(order_type) is None:
            raise TypeError("Required parameter order_type not of type OrderType")

        if ProductType.parse(product_type) is None:
            raise TypeError("Required parameter product_type not of type ProductType")

        # construct order object after all required parameters are met
        order = {'transaction_type': transaction_type, 'exchange': instrument.exchange,
                 'symbol': instrument.symbol,
                 'quantity': quantity, 'order_type': order_type, 'product': product_type}

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

        if duration is not None and DurationType.parse(duration) is None:
            raise TypeError("Optional parameter duration not of type DurationType")
        elif duration is not None:
            order['duration'] = duration

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

    def modify_order(self, order_id, quantity=None, order_type=None, price=None,
                     trigger_price=None, disclosed_quantity=None, duration=None):
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

        if order_type is not None and OrderType.parse(order_type) is None:
            raise TypeError("Optional parameter order_type not of type OrderType")
        elif order_type is not None:
            order['order_type'] = order_type

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

        if duration is not None and DurationType.parse(duration) is None:
            raise TypeError("Optional parameter duration not of type DurationType")
        elif duration is not None:
            order['duration'] = duration

        return self.api_call_helper('modifyOrder', PyCurlVerbs.PUT, {'order_id': order_id}, order)

    def cancel_order(self, order_id):

        # if not isinstance(order_id, int):
        #     raise TypeError("Required parameter order_id not of type int")

        print(type(order_id));
        if type(order_id) is list:
            for order_no in order_id:
                if not isinstance(order_no, int):
                    raise TypeError("Required parameter order_id not of type int")
            order_id = ",".join(str(x) for x in order_id)

        return self.api_call_helper('cancelOrder', PyCurlVerbs.DELETE, {'order_id': order_id}, None)

    def cancel_all_orders(self):

        # if not isinstance(order_id, int):
        #     raise TypeError("Required parameter order_id not of type int")

        return self.api_call_helper('cancelAllOrders', PyCurlVerbs.DELETE, None, None)

    def subscribe(self, instrument, live_feed_type, exchange = None):
        """ subscribe to the current feed of an instrument """
        symbol = ""
        if (isinstance(instrument, list)):
            for _instrument in instrument:
                if not isinstance(_instrument, Instrument):
                    raise TypeError("Required parameter instrument not of type Instrument")

                if exchange == None:
                    logger.warning('Invalid exchange value provided: [%s]' % (exchange))
                    raise ValueError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

                exchange = exchange.lower()

                if exchange not in self.enabled_exchanges:
                    logger.warning('Invalid exchange value provided: [%s]' % (exchange))
                    raise TypeError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

                if(_instrument.exchange.lower() != exchange):
                    raise ValueError("Given instrument is not of the same exchange provided [%s]" % (exchange))

                if LiveFeedType.parse(live_feed_type) is None:
                    raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

                symbol += _instrument.symbol + ","

            symbol = symbol[:-1]
        else:
            if not isinstance(instrument, Instrument):
                raise TypeError("Required parameter instrument not of type Instrument")

            if LiveFeedType.parse(live_feed_type) is None:
                raise TypeError("Required parameter live_feed_type not of type LiveFeedType")
            exchange = instrument.exchange
            symbol = instrument.symbol

        return self.api_call_helper('liveFeedSubscribe', PyCurlVerbs.GET, {'exchange': exchange,
                                                                           'symbol': symbol,
                                                                           'type': live_feed_type}
                                    , None);

    def unsubscribe(self, instrument, live_feed_type, exchange = None):
        """ unsubscribe to the current feed of an instrument """
        symbol = ""
        if (isinstance(instrument, list)):
            for _instrument in instrument:
                if not isinstance(_instrument, Instrument):
                    raise TypeError("Required parameter instrument not of type Instrument")

                if exchange == None:
                    logger.warning('Invalid exchange value provided: [%s]' % (exchange))
                    raise ValueError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

                exchange = exchange.lower()

                if exchange not in self.enabled_exchanges:
                    logger.warning('Invalid exchange value provided: [%s]' % (exchange))
                    raise TypeError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

                if(_instrument.exchange.lower() != exchange):
                    raise ValueError("Given instrument is not of exchange provided exchange [%s]" % (exchange))

                if LiveFeedType.parse(live_feed_type) is None:
                    raise TypeError("Required parameter live_feed_type not of type LiveFeedType")

                symbol += _instrument.symbol + ","

            symbol = symbol[:-1]

        else:
            if not isinstance(instrument, Instrument):
                raise TypeError("Required parameter instrument not of type Instrument")

            if LiveFeedType.parse(live_feed_type) is None:
                raise TypeError("Required parameter live_feed_type not of type LiveFeedType")
            exchange = instrument.exchange
            symbol = instrument.symbol

        return self.api_call_helper('liveFeedUnsubscribe', PyCurlVerbs.GET, {'exchange': exchange,
                                                                             'symbol': symbol,
                                                                             'type': live_feed_type}
                                    , None);

    def get_instrument_by_symbol(self, exchange, symbol):
        # get instrument given exchange and symbol
        global master_contracts_by_symbol

        exchange = exchange.lower()
        symbol = symbol.lower()
        # check if master contract exists
        if exchange not in master_contracts_by_symbol:
            logger.warning("Cannot find exchange [%s] in master contract. "
                            "Please ensure you have called get_master_contract function first" % exchange)
            return None

        master_contract = master_contracts_by_symbol[exchange]

        if symbol not in master_contract:
            logger.warning("Cannot find symbol [%s:%s] in master contract" % (exchange, symbol))
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
            logger.warning(
                "Cannot find exchange [%s] in master contract. "
                "Please ensure you have called get_master_contract function first" % exchange)
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
            logger.warning(
                "Cannot find exchange [%s] in master contract. "
                "Please ensure you have called get_master_contract function first" % exchange)
            return None

        master_contract = master_contracts_by_token[exchange]

        if token not in master_contract:
            logger.warning("Cannot find token [%s:%s] in master contracts" % (exchange, token))
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
            logger.warning('Invalid exchange value provided: [%s]' % (exchange))
            raise ValueError("Please provide a valid exchange [%s]" % ",".join(self.enabled_exchanges))

        logger.debug('Downloading master contracts for exchange: %s' % (exchange))
        body = self.api_call_helper('masterContract', PyCurlVerbs.GET, {'exchange': exchange}, None)
        count = 0
        master_contract_by_token = OrderedDict()
        master_contract_by_symbol = OrderedDict()
        for line in body:
            count += 1
            if count == 1:
                continue
            item = line.split(',')

            # convert token
            if item[1] is not u'':
                item[1] = int(item[1])

            # convert parent token
            if item[2] is not u'':
                item[2] = int(item[2])
            else:
                item[2] = None;

            # convert symbol to upper
            item[3] = item[3].lower()

            # convert closing price to float
            if item[5] is not u'':
                item[5] = float(item[5])
            else:
                item[5] = None;

            # convert expiry to none if it's non-existent
            if item[6] is u'':
                item[6] = None;

            # convert strike price to float
            if item[7] is not u'' and item[7] is not u'0':
                item[7] = float(item[7])
            else:
                item[7] = None;

            # convert tick size to int
            if item[8] is not u'':
                item[8] = float(item[8])
            else:
                item[8] = None;

            # convert lot size to int
            if item[9] is not u'':
                item[9] = int(item[9])
            else:
                item[9] = None

            # convert instrument_type to none if it's non-existent
            if item[10] is u'':
                item[10] = None;

            # convert isin to none if it's non-existent
            if item[11] is u'':
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
        if "INDEX" in exchange.upper():
            return master_contracts_by_symbol[exchange]
        return master_contracts_by_token[exchange]

    def api_call_helper(self, name, http_method, params, data):
        # helper formats the url and reads error codes nicely
        url = self.config['host'] + self.config['routes'][name]

        if params is not None:
            url = url.format(**params)

        response = self.api_call(url, http_method, data)

        if response.status_code != 200:
            raise requests.HTTPError(response.text)

        body = json.loads(response.text)

        if is_status_2xx(body['code']):
            # success
            return body['data']
        else:
            raise requests.HTTPError(response.text)

        return

    def api_call(self, url, http_method, data):

        headers = {"Content-Type": "application/json", "x-api-key": self.api_key,
                   "authorization": "Bearer " + self.access_token}

        logger.debug('url:: %s http_method:: %s data:: %s headers:: %s', url, http_method, data, headers)

        r = None

        if http_method is PyCurlVerbs.POST:
            r = requests.post(url, data=json.dumps(data), headers=headers)
        elif http_method is PyCurlVerbs.DELETE:
            r = requests.delete(url, headers=headers)
        elif http_method is PyCurlVerbs.PUT:
            r = requests.put(url, data=json.dumps(data), headers=headers)
        elif http_method is PyCurlVerbs.GET:
            r = requests.get(url, headers=headers)

        return r
