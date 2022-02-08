from django.urls import path
from user import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="list-users"),
    path("borrowed-books/", views.UsersandBorrowedBooksView.as_view(), name="users-and-borrowed-books"),
    path("register/", views.RegisterUserView.as_view(), name="register-user"),
]
