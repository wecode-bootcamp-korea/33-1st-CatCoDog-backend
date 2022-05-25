import re

from django.core.exceptions import ValidationError

def validate_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(REGEX_EMAIL, email):
        raise ValidationError("INVALID_EMAIL")

def validate_password(password):
    REGEX_PASSWORD  = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("INVALID_PASSWORD")

def validate_mobile_number(mobile_number):
    REGEX_MOBILE = "\d{3}-\d{3,4}-\d{4}"
    
    if not re.match(REGEX_MOBILE, mobile_number):
        raise ValidationError("INVALID_MOBILE_NUMBER")

def validate_name(name):
    REGEX_NAME = r"^[가-힣]{1,}$"

    if not re.match(REGEX_NAME, name):
        raise ValidationError("INVALID NAME FORMAT")