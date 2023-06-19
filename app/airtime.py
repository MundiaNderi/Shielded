"""Import the Africa's Talking module here"""
import africastalking
import requests

"""Authenticate with the service"""
username = "sandbox"
api_key = "58d691a0af4a9082922b4a71deb45f9fc89632f8993260e4679d423b1b5d722f"

africastalking.initialize(username, api_key)

phone_number = "+254716299581"  # In international format
currency_code = "KES"  # Change this to your country's code


url = "https://api.sandbox.africastalking.com/version1/airtime/send"

"""Adding headers by passing them as a dictionary"""
headers = {
    "apiKey": "58d691a0af4a9082922b4a71deb45f9fc89632f8993260e4679d423b1b5d722f",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}

"""This data parameter contains the form data as a dictionary"""
data = {
    "username": "sandbox",
    "recipients": [{"phoneNumber": phone_number, "currencyCode": currency_code}]
}

response = requests.post(url, headers=headers, data=data)
response_json = response.json()
