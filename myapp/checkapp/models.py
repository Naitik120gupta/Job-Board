from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    ACCOUNT_TYPES = [
        ('Job Seeker', 'Job Seeker'),
        ('Company', 'Company'),
        ('Admin', 'Admin'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='Job Seeker')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class JobPosting(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'account_type': 'Company'},related_name='job_postings')
    job_title = models.CharField(max_length=255,default="No title given")
    job_description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    application_deadline = models.DateField()
    status = models.CharField(max_length=10, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open')
    applicants = models.ManyToManyField(User, related_name='applied_jobs', blank=True, limit_choices_to={'account_type': 'Job Seeker'})

    def __str__(self):
        return self.title

class Application(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'account_type': 'Job Seeker'})
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    application_date = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    def __str__(self):
        return f"{self.job_seeker.email} - {self.job.title}"
