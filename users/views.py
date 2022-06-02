import json
import re
import bcrypt
import jwt

from django.views  import View
from django.http   import JsonResponse

from users.models  import User
from django.conf   import settings

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            account          = data['user_account']
            name             = data['user_name']
            email            = data['user_email']
            password         = data['user_password']
            contact          = data['user_contact']
            birth            = data['user_birth']
            terms_agreements = data['user_terms_agreements']

            REX_ACCOUNT  = '^^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{4,12}$'
            REX_PASSWORD = '^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,16}$'
            REX_BIRTH    = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'

            if User.objects.filter(account=account).exists():
                return JsonResponse({"Message": "ERROR_ACCOUNT_ALREADY_EXIST"}, status=400)

            if User.objects.filter(contact=contact).exists():
                return JsonResponse({"Message": "ERROR_CONTACT_ALREADY_EXIST"}, status=400)

            if not re.match(REX_ACCOUNT, account):
                return JsonResponse({"Message": "INVALID_ACCOUNT"}, status=400)

            if not re.match(REX_PASSWORD, password):
                return JsonResponse({"Message": "INVALID_PASSWORD"}, status=400)

            if not re.match(REX_BIRTH, birth):
                return JsonResponse({"Message": "INVALID_BIRTH"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                account          = account,
                name             = name,
                email            = email,
                password         = hashed_password,
                contact          = contact,
                birth            = birth,
                terms_agreements = terms_agreements
            )

            return JsonResponse({'Message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(account=data['user_account'])

            if not bcrypt.checkpw(data['user_password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({
                "message"      : "SUCCESS",
                "access_token" : access_token
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_ACCOUNT"}, status=404)
