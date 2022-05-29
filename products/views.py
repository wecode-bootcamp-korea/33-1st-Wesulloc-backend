from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count, F, Sum

from products.models  import Product

class ProductListView(View):
    def get(self, request):
        try:
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
                    "img_url"      : [image.img_url for image in product.productimage_set.all()]
            } for product in products]

            return JsonResponse({'results': products_list}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 401)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        try:
            limit   = int(request.GET.get('limit', 4))
            offset  = int(request.GET.get('offset',0))
            recommendations = Product.objects.all().order_by("?")[offset:offset+limit]
            products = Product.objects.filter(id=kwargs["product_id"])

            product_detail = [{
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
            } for product in products]

            product_recommendation = [{
                    "id" : recommendation.id,
                    "img_url" : [image.img_url for image in recommendation.productimage_set.all()],
                    "name" : recommendation.name,
                    "price" : recommendation.price,
            } for recommendation in recommendations]
            
            return JsonResponse({'recommendation': product_recommendation, 'deatils' : product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 401)
