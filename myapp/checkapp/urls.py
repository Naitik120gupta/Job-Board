# jobboard/urls.py

from django.urls import path
from .views import RegisterView, LoginView, JobListView, JobPostView, ApplyJobView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('job/list/', JobListView.as_view(), name='job_list'),
    path('job/post/', JobPostView.as_view(), name='job_post'),
    path('job/<int:job_id>/apply/', ApplyJobView.as_view(), name='job_apply'),
]
