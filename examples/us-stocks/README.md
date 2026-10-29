# US Stocks – Example code

Links to all US stocks examples in the `code/` folder. Endpoints are exposed on
`UsStocksOrderApi`, `UsStocksChargesApi`, `UsStocksPortfolioApi`,
`UsStocksFundsApi` and `UsMarketHolidaysAndTimingsApi`. Prices and amounts are in USD.

> ⚠️ US stocks endpoints are currently available on UAT only. Until they reach
> production, point both hosts at UAT:
>
> ```python
> configuration.host = 'https://uat-api.upstox.com'
> configuration.order_host = 'https://uat-api.upstox.com'
> ```
>
> `order_host` is needed because place/modify/cancel requests are routed to it.

## 1. Place Order

- 1.1 [Place a market order by quantity](code/place-us-order.md#place-a-market-order-by-quantity)
- 1.2 [Place a market order by USD amount](code/place-us-order.md#place-a-market-order-by-usd-amount)
- 1.3 [Place a limit order](code/place-us-order.md#place-a-limit-order)

## 2. Modify Order

- 2.1 [Modify an open order](code/modify-us-order.md#modify-an-open-order)

## 3. Cancel Order

- 3.1 [Cancel an open order](code/cancel-us-order.md#cancel-an-open-order)

## 4. Order Book & Order Details

- 4.1 [Get US order book](code/get-us-orders.md#get-us-order-book)
- 4.2 [Get US order details by order id](code/get-us-orders.md#get-us-order-details-by-order-id)

## 5. Charges & Margin

- 5.1 [Estimate charges for a market order](code/us-charges-and-margin.md#estimate-charges-for-a-market-order)
- 5.2 [Estimate charges for a limit order](code/us-charges-and-margin.md#estimate-charges-for-a-limit-order)
- 5.3 [Calculate margin for multiple orders](code/us-charges-and-margin.md#calculate-margin-for-multiple-orders)

## 6. Funds & Holdings

- 6.1 [Get US funds](code/us-funds-and-holdings.md#get-us-funds)
- 6.2 [Get US holdings](code/us-funds-and-holdings.md#get-us-holdings)

## 7. Market Status, Holidays & Timings

- 7.1 [Get US market status](code/us-market-information.md#get-us-market-status)
- 7.2 [Get US market holidays for the year](code/us-market-information.md#get-us-market-holidays-for-the-year)
- 7.3 [Get US market holiday on a date](code/us-market-information.md#get-us-market-holiday-on-a-date)
- 7.4 [Get US market timings on a date](code/us-market-information.md#get-us-market-timings-on-a-date)
