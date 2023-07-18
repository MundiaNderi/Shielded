import os
from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv.main import load_dotenv
import africastalking
import requests
from requests.auth import HTTPBasicAuth
# from crud import get_case_officer_details, save_ussd, get_safe_house_location, get_staff_details
from airtime import top_up_airtime
from send_sms import sms


# Initialize Africa's Talking API
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)


airtime = africastalking.Airtime


# Initialize daraja  API
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mvrqdpje:U4fsMj4doJ3COF-BEFAU9FG9VpCEKdvd@tyke.db.elephantsql.com/mvrqdpje'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# database tables


class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(100))
    message = db.Column(db.Text)
    phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<FormSubnission {self.name}>'


class CaseOfficer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<CaseOfficer {self.firstname}>'


class SafeHouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    housename = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    managerfirstname = db.Column(db.String(80), nullable=False)
    managerlastname = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<SafeHouse {self.housename}>'


class StaffDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer)

    def __repr__(self):
        return f'<StaffDetails {self.firstname}>'


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    mpesanumber = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Donation {self.name}>'

# Fetches the first record in case_officer table


def get_case_officer_details():
    caseofficer = CaseOfficer.query.first()
    return caseofficer

# Fetches the first record in safe_house table


def get_safe_house_location(text):
    safe_house_location = SafeHouse.query.filter_by(id=text).first()
    return safe_house_location

# Fetches the first record in staff_details table


def get_staff_details():
    staff_details = StaffDetails.query.first()
    return staff_details

# Saves ussd data in the database


def save_ussd(phone):
    new_user = FormSubmission(phone=phone)
    db.session.add(new_user)
    db.session.commit()


# Create Routes


"""@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    return handle_ussd_callback(session_id, service_code, phone_number, text, sms, airtime)"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')

# Create route for the donate page


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        mpesa = request.form.get('mpesa')

        # Save the donation to the database
        donation = Donation(name=name, amount=amount, mpesa=mpesa)
        db.session.add(donation)
        db.session.commit()

        return "Thank you for your donation, {}! We received {} KES.".format(name, amount)

    return render_template('donate.html')


"""@app.route('/php-form-handler', methods=['POST'])
def php_form_handler():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # save form to the database
    form_submission = FormSubmission(
        name=name, email=email, subject=subject, message=message)
    db.session.add(form_submission)
    db.session.commit()

    return render_template('index.html')"""


"""Create incoming messages route"""


@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f'Incoming message...\n {data}')
    return Response(status=200)


"""create delivery reports route"""


@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    print(f'Delivery report response....\n {data}')
    return Response(status=200)


"""Safaricom daraja API routes"""
# access token


def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data = (requests.get(mpesa_auth_url, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))).json()
    return data['access_token']


@app.route('/access_token')
def token():
    data = ac_token()
    return data


# ussd route
@app.route('/', methods=['POST'])
def handle_ussd_callback():
    global response
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)
    print("dial", text)
    if text == "":
        # Initial USSD request
        response = "CON Welcome to Shielded! How may we help you today?\n"
        response += "1. Talk to a case officer\n"
        response += "2. Access a Safe house\n"
        response += "3. Request airtime\n"
        response += "4. Speak to one of us"
    elif text == "1":
        # Option 1: Talk to a case officer
        case_officer_details = get_case_officer_details()
        name = case_officer_details.lastname
        contact = case_officer_details.phone
        message = (
            "Case officer details: \nName: {}\nContact: {}".format(name, contact))
        sms.send(phone_number, message)

        response = "END We will send an SMS with the case officer's contact information shortly.Feel free to reach out to them. Thank you."
        # save_ussd(phone_number)

    elif text == "2":
        # Option 2: Access a Safe house
        response = "CON Select a safe house location closest to you:\n"
        response += "1. Moyale\n"
        response += "2. Narok\n"
        response += "3. Isiolo"

    elif text.startswith("2*"):
        locationid = text.split("*")[1]

        # User has selected a safe house location
        safe_house_location = get_safe_house_location(locationid)
        print(phone_number)
        print(safe_house_location)
        print(type(safe_house_location))
        location = safe_house_location.location
        manager = safe_house_location.managerfirstname
        contact = safe_house_location.phone
        name = safe_house_location.housename
        print(name)

        message = ("Safe house location: \nName: {}\nLocation: {}\nManager: {}\nContact: {}".format(
            name, location, manager, contact))

        sms.send(phone_number, message)

        response = "END Details of the safe house location" + \
            locationid + "nearest to you has been sent to your phone."
        # save_ussd(phone_number)

    elif text == "3":
        # Option 3: Request airtime
        amount = '5'
        currency_code = 'KES'
        top_up_airtime(phone_number, amount, currency_code)
        sms.send(phone_number, "Your account has been topped up with airtime.")

        response = "END Your account has been topped up with airtime."
        # save_ussd(phone_number)

    elif text == "4":
        # Option 4: Speak to one of us

        staff_details = get_staff_details()
        name = staff_details.firstname
        phone = staff_details.phone
        message = ("Staff details:\nName: {}\nPhone: {}".format(name, phone))

        sms.send(phone_number, message)

        # sms.send(phone_number, "Staff contact details:\nName: {}\nPhone: {}".format(
        # staff_details['name'], staff_details['phone']))

        response = "END The contact details of one of our staff has been sent to your phone."

        # save_ussd(phone_number)

    else:
        # Invalid input
        response = "END Invalid input. Please try again."

    return response


# Invalid URL

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=os.environ.get("PORT"))
