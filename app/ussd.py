from send_sms import sms
from airtime import top_up_airtime
from flask import Flask, request
import os

app = Flask(__name__)
response = ""


@app.route('/', methods=['POST'])
def handle_ussd_callback(phone_number, text):
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    from crud import get_case_officer_details, save_ussd, get_safe_house_location, get_staff_details
    if text == "":
        # Initial USSD request
        response = "CON Welcome to Shielded!. How may we help you today?\n"
        response += "1. Talk to a case officer\n"
        response += "2. Access a Safe house\n"
        response += "3. Request airtime\n"
        response += "4. Speak to one of us"
    elif text == "1":
        # Option 1: Talk to a case officer
        case_officer_details = get_case_officer_details()
        sms(phone_number, "Case officer contact details:\nName: {}\nPhone: {}".format(
            case_officer_details['name'], case_officer_details['phone']))
        response = "END We will send an SMS with the case officer's contact information shortly.Feel free to reach out to them. Thank you."
        save_ussd(phone_number)

    elif text == "2":
        # Option 2: Access a Safe house
        response = "CON Select a safe house location closest to you:\n"
        response += "1. Location 1\n"
        response += "2. Location 2\n"
        response += "3. Location 3"

    elif text in ["1", "2", "3"]:
        # User has selected a safe house location
        safe_house_location = get_safe_house_location(text)
        sms(phone_number, "Safe house location: \nName: {}\nLocation: {}\nManager: {}\nContact: {}".format(
            safe_house_location['name'], safe_house_location['location'], safe_house_location['manager'], safe_house_location['contact']))

        """safe_house_location.name, safe_house_location.location"""
        response = "END Details of the Safe house location nearest to you has been sent to your phone."
        save_ussd(phone_number)

    elif text == "3":
        # Option 3: Request airtime
        top_up_airtime()
        sms(phone_number, "Your account has been topped up with airtime.")

        response = "END Your account has been topped up with airtime."
        save_ussd(phone_number)

    elif text == "4":
        # Option 4: Speak to one of us
        staff_details = get_staff_details()
        sms(phone_number, "Staff contact details:\nName: {}\nPhone: {}".format(
            staff_details['name'], staff_details['phone']))

        response = "END The contact details of one of our staff has been sent to your phone."

        save_ussd(phone_number)

    else:
        # Invalid input
        response = "END Invalid input. Please try again."

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
