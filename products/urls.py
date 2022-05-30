from django.urls import path
from products.views import ProductListView, CategoryView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/list', ProductListView.as_view()),
]