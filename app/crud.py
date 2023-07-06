"""Database Functions
"""
from app import db, CaseOfficer, SafeHouse, StaffDetails, FormSubmission


def get_case_officer_details():
    caseofficer = CaseOfficer.query.first()
    return caseofficer


def get_safe_house_location(text):
    safe_house_location = SafeHouse.query.filter_by(location=text).first()
    return safe_house_location


def get_staff_details():
    staff_details = StaffDetails.query.first()
    return staff_details


def save_ussd(phone):
    new_user = FormSubmission(phone=phone)
    db.session.add(new_user)
    db.session.commit()
