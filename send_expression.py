#!/usr/bin/env python3
"""
Daily English Expression Bot for Telegram
Sends a random English expression to your Telegram chat daily.
"""

import json
import os
import random
from pathlib import Path

import requests


def load_expressions() -> list:
    """Load expressions from the JSON database."""
    script_dir = Path(__file__).parent
    data_file = script_dir / "data" / "expressions.json"

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["expressions"]


def get_random_expression(expressions: list) -> dict:
    """Select a random expression from the list."""
    return random.choice(expressions)


def format_message(expression: dict) -> str:
    """Format the expression as a Telegram message."""
    message = f"""🌟 *오늘의 영어 표현* 🌟

📚 *Expression:* {expression['expression']}

💡 *Meaning:* {expression['meaning']}

🇰🇷 *뜻:* {expression['meaning_kr']}

📝 *Example:*
_{expression['example']}_

━━━━━━━━━━━━━━━
Have a great day! 좋은 하루 보내세요! 🚀"""

    return message


def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Message sent successfully!")
        return True
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
        return False


def main():
    """Main function to send daily English expression."""
    # Get environment variables
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    if not chat_id:
        raise ValueError("TELEGRAM_CHAT_ID environment variable is not set")

    # Load expressions and select random one
    expressions = load_expressions()
    expression = get_random_expression(expressions)

    # Format and send message
    message = format_message(expression)
    success = send_telegram_message(bot_token, chat_id, message)

    if not success:
        raise RuntimeError("Failed to send Telegram message")

    print(f"Sent expression: {expression['expression']}")


if __name__ == "__main__":
    main()
