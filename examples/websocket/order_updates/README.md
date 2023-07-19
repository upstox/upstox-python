# Portfolio Stream Feed WebSocket Client

This Python project demonstrates how to connect to the Upstox WebSocket API for streaming live order updates. It fetches the order updates and prints them to the console.

## Getting Started

These instructions will help you run the sample websocket client.

### Prerequisites

Before you can run this script, you need to have Python 3.8 or later installed on your system. If you haven't installed Python yet, you can download it from the official website:

[Download Python](https://www.python.org/downloads/)

You will also need to install several Python packages:

- `upstox-python-sdk`
- `websockets`
- `asyncio`

You can install these packages using pip, a package manager for Python. Open a terminal and enter the following command:

```sh
pip install upstox-python-sdk websockets asyncio
```

### Configuration

The script requires an Upstox API access token for authorization. You will need to specify your Upstox API access token in the Python script. Look for the line below and replace 'ACCESS_TOKEN' with your actual access token.

```
configuration.access_token = 'ACCESS_TOKEN'
```

### Running the Script

After installing the prerequisites and setting up your access token, you can run the script. Navigate to the directory containing the script and run the following command:

```
python3 websocket_client.py
```

Replace websocket_client.py with the name of your Python script.

## Understanding the Code

The script first sets up an SSL context and an OAuth2 access token for authorization. It fetches the authorized redirect URI from the Upstox server and uses this to establish a connection to the WebSocket server.

The script then enters a loop, where it continually receives order update messages from the server and prints them to the console..

## Support

If you encounter any problems or have any questions about this project, feel free to open an issue in this repository.

## Disclaimer

This is a sample script meant for educational purposes. It may require modifications to work with your specific requirements.

Please replace `'ACCESS_TOKEN'` with your actual access token and `websocket_client.py` with the name of your Python script. Modify any other details as needed to fit your project.


