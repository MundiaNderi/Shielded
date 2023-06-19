import requests
import json

response = requests.get(
    'https://api.sandbox.africastalking.com/version1/airtime/send/')
print(response.json)
