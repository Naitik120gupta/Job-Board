from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, JobPosting, Application
from .serializers import UserSerializer, JobPostingSerializer, ApplicationSerializer
from .permissions import IsCompanyUser, IsJobSeekerUser

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class JobListView(generics.ListAPIView):
    queryset = JobPosting.objects.filter(status='Open')
    serializer_class = JobPostingSerializer
    permission_classes = (AllowAny,)

class JobPostView(generics.CreateAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = (IsAuthenticated, IsCompanyUser)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

class ApplyJobView(APIView):
    permission_classes = (IsAuthenticated, IsJobSeekerUser) 

    def post(self, request, job_id):
        job = JobPosting.objects.get(id=job_id)
        application = Application(job_seeker=request.user, job=job)
        application.save()
        return Response({"message": "Application submitted successfully"})
