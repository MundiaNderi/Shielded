import africastalking
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Africa's Talking


class sms:

    def send(phone_numbers, message):
        username = os.environ['USERNAME']
        api_key = os.environ['API_KEY']

        # Send message
        recipients = [phone_numbers]
        message = message
        africastalking.initialize(username, api_key)

        # Create an instance of the SMS class
        sms = africastalking.SMS
        print(message)
        print(recipients)
        try:
            response = sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')
            print(e)
