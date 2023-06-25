import africastalking
from dotenv import load_dotenv
import os

"""Initialize Africa's Talking"""
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)

sms = africastalking.SMS


class send_sms():
    def send(self):
        recipients = ["+254716299581"]
        message = "Hey Shielded Ninja!"
        sender = "+254700000000"
        try:
            response = sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print(f'Nairobi, we have a problem: {e}')


# Create an instance of the send_sms class
sms_instance = send_sms()

# Call the send method
sms_instance.send()
