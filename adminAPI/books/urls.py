from django.urls import path
from books import views

urlpatterns = [
    # path("", views.BookListView.as_view(), name="book-list"),
    path("borrowed/", views.BorrowedBooksListView.as_view(), name="borrowed-books"),
    path("create/", views.BookCreateView.as_view(), name="create-book"),
    # path("<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    # path("<int:pk>/borrow/", views.BookUpdateView.as_view(), name="borrow-book"),
    path("<int:pk>/delete/", views.BookDeleteView.as_view(), name="delete-book"),
]
