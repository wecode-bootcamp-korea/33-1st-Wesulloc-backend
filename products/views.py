from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count, F

from products.models  import Product


class ProductListView(View):
    def get(self, request):
        try:
            menu          = request.GET.get('menu', None)
            main_category = request.GET.get('main_category', None)
            category      = request.GET.get('category', None)
            search        = request.GET.get('search')
            sort          = request.GET.get('sort', 'new')
            limit         = int(request.GET.get('limit', 4))
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
                'high_price': '-price',
                'low_price' : 'price'
                }

            products = Product.objects.filter(q)\
                        .annotate(total_sales=Count('orderitem__id') * F('orderitem__quantity')\
                        , total_reviews=Count('review__id')).distinct()\
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