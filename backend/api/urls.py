from django.urls import path
from .views import HealthStatusView, ImageApiQueryUploadView, ServeThumbnailView

urlpatterns = [
    path('health/status', HealthStatusView.as_view()),
    path('images/analyze-image', ImageApiQueryUploadView.as_view()),
    path('thumbnails/<str:filename>/', ServeThumbnailView.as_view(), name='thumbnail-serve'),
]
