from django.db import models
from django.contrib.auth.models import User  # Use the built-in User model

# Resume model
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField()
    address = models.TextField()
    skills = models.TextField()
    portfolio = models.URLField(blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    chosen_template = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# WorkExperience model
class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255)
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.degree} from {self.school}"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"

# AdditionalCourse model
class AdditionalCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)

     
    def __str__(self):
        return self.course_name

class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tied to the user
    language = models.CharField(max_length=255)  # The language name
    proficiency_level = models.CharField(
        max_length=50,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Fluent', 'Fluent'),
        ],
        default='Beginner'
    )

    def __str__(self):
        return f"{self.language} ({self.proficiency_level})"

class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)  # This should match the column in the DB
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Skills model
class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use the built-in User model
    skill = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ], default='Beginner')

    def __str__(self):
        return f"{self.skill} ({self.proficiency})"


class Template(models.Model):
    name = models.CharField(max_length=255)
    image_path = models.ImageField(upload_to='templates/images/')  # path to the image file

    def __str__(self):
        return self.name
    