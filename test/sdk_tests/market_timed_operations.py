import upstox_client
import data_token
import threading
import time

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

# Initialize streamer with "NSE_INDEX|Nifty 50" in "full" mode
streamer = upstox_client.MarketDataStreamerV3(
    upstox_client.ApiClient(configuration), 
    instrumentKeys=["NSE_INDEX|Nifty 50"], 
    mode="full"
)

streamer.auto_reconnect(True, 5, 10)

# Timer references for cleanup
timers = []

def on_open():
    print("WebSocket connection opened")
    print("Initial subscription: NSE_INDEX|Nifty 50 in 'full' mode")
    
    timer1 = threading.Timer(6, subscribe_bank_nifty)
    timer1.start()
    timers.append(timer1)
    
    timer2 = threading.Timer(15, unsubscribe_nifty_50)
    timer2.start()
    timers.append(timer2)
    
    timer3 = threading.Timer(30, change_mode_to_d30)
    timer3.start()
    timers.append(timer3)
    
    timer4 = threading.Timer(50, cleanup_and_exit)
    timer4.start()
    timers.append(timer4)

def subscribe_bank_nifty():
    print("\n[1 MINUTE] Subscribing to 'NSE_INDEX|Nifty Bank' in 'full' mode")
    try:
        streamer.subscribe(["NSE_INDEX|Nifty Bank"], "full")
        print("Successfully subscribed to Nifty Bank")
    except Exception as e:
        print(f"Error subscribing to Nifty Bank: {e}")

def unsubscribe_nifty_50():
    print("\n[2 MINUTES] Unsubscribing from 'NSE_INDEX|Nifty 50'")
    try:
        streamer.unsubscribe(["NSE_INDEX|Nifty 50"])
        print("Successfully unsubscribed from Nifty 50")
    except Exception as e:
        print(f"Error unsubscribing from Nifty 50: {e}")

def change_mode_to_d30():
    print("\n[3 MINUTES] Changing mode to 'full_d30' for all remaining subscriptions")
    try:
        # Change mode for Nifty Bank (which should be the only remaining subscription)
        streamer.change_mode(["NSE_INDEX|Nifty Bank"], "full_d30")
        print("Successfully changed mode to 'full_d30' for Nifty Bank")
    except Exception as e:
        print(f"Error changing mode to full_d30: {e}")

def cleanup_and_exit():
    print("\n[4 MINUTES] Cleaning up and disconnecting...")
    try:
        # Cancel any remaining timers
        for timer in timers:
            if timer.is_alive():
                timer.cancel()
        
        # Disconnect the streamer
        if hasattr(streamer, 'disconnect'):
            streamer.disconnect()
        elif hasattr(streamer, 'feeder') and streamer.feeder and hasattr(streamer.feeder, 'ws'):
            streamer.feeder.ws.close()
        
        print("Cleanup completed. Exiting...")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def on_close(a, b):
    print(f"WebSocket connection closed: {a}")

def on_message(data):
    try:
        if isinstance(data, dict) and data.get('type') == 'live_feed':
            feeds = data.get('feeds', {})
            
            for instrument_key, feed_data in feeds.items():
                mode = feed_data.get('requestMode', 'Unknown')
                
                # Extract LTP based on the feed structure
                ltp = None
                if 'fullFeed' in feed_data:
                    # Full mode data structure
                    full_feed = feed_data['fullFeed']
                    if 'indexFF' in full_feed and 'ltpc' in full_feed['indexFF']:
                        ltp = full_feed['indexFF']['ltpc'].get('ltp')
                    elif 'ltpc' in full_feed:
                        ltp = full_feed['ltpc'].get('ltp')
                elif 'ltpc' in feed_data:
                    # LTPC mode data structure
                    ltp = feed_data['ltpc'].get('ltp')
                
                print(f"[{mode.upper()}] {instrument_key} - LTP: {ltp}")
        else:
            # Fallback for other message types
            print(f"Other message: {data}")
            
    except Exception as e:
        print(f"Error parsing message: {e}")
        print(f"Raw data: {data}")

def on_error(er):
    print(f"WebSocket error: {er}")

def on_reconnecting(data):
    print(f"Reconnecting event: {data}")

# Register event handlers
streamer.on("open", on_open)
streamer.on("message", on_message)
streamer.on("close", on_close)
streamer.on("reconnecting", on_reconnecting)
streamer.on("error", on_error)

print("Starting MarketDataStreamerV3 with timed operations...")
print("Timeline:")
print("  0 min: Connect with 'NSE_INDEX|Nifty 50' in 'full' mode")
print("  1 min: Subscribe to 'NSE_INDEX|Nifty Bank' in 'full' mode")
print("  2 min: Unsubscribe from 'NSE_INDEX|Nifty 50'")
print("  3 min: Change mode to 'full_d30' for remaining subscriptions")
print("  4 min: Cleanup and exit")
print("\nConnecting...")

# Start the connection
streamer.connect()

# Keep the main thread alive to allow timers to execute
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Cleaning up...")
    cleanup_and_exit()
