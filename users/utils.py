import re
from datetime import datetime

import jwt
from django.http            import JsonResponse
from django.conf            import settings
from django.core.exceptions import ValidationError

from users.models import User

def validate_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(REGEX_EMAIL, email):
        raise ValidationError("INVALID_EMAIL")

def validate_password(password):
    REGEX_PASSWORD  = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,16}$"

    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("INVALID_PASSWORD")

def validate_mobile_number(mobile_number):
    REGEX_MOBILE = "^\d{10,11}$"
    
    if not re.match(REGEX_MOBILE, mobile_number):
        raise ValidationError("INVALID_MOBILE_NUMBER")

def validate_name(name):
    REGEX_NAME = r"^[가-힣]{1,}$"

    if not re.match(REGEX_NAME, name):
        raise ValidationError("INVALID_NAME_FORMAT")

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
            
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 400)

    return wrapper