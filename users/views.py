from django.views import View
from .models import User
from django.http import JsonResponse
from wesulloc.settings   import SECRET_KEY, ALGORITHM
import json, re, bcrypt, jwt



#http -v POST http://localhost:8000/users/signup user_name=최바다 user_email=choibaba@naver.com  user_password=1234qweq@@ user_account=1 user_address=주소 user_contact=1234 user_birth=1982-04-22 user_gender=남 user_terms_agreements={'1':'2'} 

class SignUpView(View):
    def post(self, request):
        try:

            data = json.loads(request.body)

            account          = data['user_account']
            name             = data['user_name']
            email            = data['user_email']
            password         = data['user_password']
            address          = data['user_address']
            contact          = data['user_contact']
            birth            = data['user_birth']
            gender           = data['user_gender']
            terms_agreements = data['user_terms_agreements']

            REX_ACCOUNT  = "^[a-z]+[a-z0-9]{5,19}$"
            REX_MAIL     = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            REX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
            REX_BIRTH    = "^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


            if User.objects.filter(email=email).exists():
                return JsonResponse({"Message": "ERROR_EMAIL_ALREADY_EXIST"}, status=400)

            if not re.match(REX_ACCOUNT, account):
                return JsonResponse({"Message": "INVALID_ACCOUNT"}, status=400)
               
            if not re.match(REX_MAIL, email):
                return JsonResponse({"Message": "INVALID_MAIL"}, status=400)

            if not re.match(REX_PASSWORD, password):
                return JsonResponse({"Message": "INVALID_PASSWORD"}, status=400)

            if not re.match(REX_BIRTH, birth):
                return JsonResponse({"Message": "INVALID_BIRTH"}, status=400)

            User.objects.create(
       
                account          = account,
                name             = name,
                email            = email,
                password         = hashed_password,
                address          = address,
                contact          = contact,
                birth            = birth,
                gender           = gender,
                terms_agreements = terms_agreements
            )

            return JsonResponse({'Message': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)



class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(email=data['user_email'])

            if not bcrypt.checkpw(data['user_password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({
                 "message"      : "SUCCESS",
                 "access_token" : access_token
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=401)

#http -v POST http://localhost:8000/users/login user_email=choibaba@naver.com  user_password=1234qweq@@
