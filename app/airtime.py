"""Import the Africa's Talking module here"""
import africastalking
from dotenv import load_dotenv
import os

url = "https://api.sandbox.africastalking.com/version1/airtime/send"


"""Authenticate with the service"""
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)

"""Create an instance of the Airtime class"""
airtime = africastalking.Airtime


def top_up_airtime(phone_number, amount, currency_code):
    try:
        response = airtime.send(phone_number=phone_number,
                                amount=amount, currency_code=currency_code)
        print(f"the results is {response}")

    except Exception as e:
        print(e)
        print(
            f"Encountered an error while sending airtime. More error details below\n {e}")
