import json

from django.http      import JsonResponse
from django.views     import View

from users.models     import User
from products.models  import ProductImage
from carts.models     import Cart

# """장바구니 구현 관련 (CART 구현)"""
# """
# [ {
#     id: 1,
#     name: '영귤섬 아이스티',
#     packingState: '포장불가',
#     price: 13000,
#     amount: 1,
#   },
# ]
# """
class CartView(View):
    #@login_decorator
    def get(self, request):
        try:
            # user = request.user
            carts = Cart.objects.filter(user_id=1) # 데코레이터 들어오면 수정해야함

            cart_list = [{
                # "user_id" : user.id,
                "cart_id" : cart.id,
                "product_id" : cart.product.id,
                "product_name" : cart.product.name,
                "product_img" : ProductImage.objects.get(id=cart.product.id).img_url,
                "price" : cart.product.price,
                "quantity" : cart.quantity,
            } for cart in carts]

            return JsonResponse({"results" : cart_list}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            # user = request.user
            # 데코레이터 들어오면 빼줘야함           
            product_id = int(data['product_id'])
            quantity = int(data['quantity'])

            cart, created = Cart.objects.get_or_create(
                user_id = User.objects.get(id=1).id, #데코레이터 들어오면 수정
                product_id = product_id,
                quantity = quantity
            )
            
            cart.save()

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status=400)
            
    def patch(self, request):
        try:
            data = json.loads(request.body)

            # user = request.user
            user = User.objects.get(id=1)
            cart_id = data['cart_id']
            product_id = data['product_id']
            quantity = data['quantity']
            cart = Cart.objects.get(id=cart_id, product_id=product_id, user_id=user.id)

            cart.quantity = quantity
            cart.save()

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status=404)
            
    def delete(self, request):
        try:
            # user = request.user
            user = User.objects.get(id=1)
            cart_id = request.GET.getlist('cart_id')

            cart = Cart.objects.get(id__in=cart_id, user_id=user.id)
            cart.delete()

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status=404)