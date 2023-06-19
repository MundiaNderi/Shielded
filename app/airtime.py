"""Import the Africa's Talking module here"""
import africastalking
import requests
import pprint

url = "https://api.sandbox.africastalking.com/version1/airtime/send"


"""Authenticate with the service"""
username = "sandbox"
api_key = "35e3faad2fda8ffe4c35ca4a232c279b08cb4205f14adc9ea22c8776ddf7561a"
africastalking.initialize(username, api_key)


"""Create an instance of the Airtime class"""
airtime = africastalking.Airtime

phone_number = "+254717209081"  # In international format
currency_code = "KES"  # Change this to your country's code
amount = 270

try:
    response = airtime.send(phone_number=phone_number,
                            amount=amount, currency_code=currency_code)
    print(f"the results is {response}")

except Exception as e:
    print(
        f"Encountered an error while sending airtime. More error details below\n {e}")

"""This data parameter contains the form data as a dictionary"""
"""data = {
    "username": "sandbox",
    "recipients": [{"phoneNumber": phone_number, "currencyCode": currency_code}]
}

# response = requests.post(url, headers=headers, data=data)
response_json = response.json()"""
