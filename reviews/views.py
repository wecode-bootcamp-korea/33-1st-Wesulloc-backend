import json

from django.http      import JsonResponse
from django.views     import View
from core.utils       import access_token_check

from products.models  import Product
from reviews.models   import Review
from django.db.models import Avg

class ReviewView(View):
    @access_token_check
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            rating  = data['rating']
            content = data['content']

            product = Product.objects.get(id = product_id)

            Review.objects.create(
                user_id    = user.id,
                product_id = product.id,
                content    = content,
                rating     = rating
            )
            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)

    def get(self, request, product_id):
        limit  = int(request.GET.get('limit', 5))
        offset = int(request.GET.get('offset',0))

        reviews = Review.objects.filter(product_id = product_id)

        total_reviews = reviews.count()
        average_rates = reviews.aggregate(avg_rating=Avg('rating'))

        review_list = [{
            "reviewId" : review.id,
            "productId": product_id,
            "account"  : review.user.account,
            "content"  : review.content,
            "rating"   : review.rating,
            "date"     : review.created_at,
        } for review in reviews[offset:offset+limit]]

        return JsonResponse({"totalReviews" : total_reviews, "averageRating": round(float(average_rates["avg_rating"]),1), "reviews" : review_list}, status=200)

    @access_token_check
    def delete(self, request, product_id, review_id):
        try:
            user = request.user.id
            Review.objects.get(id = review_id, user_id = user).delete()
            return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({"message" : "CONTENT_DOES_NOT_EXIST"}, status=404)