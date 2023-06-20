from flask import Flask, request
import africastalking
from ussd import handle_ussd_callback

# Initialize Africa's Talking API
username = "<shieldedApp>"
api_key = "<84b3ed23535f2352fa0a5d022da04f27c319f59d62d93f60c8927d89d933cc2c>"
africastalking.initialize(username, api_key)
sms = africastalking.SMS
airtime = africastalking.Airtime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    return handle_ussd_callback(session_id, service_code, phone_number, text, sms, airtime)

if __name__ == '__main__':
    app.run()
