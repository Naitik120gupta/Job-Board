from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import JobPosting, Application  

User = get_user_model()

admin.site.register(User)
admin.site.register(JobPosting)
admin.site.register(Application)
