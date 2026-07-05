from django.urls import path

from .views import RepositoryImportView

urlpatterns = [
    path(
        "import/",
        RepositoryImportView.as_view(),
        name="repository-import",
    ),
]