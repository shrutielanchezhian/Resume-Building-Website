from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    summary = models.TextField(blank=True, null=True)  # Optional
    address = models.CharField(max_length=255, blank=True, null=True)  # Optional
    work_experience = models.TextField(blank=True, null=True)  # Optional
    education = models.TextField(blank=True, null=True)  # Optional
    skills = models.TextField(blank=True, null=True)  # Optional
    portfolio = models.URLField(blank=True, null=True)  # Optional
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.job_title} at {self.employer}"