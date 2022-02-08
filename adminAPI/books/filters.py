from rest_framework import filters
from django.utils.translation import gettext_lazy as _


class PublisherFilter(filters.SearchFilter):
    search_param = "publisher"
    search_title = _("Publisher Filter")
    search_description = _(
        "Filter Books by publisher."
    )

    def get_search_fields(self, view, request):
        return ["publisher"]

class CategoryFilter(filters.SearchFilter):
    search_param = "category"
    search_title = _("Category Filter")
    search_description = _(
        "Filter Books by category."
    )

    def get_search_fields(self, view, request):
        return ["category"]