import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))

# Full market quotes for a single instrument
try:
    api_response = api_instance.get_full_market_quote_v3(instrument_key="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_full_market_quote_v3 with a single instrument_key")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3 single: %s\n" % e)

# Full market quotes for multiple instruments
try:
    api_response = api_instance.get_full_market_quote_v3(
        instrument_key="NSE_EQ|INE669E01016,NSE_INDEX|Nifty 50")
    if api_response.status != "success":
        print("error in get_full_market_quote_v3 with multiple instrument_keys")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3 multiple: %s\n" % e)

# Full market quotes without any filter
try:
    api_response = api_instance.get_full_market_quote_v3()
    if api_response.status != "success":
        print("error in get_full_market_quote_v3 without instrument_key")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_full_market_quote_v3 no filter: %s\n" % e)

# LTP quotes
try:
    api_response = api_instance.get_ltp(instrument_key="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_ltp")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_ltp: %s\n" % e)

# OHLC quotes
try:
    api_response = api_instance.get_market_quote_ohlc("I1", instrument_key="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_market_quote_ohlc")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_ohlc: %s\n" % e)

# Option greeks
try:
    api_response = api_instance.get_market_quote_option_greek(instrument_key="NSE_FO|38516")
    if api_response.status != "success":
        print("error in get_market_quote_option_greek")
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_option_greek: %s\n" % e)

# Model instantiation tests
ohlc = upstox_client.OhlcV3(
    open=100.5,
    high=110.25,
    low=99.75,
    close=105.0,
    volume=125000,
    ts=1788590331000
)
if ohlc.open != 100.5:
    print("error: OhlcV3 open field not set correctly")
if ohlc.volume != 125000:
    print("error: OhlcV3 volume field not set correctly")

buy_depth = upstox_client.Depth(quantity=50, price=104.95, orders=3)
sell_depth = upstox_client.Depth(quantity=75, price=105.05, orders=4)
depth = upstox_client.DepthMap(buy=[buy_depth], sell=[sell_depth])
if depth.buy[0].quantity != 50:
    print("error: DepthMap buy field not set correctly")
if depth.sell[0].price != 105.05:
    print("error: DepthMap sell field not set correctly")

symbol = upstox_client.MarketQuoteSymbolV3(
    ohlc=ohlc,
    depth=depth,
    timestamp="2026-09-05T09:15:00+05:30",
    instrument_token="NSE_EQ|INE669E01016",
    symbol="IDEA",
    last_price=105.0,
    volume=125000,
    average_price=104.5,
    oi=8500.0,
    net_change=4.5,
    total_buy_quantity=12000.0,
    total_sell_quantity=11500.0,
    lower_circuit_limit=94.5,
    upper_circuit_limit=115.5,
    last_trade_time="2026-09-05T09:14:59+05:30",
    oi_day_high=9100.0,
    oi_day_low=8100.0,
    prev_close_price=100.5,
    year_high=140.0,
    year_low=80.0,
    previous_oi=8300.0,
    indicative_equilibrium_price=105.25,
    reference_price=100.5,
    indicative_equilibrium_quantity=4500,
    indicative_imbalance_quantity_total=1200,
    indicative_imbalance_quantity_market=300,
    cas_eligible=True
)
if symbol.symbol != "IDEA":
    print("error: MarketQuoteSymbolV3 symbol field not set correctly")
if symbol.last_price != 105.0:
    print("error: MarketQuoteSymbolV3 last_price field not set correctly")
if symbol.volume != 125000:
    print("error: MarketQuoteSymbolV3 volume field not set correctly")
if symbol.cas_eligible is not True:
    print("error: MarketQuoteSymbolV3 cas_eligible field not set correctly")
if symbol.indicative_equilibrium_quantity != 4500:
    print("error: MarketQuoteSymbolV3 indicative_equilibrium_quantity field not set correctly")
if symbol.ohlc.close != 105.0:
    print("error: MarketQuoteSymbolV3 nested ohlc field not set correctly")
if symbol.depth.buy[0].orders != 3:
    print("error: MarketQuoteSymbolV3 nested depth field not set correctly")

full_quote_response = upstox_client.GetFullMarketQuoteResponseV3(
    status="success",
    data={"NSE_EQ:IDEA": symbol}
)
if full_quote_response.status != "success":
    print("error: GetFullMarketQuoteResponseV3 status field not set correctly")
if full_quote_response.data["NSE_EQ:IDEA"].symbol != "IDEA":
    print("error: GetFullMarketQuoteResponseV3 data field not set correctly")
if full_quote_response.to_dict()["data"]["NSE_EQ:IDEA"]["last_price"] != 105.0:
    print("error: GetFullMarketQuoteResponseV3 to_dict did not serialise nested data")

try:
    upstox_client.GetFullMarketQuoteResponseV3(status="not_a_valid_status")
    print("error: GetFullMarketQuoteResponseV3 accepted an invalid status value")
except ValueError:
    pass
