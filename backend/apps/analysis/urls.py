from django.urls import path

from .views import StartAnalysisView

urlpatterns = [
    path(
        "start/",
        StartAnalysisView.as_view(),
        name="start-analysis",
    ),
]