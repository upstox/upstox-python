from __future__ import print_function
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint


def login_and_authorize(api_version, configuration, client_id, client_secret, redirect_uri, auth_code):
    # Login API
    api_instance = upstox_client.LoginApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.token(api_version, code=auth_code, client_id=client_id,
                                      client_secret=client_secret, redirect_uri=redirect_uri, grant_type="authorization_code")
    return api_response.access_token


def get_profile(api_version, configuration):
    api_instance = upstox_client.UserApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_profile(api_version)
    return api_response


def get_funds_and_margin(api_version, configuration):
    api_instance = upstox_client.UserApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_user_fund_margin(api_version)
    return api_response


def get_positions(api_version, configuration):
    api_instance = upstox_client.PortfolioApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_positions(api_version)
    return api_response


def get_holdings(api_version, configuration):
    api_instance = upstox_client.PortfolioApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_holdings(api_version)
    return api_response


def place_order(api_version, configuration, order_details):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.place_order(order_details, api_version)
    return api_response


def modify_order(api_version, configuration, order_details):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.modify_order(order_details, api_version)
    return api_response


def cancel_order(api_version, configuration, order_id):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.cancel_order(order_id, api_version)
    return api_response


def get_trades_by_order(api_version, configuration, order_id):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_trades_by_order(order_id, api_version)
    return api_response


def get_trade_history(api_version, configuration):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_trade_history(api_version)
    return api_response


def get_order_book(api_version, configuration):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_order_book(api_version)
    return api_response


def get_order_details(api_version, configuration, order_id):
    api_instance = upstox_client.OrderApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_order_details(
        api_version, order_id=order_id)
    return api_response


def convert_positions(api_version, configuration, body):
    api_instance = upstox_client.PortfolioApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.convert_positions(body, api_version)
    return api_response


def get_full_market_quote(api_version, configuration, instrument_key):
    api_instance = upstox_client.MarketQuoteApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_full_market_quote(
        instrument_key, api_version)
    return api_response


def get_market_quote_ohlc(api_version, configuration, instrument_key, interval):
    api_instance = upstox_client.MarketQuoteApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_market_quote_ohlc(
        instrument_key, interval, api_version)
    return api_response


def ltp(api_version, configuration, instrument_key):
    api_instance = upstox_client.MarketQuoteApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.ltp(instrument_key, api_version)
    return api_response


def get_trade_wise_profit_and_loss_meta_data(api_version, configuration, segment, year):
    api_instance = upstox_client.TradeProfitAndLossApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_trade_wise_profit_and_loss_meta_data(
        segment, year, api_version)
    return api_response


def get_trade_wise_profit_and_loss_data(api_version, configuration, segment, year):
    api_instance = upstox_client.TradeProfitAndLossApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_trade_wise_profit_and_loss_data(
        segment, year, 1, 3000, api_version)
    return api_response


def get_profit_and_loss_charges(api_version, configuration, segment, year):
    api_instance = upstox_client.TradeProfitAndLossApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_profit_and_loss_charges(
        segment, year, api_version)
    return api_response


def get_historical_candle_data(api_version, configuration, instrument_key, interval, to_date, from_date=None):
    api_instance = upstox_client.HistoryApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_historical_candle_data(
        instrument_key, interval, to_date, api_version)
    return api_response


def get_intra_day_candle_data(api_version, configuration, instrument_key, interval):
    api_instance = upstox_client.HistoryApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_intra_day_candle_data(
        instrument_key, interval, api_version)
    return api_response


def get_brokerage(api_version, configuration, instrument_token, quantity, product, transaction_type, price):
    api_instance = upstox_client.ChargeApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_brokerage(
        instrument_token, quantity, product, transaction_type, price, api_version)
    return api_response


def get_portfolio_stream_feed_authorize(api_version, configuration):
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_portfolio_stream_feed_authorize(
        api_version)
    return api_response


def get_market_data_feed_authorize(api_version, configuration):
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    return api_response


def main():
    # Configure OAuth2 access token for authorization: OAUTH2
    configuration = upstox_client.Configuration()

    api_version = '2.0'
    client_id = "<API_KEY>"
    client_secret = "<API_SECRET>"
    redirect_uri = "<APP_REDIRECTION_URL>"
    auth_code = "<AUTH_CODE>"
    instrument_key = "NSE_EQ|INE848E01016"

    # Login and authorization
    access_token = login_and_authorize(
        api_version, configuration, client_id, client_secret, redirect_uri, auth_code)
    configuration.access_token = access_token

    # Get user profile
    profile = get_profile(api_version, configuration)
    pprint(profile)

    # Get funds and margin
    funds_margin = get_funds_and_margin(api_version, configuration)
    pprint(funds_margin)

    # Get positions
    positions = get_positions(api_version, configuration)
    pprint(positions)

    # Get holdings
    holdings = get_holdings(api_version, configuration)
    pprint(holdings)

    # Place order
    order_details = {
        "quantity": 1,
        "product": "D",
        "validity": "DAY",
        "price": 40,
        "tag": "string",
        "instrument_token": instrument_key,
        "order_type": "LIMIT",
        "transaction_type": "BUY",
        "disclosed_quantity": 0,
        "trigger_price": 0,
        "is_amo": False
    }
    place_order_response = place_order(
        api_version, configuration, order_details)
    pprint(place_order_response)
    order_id = place_order_response.data.order_id

    # Modify order
    modified_order_details = {
        "quantity": 1,
        "validity": "DAY",
        "price": 41,
        "order_id": order_id,
        "order_type": "LIMIT",
        "disclosed_quantity": 0,
        "trigger_price": 0
    }
    modify_order_response = modify_order(
        api_version, configuration, modified_order_details)
    pprint(modify_order_response)

    # Cancel order
    cancel_order_response = cancel_order(api_version, configuration, order_id)
    pprint(cancel_order_response)

    # Get trades by order
    trades_by_order = get_trades_by_order(api_version, configuration, order_id)
    pprint(trades_by_order)

    # Get trade history
    trade_history = get_trade_history(api_version, configuration)
    pprint(trade_history)

    # Get order book
    order_book = get_order_book(api_version, configuration)
    pprint(order_book)

    # Get order details
    order_details_response = get_order_details(
        api_version, configuration, order_id)
    pprint(order_details_response)

    # Place order CP
    order_details_cp = {
        "quantity": 1,
        "product": "D",
        "validity": "DAY",
        "price": 0,
        "tag": "string",
        "instrument_token": instrument_key,
        "order_type": "MARKET",
        "transaction_type": "BUY",
        "disclosed_quantity": 0,
        "trigger_price": 0,
        "is_amo": False
    }
    place_order_cp_response = place_order(
        api_version, configuration, order_details_cp)
    pprint(place_order_cp_response)

    # Convert positions
    convert_positions_details = {
        "instrument_token": instrument_key,
        "new_product": "I",
        "old_product": "D",
        "transaction_type": "BUY",
        "quantity": 1
    }
    convert_positions_response = convert_positions(
        api_version, configuration, convert_positions_details)
    pprint(convert_positions_response)

    # Get full market quote
    full_market_quote = get_full_market_quote(
        api_version, configuration, instrument_key)
    pprint(full_market_quote)

    # Get market quote OHLC
    interval = "1d"
    market_quote_ohlc = get_market_quote_ohlc(
        api_version, configuration, instrument_key, interval)
    pprint(market_quote_ohlc)

    # Get LTP
    ltp_response = ltp(api_version, configuration, instrument_key)
    pprint(ltp_response)

    # Get trade-wise profit and loss metadata
    segment = "EQ"
    year = "2223"
    trade_profit_loss_meta_data = get_trade_wise_profit_and_loss_meta_data(
        api_version, configuration, segment, year)
    pprint(trade_profit_loss_meta_data)

    # Get trade-wise profit and loss data
    trade_profit_loss_data = get_trade_wise_profit_and_loss_data(
        api_version, configuration, segment, year)
    pprint(trade_profit_loss_data)

    # Get profit and loss charges
    profit_loss_charges = get_profit_and_loss_charges(
        api_version, configuration, segment, year)
    pprint(profit_loss_charges)

    # Get historical candle data
    interval = "month"
    to_date = "2023-01-01"
    historical_candle_data = get_historical_candle_data(
        api_version, configuration, instrument_key, interval, to_date)
    pprint(historical_candle_data)

    # Get intra-day candle data
    interval = "30minute"
    intra_day_candle_data = get_intra_day_candle_data(
        api_version, configuration, instrument_key, interval)
    pprint(intra_day_candle_data)

    # Get brokerage
    quantity = 56  # int | Quantity with which the order is to be placed
    product = 'I'  # str | Product with which the order is to be placed
    transaction_type = 'BUY'  # str | Indicates whether its a BUY or SELL order
    price = 3.4  # float | Price with which the order is to be placed
    brokerage = get_brokerage(api_version, configuration,
                              instrument_key, quantity, product, transaction_type, price)
    pprint(brokerage)

    # Get portfolio stream feed authorize
    portfolio_stream_feed_authorize = get_portfolio_stream_feed_authorize(
        api_version, configuration)
    pprint(portfolio_stream_feed_authorize)

    # Get market data feed authorize
    market_data_feed_authorize = get_market_data_feed_authorize(
        api_version, configuration)
    pprint(market_data_feed_authorize)


if __name__ == '__main__':
    main()
