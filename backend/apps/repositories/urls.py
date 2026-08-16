from django.urls import path

from .views import RepositoryImportView
from .views import RepositoryListView


urlpatterns = [
    path(
        "import/",
        RepositoryImportView.as_view(),
        name="repository-import",
    ),
    path(
    "",
    RepositoryListView.as_view(),
    name="repository-list",
    ),
]