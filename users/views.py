import json, bcrypt

from django.http import JsonResponse
from django.views import View

from users.models import User, PetType
from users.utils import (validate_name,
                         validate_email,
                         validate_password,
                         validate_mobile_number)

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

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        User.objects.create(
                name               = name,
                email              = email,
                password           = hashed_password,
                mobile_number      = mobile_number,
                address            = address,
                email_subscription = email_subscription,
                membership_point   = 1000,
                pet_type           = pet_type,
        )
        
        return JsonResponse({"message": "SUCCESS"}, status=201)