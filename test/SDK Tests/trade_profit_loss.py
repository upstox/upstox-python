import upstox_client
from upstox_client.rest import ApiException
import const_file
configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token

api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'EQ'
financial_year = '2324' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
api_version = '2.0' # str | API Version Header
from_date = '02-04-2023' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = '20-03-2024' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_trade_wise_profit_and_loss_meta_data(segment, financial_year, api_version, from_date=from_date, to_date=to_date)
    print(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)

api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'EQ'
financial_year = '2324' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
page_number = 1
page_size = 4
api_version = '2.0' # str | API Version Header
from_date = '02-04-2023' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = '20-03-2024' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_trade_wise_profit_and_loss_data(segment, financial_year, page_number, page_size, api_version, from_date=from_date, to_date=to_date)
    print(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)

api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'EQ'
financial_year = '2324' # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
api_version = '2.0' # str | API Version Header
from_date = '02-04-2023' # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = '20-03-2024' # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_profit_and_loss_charges(segment, financial_year, api_version, from_date=from_date, to_date=to_date)
    print(api_response)
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)
