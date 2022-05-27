
from django.urls import path 
from users.views import SignUpView, LogInView


urlpatterns = [
    # path("/users", UserView.as_view()),
    path("/signup", SignUpView.as_view()),
    path("/login", LogInView.as_view()),

]