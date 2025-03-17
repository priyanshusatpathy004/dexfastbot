import requests
import time

# Telegram bot token
BOT_TOKEN = "7874452701:AAHKzqafmdS21jqXWENYyKY7eZbtgftOEyg"
# Your Telegram chat ID (replace with your actual chat ID)
CHAT_ID = "-4617340853"

# DEX Screener API URL for latest tokens
API_URL = "https://api.dexscreener.com/token-profiles/latest/v1"



# Store known token addresses to track new arrivals
known_tokens = set()

def send_telegram_message(message):
    """Send a message to the Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def check_new_tokens():
    """Fetch latest tokens and compare with known ones."""
    global known_tokens
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        for token in data:  # Assuming response is a list of tokens
            token_address = token["tokenAddress"]
            chain_id = token.get("chainId", "Unknown")  # Extract chainId

            if token_address not in known_tokens:
                known_tokens.add(token_address)
                message = f"🚀 New Token Detected!\n\n🔗 URL: {token['url']}\n🏷 Address: {token_address}\n🔗 Chain ID: {chain_id}\n📜 Description: {token.get('description', 'No description')}"
                send_telegram_message(message)

# Run the script continuously
while True:
    check_new_tokens()
    time.sleep(5)  # Check every 1 seconds
