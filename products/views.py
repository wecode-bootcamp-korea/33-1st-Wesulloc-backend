import json
from unicodedata import category
from django import views
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count, Sum

from products.models  import Product, MainCategory, Category, Menu

class CategoryView(View):
    def get(self, reqeust):
        category_list = [{
            'menu_id'      : menu.id,
            'menu_name'    : menu.name,
            'main_category': [{
                'main_category_id'  : main_category.id,
                'main_category_name': main_category.name,
                'category'          : [{
                    'category_id'  : category.id,
                    'category_name': category.name,
                } for category in Category.objects.filter(main_category=main_category.id)]
            } for main_category in MainCategory.objects.filter(menu_id=menu.id)]
        } for menu in Menu.objects.all()]

        return JsonResponse({"results" : category_list}, status=200)

class ProductListView(View):
    def get(self, request):
        menu          = request.GET.get('menu', None)
        main_category = request.GET.get('main_category', None)
        category      = request.GET.get('category', None)
        search        = request.GET.get('search')
        sort          = request.GET.get('sort', 'new')
        limit         = int(request.GET.get('limit', 12))
        offset        = int(request.GET.get('offset',0))

        q = Q()

        if menu:
            q &= Q(categoryproduct__category__main_category__menu__id = menu)

        if main_category:
            q &= Q(categoryproduct__category__main_category = main_category)

        if category:
            q &= Q(categoryproduct__category = category)

        if search:
            q &= Q(name__icontains = search)

        sort_type = {
            'reviews'   : '-total_reviews',
            'sales'     : '-total_sales',
            'new'       : '-id',
            'price_desc': '-price',
            'price_asc' : 'price'
            }

        products = Product.objects.filter(q).annotate(total_sales=Sum('orderitem__quantity', distinct=True))\
                    .annotate(total_reviews=Count('review__id', distinct=True))\
                    .order_by(sort_type.get(sort))[offset:offset+limit]
        
        products_list = [{
                "id"           : product.id,
                "name"         : product.name,
                "price"        : product.price,
                "discount_rate": product.discount_rate,
                "new"          : True if product in Product.objects.all().order_by('-id')[:2] else False,
                "sale_or_not"  : False if product.discount_rate == 0 else True,
                "img_url"      : [image.img_url for image in product.productimage_set.all()],
        } for product in products]

        return JsonResponse({'results': products_list}, status=200)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs["product_id"])

            product_detail = {
                    "id"           : product.id,
                    "img_url"      : [image.img_url for image in product.productimage_set.all()],
                    "name"         : product.name,
                    "price"        : product.price,
                    "discount_rate": product.discount_rate,
                    "new"          : True if product in Product.objects.all().order_by('-id')[:2] else False,
                    "sale_or_not"  : False if product.discount_rate == 0 else True,
                    "description"  : product.description,
                    "category"     : product.categoryproduct_set.filter().last().category.name,
                    "main_category": product.categoryproduct_set.filter().last().category.main_category.name,
            }

            return JsonResponse({'results' : product_detail}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 401)

class RecommendationView(View):
    def get(self, request):
        try:
            limit   = int(request.GET.get('limit', 4))
            offset  = int(request.GET.get('offset',0))
            recommendations = Product.objects.all().order_by("?")[offset:offset+limit]

            product_recommendation = [{
                    "id" : recommendation.id,
                    "img_url" : [image.img_url for image in recommendation.productimage_set.all()],
                    "name" : recommendation.name,
                    "price" : recommendation.price,
            } for recommendation in recommendations]
            
            return JsonResponse({'results' : product_recommendation}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 401)

# """장바구니 구현 관련 (CART 구현)"""
# """
# [ {
#     id: 1,
#     name: '영귤섬 아이스티',
#     packingState: '포장불가',
#     price: 13000,
#     amount: 1,
#   },
#   {
#     id: 2,
#     name: '러블리 티 박스',
#     packingState: '포장가능',
#     price: 20000,
#     amount: 1,
#   },
#   {
#     id: 3,
#     name: '그린티 랑드샤 세트',
#     packingState: '포장불가',
#     price: 36000,
#     amount: 1,
#   },
# ]
# """
# class CartView(View):
#     #@login_decorator
#     def get(self, request):
#         try:
#             # user = request.user
#             carts = Cart.objects.filter(user_id=1)

#             cart_list = [{
#                 # "user_id" : user.id,
#                 "cart_id" : cart.id,
#                 "product_id" : cart.product.id,
#                 "product_name" : cart.product.name,
#                 "product_img" : ProductImage.objects.get(id=cart.product.id).img_url,
#                 "price" : cart.product.price,
#                 "quantity" : cart.quantity,
#             } for cart in carts]

#             return JsonResponse({"cart_list" : cart_list}, status=200)
        
#         except KeyError:
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
#     # @login_decorator
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             # user = request.user
#             product_id = int(data['product_id'])
#             quantity = int(data['quantity'])

#             cart, created = Cart.objects.get_or_create(
#                 user_id = user.id,
#                 product_id = product_id,
#                 quantity = quantity
#             )
#             cart.save()
#             return JsonResponse({"message" : "SUCCESS"}, status=201)

#         except KeyError:
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)
#         except Cart.DoesNotExist:
#             return JsonResponse({"message" : "CART_DOES_NOT_EXIST"}, status=400)
            


#             return JsonResponse

#         except KeyError:
#             return JsonResponse

#     def patch(self, request):

#         return

#     def delete(self, request):

#         return