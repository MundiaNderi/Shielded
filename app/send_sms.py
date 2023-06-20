import africastalking
from dotenv.main import load_dotenv
import os

"""Initialize Africa's Talking"""
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)

sms = africastalking.SMS


class send_sms():
    def send(self):
        def sending(self):
            """Set the numbers in an international format"""
            recipients = [+254716299581]
            """Set your message"""
            message = "Hey Shielded Ninja!"
            sender = "Shielded"
            try:
                response = self.sms.send(message, recipients, sender)
                print(response)
            except Exception as e:
                print(f'Nairobi, we have a problem: {e}')
