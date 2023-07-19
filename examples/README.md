# Python Sample Implementation

## Websocket

### Market stream feed

Python script to connect to the Upstox Websocket API for streaming live market data. It fetches market data for a list of instrument keys and decodes the incoming protobuf data to a JSON format.

[Market updates using Upstox's websocket](websocket/market_data/)

### Porfolio stream feed

Python scripts to connect to the Upstox WebSocket API for streaming live order updates. It fetches the order updates and prints them to the console.

[Order updates using Upstox's websocket](websocket/order_updates/)