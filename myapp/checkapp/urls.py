from django.urls import path
from . import views
from .views import RegisterView, LoginView, JobListView, JobPostView, ApplyJobView,update_job
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('job/list/', JobListView.as_view(), name='job_list'),
    path('job/post/', JobPostView.as_view(), name='job_post'),
    path('job/<int:job_id>/apply/', ApplyJobView.as_view(), name='job_apply'),
    path('job/<int:job_id>/update/', views.update_job, name='job_update'),
    path('application/<int:application_id>/cancel/', views.cancel_application, name='cancel_application'),
    path('application/<int:application_id>/accept/', views.update_application_status, {'status': 'Accepted'}, name='accept_application'),
    path('application/<int:application_id>/reject/', views.update_application_status, {'status': 'Rejected'}, name='reject_application'),
    # path('password/reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
