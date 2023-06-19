"""Import the Africa's Talking module here"""
import africastalking
import requests

url = "https://api.sandbox.africastalking.com/version1/airtime/send"


"""Authenticate with the service"""
username = "sandbox"
api_key = "58d691a0af4a9082922b4a71deb45f9fc89632f8993260e4679d423b1b5d722f"
africastalking.initialize(username, api_key)


"""Create an instance of the Airtime class"""
airtime = africastalking.Airtime

phone_number = "+254716299581"  # In international format
currency_code = "KES"  # Change this to your country's code
amount = 100

try:
    response = airtime.send(phone_number=phone_number,
                            amount=amount, currency_code=currency_code)
    print(response)
except Exception as e:
    print(
        "Encountered an error while sending airtime. More error details below\n {e}")

"""This data parameter contains the form data as a dictionary"""
data = {
    "username": "sandbox",
    "recipients": [{"phoneNumber": phone_number, "currencyCode": currency_code}]
}

response = requests.post(url, headers=headers, data=data)
response_json = response.json()
