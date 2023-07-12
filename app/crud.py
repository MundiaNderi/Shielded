"""Database Functions
"""
from app import db, CaseOfficer, SafeHouse, StaffDetails, FormSubmission

# Fetches the first record in case_officer table
def get_case_officer_details():
    caseofficer = CaseOfficer.query.first()
    return caseofficer

# Fetches the first record in safe_house table
def get_safe_house_location(text):
    safe_house_location = SafeHouse.query.filter_by(location=text).first()
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
