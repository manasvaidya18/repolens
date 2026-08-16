from django.urls import path

from .views import (
    StartAnalysisView,
    AnalysisDetailView,
)

urlpatterns = [
    path(
        "start/",
        StartAnalysisView.as_view(),
        name="start-analysis",
    ),

    path(
        "<int:job_id>/",
        AnalysisDetailView.as_view(),
        name="analysis-detail",
    ),
]