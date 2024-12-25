# app/utils/validators.py
import re
from email_validator import validate_email, EmailNotValidError

def validate_email_format(email):
    try:
        validation = validate_email(email, check_deliverability=False)
        return True, validation.email
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_format(phone):
    pattern = r'^\(5[0-9]{2}\) [0-9]{3} [0-9]{2} [0-9]{2}$'
    if not re.match(pattern, phone):
        return False, "Phone number must be in format: (5xx) xxx xx xx"
    return True, phone
