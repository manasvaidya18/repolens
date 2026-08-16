from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from apps.accounts.views import (
    CustomTokenObtainPairView,
)

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/repositories/",
        include("apps.repositories.urls"),
    ),

    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "api/analysis/",
        include("apps.analysis.urls"),
    ),

    path(
        "api/auth/",
        include("apps.accounts.urls"),
    ),
]