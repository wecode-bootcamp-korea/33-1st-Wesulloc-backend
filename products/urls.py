from django.urls import path

from products.views import ProductDetailView, ProductListView, RecommendationView, CategoryView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/recommendation', RecommendationView.as_view()),
]