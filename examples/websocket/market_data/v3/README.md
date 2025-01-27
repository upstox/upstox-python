# Market Stream feed websocket client

This Python project demonstrates how to connect to the Upstox Websocket API for streaming live market data. It fetches market data for a list of instrument keys and decodes the incoming protobuf data to a JSON format.

## Getting Started

These instructions will help you run the sample v3 websocket client.

### Prerequisites

Before you can run this script, you need to have Python 3.8 or later installed on your system. If you haven't installed Python yet, you can download it from the official website:

[Download Python](https://www.python.org/downloads/)

You will also need to install several Python packages:

- `websockets`
- `asyncio`
- `protobuf`
- `requests`


You can install these packages using pip, a package manager for Python. Open a terminal and enter the following command:

```sh
pip install websockets asyncio protobuf requests
```

### Protocol Buffers (Protobuf) Classes Generation

Generate the Protobuf classes in Python from `.proto` file.

Before you can generate the Protobuf classes, you need to download the [proto file](https://assets.upstox.com/feed/market-data-feed/v3/MarketDataFeed.proto) and install the Protocol Buffers compiler (protoc).

To download the Protocol Buffers compiler, go to the [Google Protocol Buffers GitHub repository](https://github.com/protocolbuffers/protobuf/releases) and download the appropriate `protoc-<version>-<os>.zip` file for your operating system. Extract the ZIP file and add the `bin` directory to your system PATH.

For example, on a Unix-like system, you can add the directory to your PATH like this:

```bash
export PATH=$PATH:/path/to/protoc/bin
```

You can confirm that the compiler is correctly installed by opening a new terminal window and running the following command:

```
protoc --version
```

This should print the protoc version.

#### Generate Protobuf classes

Navigate to the directory containing your .proto files and run the following command:

```
protoc --python_out=. *.proto
```

This will generate .py files for each .proto file in the directory.

In your Python code, you can now import the generated classes like any other Python module. For example, if you have a file MarketDataFeedV3.proto and you've generated MarketDataFeedV3_pb2.py, you can import it like this:

```
import MarketDataFeedV3_pb2 as pb
```

Sample class (MarketDataFeedV3_pb2.py) included as part of this repo.

### Configuration

The script requires an Upstox API access token for authorization. You will need to specify your Upstox API access token in the Python script. Look for the line below and replace 'ACCESS_TOKEN' with your actual access token.

```
access_token = 'ACCESS_TOKEN'
```

### Running the Script

After installing the prerequisites and setting up your access token, you can run the script. Navigate to the directory containing the script and run the following command:

```
python3 websocket_client.py
```

Replace websocket_client.py with the name of your Python script.

## Understanding the Code

The script first sets up an SSL context. It then fetches the authorized redirect URI from the Upstox server using a valid access token and utilizes this URI to establish a connection with the WebSocket server.

The script sends a subscription request for "NSE_INDEX|Nifty Bank" and "NSE_INDEX|Nifty 50". When it receives data from the server, it decodes the protobuf data into a FeedResponse object, converts this object into a dictionary, and then prints the dictionary.

## Support

If you encounter any problems or have any questions about this project, feel free to post it on our [Developer Community](https://community.upstox.com/c/developer-api/15).

## Disclaimer

This is a sample script meant for educational purposes. It may require modifications to work with your specific requirements.

Please replace `'ACCESS_TOKEN'` with your actual access token and `websocket_client.py` with the name of your Python script. Modify any other details as needed to fit your project.


