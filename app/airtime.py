"""Import the Africa's Talking module here"""
import africastalking
from dotenv import load_dotenv
import requests
import pprint
import os

url = "https://api.sandbox.africastalking.com/version1/airtime/send"


"""Authenticate with the service"""
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)

"""Create an instance of the Airtime class"""
airtime = africastalking.Airtime

phone_number = "+254716299581"  # In international format
currency_code = "KES"  # Change this to your country's code
amount = 20


def top_up_airtime(phone_number, amount, currency_code):
    try:
        response = airtime.send(phone_number=phone_number,
                                amount=amount, currency_code=currency_code)
        print(f"the results is {response}")

    except Exception as e:
        print(e)
        print(
            f"Encountered an error while sending airtime. More error details below\n {e}")


top_up_airtime(phone_number, amount, currency_code)
