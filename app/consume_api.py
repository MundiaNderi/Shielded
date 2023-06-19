import requests
import json
import pprint

url = 'https://api.sandbox.africastalking.com/version1airtme/send'

parameters = {
    'api_key': "58d691a0af4a9082922b4a71deb45f9fc89632f8993260e4679d423b1b5d722f",
    'username': "shielded"
}

headers = {
    "api_key": "58d691a0af4a9082922b4a71deb45f9fc89632f8993260e4679d423b1b5d722f",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accepts": "application/json"
}

response = requests.get(url, params=parameters, headers=headers)

pprint.pprint(response.json())
