import os
from flask import Flask, request, Response
import africastalking
from ussd import handle_ussd_callback
from models import Donation

# Initialize Africa's Talking API
username = os.environ['USERNAME']
api_key = os.environ['API_KEY']
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

# Create a form class
class FormSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    message = db.Column(db.Text)

@app.route('/php-form-handler', methods=['POST'])
def php_form_handler():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    #save form to the database
    form_submission = FormSubmission(name=name, email=email, subject=subject, message=message)
    db.session.add(form_submission)
    db.session.commit()

    return 'Form submitted successfully'


@app.route('/incoming-messages', methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f'Incoming message...\n {data}')
    return Response(status=200)


@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    data = request.get_json(force=True)
    print(f'Delivery report response....\n {data}')
    return Response(status=200)

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT"))
