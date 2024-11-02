from rest_framework import serializers
from .models import User, JobPosting, Application
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'account_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'company', 'title', 'description', 'location', 'salary', 'application_deadline', 'status', 'applicants']
        read_only_fields = ['company', 'applicants']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job_seeker', 'job', 'application_date', 'status']
        read_only_fields = ['job_seeker', 'application_date']

    def validate(self, data):
        job = data.get('job')
        if job.status != 'Open':
            raise serializers.ValidationError("Cannot apply to a closed job posting.")
        return data
