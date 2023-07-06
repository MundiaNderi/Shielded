import africastalking
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Africa's Talking


class sms:
    def __init__(self):
        self.username = os.environ['USERNAME']
        self.api_key = os.environ['API_KEY']

    def send(self):
        # Send message
        recipients = ["+254716299581"]
        message = "Hello from Africa's Talking!"
        africastalking.initialize(self.username, self.api_key)

        # Create an instance of the SMS class
        sms = africastalking.SMS

        try:
            response = sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')
            print(e)


sms().send()
