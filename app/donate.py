from flask import Flask
from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# mpesa details
load_dotenv()
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
