from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, JobPosting, Application
from .serializers import UserSerializer, JobPostingSerializer, ApplicationSerializer
from .permissions import IsCompanyUser, IsJobSeekerUser
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from django.http import JsonResponse, HttpResponseForbidden
from .forms import JobUpdateForm
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def password_reset_confirm(request, token):
#     if request.method == 'POST':
#         try:
#             new_password = request.POST.get('new_password')
#             uidb64 = request.POST.get('uid')
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)
#             if default_token_generator.check_token(user, token):
#                 user.password = make_password(new_password)
#                 user.save()
#                 return JsonResponse({'message': 'Password reset successful'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid token'}, status=400)
#         except (User.DoesNotExist, ValidationError):
#             return JsonResponse({'error': 'Invalid UID or token'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@csrf_exempt
def update_job(request, job_id):
    if request.method == 'PUT':
        if request.user.account_type != 'Company':
            return HttpResponseForbidden("Only companies can update job postings.")
        job = get_object_or_404(JobPosting, id=job_id, company=request.user)
        import json
        data = json.loads(request.body)
        form = JobUpdateForm(data, instance=job)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Job posting updated successfully."}, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def cancel_application(request, application_id):
    if request.method == 'DELETE':
        if request.user.account_type != 'Job Seeker':
            return HttpResponseForbidden("You are not authorized to cancel this application.")
        application = get_object_or_404(Application, id=application_id, job_seeker=request.user)
        application.delete()
        return JsonResponse({"message": "Application cancelled successfully."}, status=200)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def update_application_status(request, application_id, status):
    if request.user.account_type != 'Company':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('job_list')
    application = get_object_or_404(Application, id=application_id)
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
        messages.success(request, f"Application has been marked as {status}.")
    else:
        messages.error(request, "Invalid status provided.")
    
    return redirect('job_list')  

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
