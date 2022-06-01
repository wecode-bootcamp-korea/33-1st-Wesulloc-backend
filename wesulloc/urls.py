from django.urls import path, include

urlpatterns = [
    path("products", include("products.urls")),
    path("carts", include("carts.urls")),
    path("user", include("users.urls")),
    path("products", include("reviews.urls")),
]
