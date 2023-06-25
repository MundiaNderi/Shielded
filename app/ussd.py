import africastalking
from sms import send_sms
from airtime import top_up_airtime
from database import get_case_officer_details, get_safe_house_location, get_staff_details
import sys


def send_sms():
    pass


def top_up_airtime():
    pass


def handle_ussd_callback(session_id, service_code, phone_number, text, sms, airtime):
    response = ""

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
        send_sms(phone_number, "Case officer contact details:\nName: {}\nPhone: {}".format(
            case_officer_details['name'], case_officer_details['phone']))
        response = "END We will send an SMS with the case officer's contact information shortly.Feel free to reach out to them. Thank you."
    elif text == "2":
        # Option 2: Access a Safe house
        response = "CON Select a safe house location closest to you:\n"
        response += "1. Location 1\n"
        response += "2. Location 2\n"
        response += "3. Location 3"
    elif text in ["1", "2", "3"]:
        # User has selected a safe house location
        safe_house_location = get_safe_house_location(text)
        send_sms(phone_number, "Safe house location: \nName: {}\nLocation: {}\nManager: {}\nContact: {}".format(
            safe_house_location['name'], safe_house_location['location'], safe_house_location['manager'], safe_house_location['contact']))

        response = "END Details of the Safe house location nearest to you has been sent to your phone."
    elif text == "3":
        # Option 3: Request airtime
        top_up_airtime(phone_number)
        send_sms(phone_number, "Your account has been topped up with airtime.")

        response = "END Your account has been topped up with airtime."
    elif text == "4":
        # Option 4: Speak to one of us
        staff_details = get_staff_details()
        send_sms(phone_number, "Staff contact details:\nName: {}\nPhone: {}".format(
            staff_details['name'], staff_details['phone']))

        response = "END The contact details of one of our staff has been sent to your phone."
    else:
        # Invalid input
        response = "END Invalid input. Please try again."

    return response
