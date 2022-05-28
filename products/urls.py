from django.urls import path
from products.views import ProductDetailView, ProductListView

urlpatterns = [
    path('/list', ProductListView.as_view()),
    path('/teashop/<int:product_id>', ProductDetailView.as_view())
]