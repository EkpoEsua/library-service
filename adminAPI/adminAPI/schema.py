from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title="Library Admin API.",
    description="Perform admin roles against the library service.",
    version="v1.0.0",
)
