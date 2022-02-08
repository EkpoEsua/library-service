from django.db import models
from user.models import User
from django.utils import timezone


class Book(models.Model):
    BOOK_STATUS = [
        ("b", "Borrowed"),
        ("a", "Available"),
    ]
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=1, choices=BOOK_STATUS, default="a")
    publisher = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    due_back = models.DateField(null=True, blank=True)
    borrow_duration = models.IntegerField(
        help_text="Borrow duration in days.", null=True)
    borrower = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, to_field="email", related_name="borrowed_books")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.borrow_duration:
            self.due_back = timezone.now().date() + timezone.timedelta(days=self.borrow_duration)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ["id"]


