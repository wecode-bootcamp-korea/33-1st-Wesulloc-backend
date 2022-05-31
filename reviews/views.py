import json

from django.http      import JsonResponse
from django.views     import View
from core.utils       import access_token_check

from users.models     import User
from products.models import Product
from reviews.models     import Review


class ReviewView(View):
    @access_token_check
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            product_id = data['product_id']
            rating = data['rating']
            content = data['content']

            product = Product.objects.get(id = product_id)

            Review.objects.create(
                user_id = user.id,
                product_id = product_id,
                content = content,
                rating = rating
            )
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)

    # def get(self, request, product_id):
