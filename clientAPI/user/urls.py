import imp
from django.urls import path
from user import views

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register-user"),
    path("", views.UserListView.as_view(), name="list-user"),
]
