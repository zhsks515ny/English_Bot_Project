#!/usr/bin/env python3
"""
Daily English Expression Bot for KakaoTalk
Sends a random English expression to your KakaoTalk daily.
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


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    """Refresh the access token using refresh token."""
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        result = response.json()
        return result.get("access_token")
    else:
        print(f"Failed to refresh token: {response.text}")
        return None


def send_kakao_message(access_token: str, expression: dict) -> bool:
    """Send a message to KakaoTalk (to myself)."""
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Create message template
    template = {
        "object_type": "text",
        "text": f"""🌟 오늘의 영어 표현 🌟

📚 Expression: {expression['expression']}

💡 Meaning: {expression['meaning']}

🇰🇷 뜻: {expression['meaning_kr']}

📝 Example:
{expression['example']}

━━━━━━━━━━━━━━━
Have a great day! 좋은 하루 보내세요! 🚀""",
        "link": {
            "web_url": "https://github.com",
            "mobile_web_url": "https://github.com"
        }
    }

    data = {
        "template_object": json.dumps(template)
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("KakaoTalk message sent successfully!")
        return True
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
        return False


def main():
    """Main function to send daily English expression."""
    # Get environment variables
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    client_secret = os.environ.get("KAKAO_CLIENT_SECRET")
    access_token = os.environ.get("KAKAO_ACCESS_TOKEN")
    refresh_token = os.environ.get("KAKAO_REFRESH_TOKEN")

    if not client_id:
        raise ValueError("KAKAO_CLIENT_ID environment variable is not set")
    if not client_secret:
        raise ValueError("KAKAO_CLIENT_SECRET environment variable is not set")
    if not access_token:
        raise ValueError("KAKAO_ACCESS_TOKEN environment variable is not set")
    if not refresh_token:
        raise ValueError("KAKAO_REFRESH_TOKEN environment variable is not set")

    # Load expressions and select random one
    expressions = load_expressions()
    expression = get_random_expression(expressions)

    # Try to send message
    success = send_kakao_message(access_token, expression)

    # If failed, try refreshing the token
    if not success:
        print("Trying to refresh access token...")
        new_access_token = refresh_access_token(client_id, client_secret, refresh_token)

        if new_access_token:
            print(f"New access token obtained!")
            success = send_kakao_message(new_access_token, expression)
        else:
            raise RuntimeError("Failed to refresh access token")

    if not success:
        raise RuntimeError("Failed to send KakaoTalk message")

    print(f"Sent expression: {expression['expression']}")


if __name__ == "__main__":
    main()
