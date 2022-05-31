import json

from django.http      import JsonResponse
from django.views     import View
from core.utils       import access_token_check

from users.models     import User
from carts.models     import Cart

class CartView(View):
    @access_token_check
    def get(self, request):
        user = request.user
        carts = Cart.objects.filter(user_id = user.id)
        cart_list = [{
            "user_id" : user.id,
            "cart_id" : cart.id,
            "product_id" : cart.product.id,
            "product_name" : cart.product.name,
            "product_img" : cart.product.productimage_set.first().img_url,
            "price" : cart.product.price,
            "quantity" : cart.quantity,
        } for cart in carts]
        return JsonResponse({"results" : cart_list}, status=200)
    
    @access_token_check
    def post(self, request):
        # POST /carts
        try:
            data = json.loads(request.body)
            user = request.user          
            product_id = int(data['product_id'])
            quantity = int(data['quantity'])

            cart, created = Cart.objects.get_or_create(
                user_id = user.id,
                product_id = product_id,
                defaults={"quantity" : quantity}
            )

            if not created:
                cart.quantity += quantity
                cart.save()

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    @access_token_check
    def patch(self, request, cart_id):
        # PATCH /carts/1
        try:
            data = json.loads(request.body)

            user = request.user
            cart_id = data['cart_id']
            quantity = data['quantity']

            cart = Cart.objects.get(id=cart_id, user_id=user.id)

            cart.quantity = quantity
            cart.save()

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status=404)
            
    def delete(self, request):
        # DELETE /carts?ids=[1,2,3]
        user = request.user
        user = User.objects.get(id=1)
        cart_ids = request.GET.getlist('cart_ids')

        Cart.objects.filter(id__in=cart_ids, user_id=user.id).delete()

        return JsonResponse({"message" : "SUCCESS"}, status=200)