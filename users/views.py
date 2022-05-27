import json
from datetime import datetime, timedelta

import bcrypt
import jwt
from django.http    import JsonResponse
from django.views   import View
from django.conf    import settings

from users.models   import User, PetType
from users.utils    import (
    validate_name,
    validate_email,
    validate_password,
    validate_mobile_number,
    login_decorator,
)

class SignUpView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            name               = data["name"]
            email              = data["email"]
            password           = data["password"]
            mobile_number      = data["mobile_number"]
            address            = data["address"]
            email_subscription = data["email_subscription"]
            pet_type           = PetType.objects.get(id=data['pet_type'])

            validate_name(name)
            validate_email(email)
            validate_password(password)
            validate_mobile_number(mobile_number)

            signup_point = 1000
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name               = name,
                email              = email,
                password           = hashed_password,
                mobile_number      = mobile_number,
                address            = address,
                email_subscription = email_subscription,
                membership_point   = signup_point,
                pet_type           = pet_type,
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            user     = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            exp_days     = 1
            payload      = {'id': user.id, 'exp': datetime.utcnow() + timedelta(days = exp_days)}
            access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            return JsonResponse({"message": "SUCCESS", "ACCESS_TOKEN": access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)