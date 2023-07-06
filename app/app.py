import os
from flask import Flask, request, Response, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv.main import load_dotenv
from ussd import handle_ussd_callback
import africastalking


# Initialize Africa's Talking API
load_dotenv()
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
africastalking.initialize(username, api_key)


sms = africastalking.SMS
airtime = africastalking.Airtime


# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
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


@app.route('/php-form-handler', methods=['POST'])
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

    return render_template('index.html')


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

# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


def main():
    if __name__ == "__main__":
        app.run(debug=True, port=os.environ.get("PORT"))


main()
