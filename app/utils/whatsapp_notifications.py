import requests
from flask import current_app
import json

class WhatsAppNotifier:
    def __init__(self, app, phone_id, token):
        self.app = app
        self.token = token.strip() if token else None
        self.phone_id = phone_id.strip() if phone_id else None
        self.api_url = f"https://graph.facebook.com/v21.0/{self.phone_id}/messages" 
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # # Log initialization details for debugging
        # current_app.logger.info(f"WhatsApp API URL: {self.api_url}")
        # current_app.logger.info(f"Phone ID: {self.phone_id}")
        # # Log first few characters of token for debugging
        # if self.token:
        #     current_app.logger.info(f"Token starts with: {self.token[:5]}...")

    def send_message(self, to_number, message, use_template=False):
        try:
            to_number = to_number.strip()
            if use_template:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_number,
                    "type": "template",
                    "template": {
                        "name": "hello_world",
                        "language": {
                            "code": "en_US"
                        }
                    }
                }
            else:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_number,
                    "type": "text",
                    "text": {"body": message}
                }
            
            # # Log the complete request for debugging
            # current_app.logger.info(f"Sending request to: {self.api_url}")
            # current_app.logger.info(f"Headers: {json.dumps(self.headers)}")
            # current_app.logger.info(f"Payload: {json.dumps(payload)}")

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,  # Using json parameter instead of data
                timeout=10  # Adding timeout
            )

            # # Log response details
            # current_app.logger.info(f"Response Status Code: {response.status_code}")
            # current_app.logger.info(f"Response Content: {response.text}")
            self.app.logger.info(f"Whatsapp message sent to <{to_number}>")

            return response.status_code in [200, 201]

        except requests.RequestException as e:
            current_app.logger.error(f"Request error: {str(e)}")
            return False
        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            return False

    def format_signup_message(self, player_name, game_date, game_time, location):
        return (
            f"🏐 Volleyball Game Signup Confirmation\n\n"
            f"Hi {player_name}!\n"
            f"You're confirmed for the game on:\n"
            f"📅 {game_date}\n"
            f"🕒 {game_time}\n"
            f"📍 {location}\n\n"
            f"See you on the court! 🎉"
        )

    def format_cancellation_message(self, player_name, game_date):
        return (
            f"Hi {player_name},\n\n"
            f"Your signup for the volleyball game on {game_date} has been cancelled.\n"
            f"Hope to see you at future games! 🏐"
        )