from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Resume, WorkExperience, Education, AdditionalCourse, Language, ContactInfo
from django.forms import modelformset_factory
from .models import AdditionalCourse

# SignUpForm for user registration
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'placeholder': 'Enter your username',
            'class': 'form-control',  # Bootstrap class for consistent styling
        }),
        label='Username',
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Enter your password',
            'class': 'form-control',  # Bootstrap class for consistent styling
        }),
        label='Password',
        max_length=128,
        required=True,
    )

# EducationForm for adding education details
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'start_date', 'end_date', 'city']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# SkillsForm for adding skills in a resume
class SkillsForm(forms.Form):
    skills = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List your skills here...'}), label="Skills")

# ResumeForm for creating or editing a resume
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'email', 'phone', 'summary', 'address', 'skills', 'portfolio', 'resume_file', 'chosen_template']

    def save(self, commit=True):
        resume = super().save(commit=False)
        if commit:
            resume.save()
        return resume

# WorkExperienceForm for adding work experience
class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['employer', 'job_title', 'start_date', 'end_date', 'city']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Formsets for Education, Additional Courses, and Languages
EducationFormSet = modelformset_factory(
    Education, fields=['school', 'degree', 'start_date', 'end_date', 'city'], extra=1
)



# ContactInfoForm for handling contact information
class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'last_name', 'city', 'postal_code', 'phone_number', 'email']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email...'}),
        }
        

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language', 'proficiency_level']
        widgets = {
            'language': forms.TextInput(attrs={'placeholder': 'Enter a language'}),
            'proficiency_level': forms.Select(choices=[
                ('Beginner', 'Beginner'),
                ('Intermediate', 'Intermediate'),
                ('Advanced', 'Advanced'),
                ('Fluent', 'Fluent'),
            ]),
        }

# Define the FormSet for handling multiple language entries
LanguageFormSet = modelformset_factory(
    Language,
    form=LanguageForm,
    extra=1,  # Allows adding one extra form
)

class AdditionalCourseForm(forms.ModelForm):
    class Meta:
        model = AdditionalCourse
        fields = ['course_name', 'institution',]
        
class TemplateForm(forms.Form):
    template_choices = [
        ('template1', 'Template 1'),
        ('template2', 'Template 2'),
        ('template3', 'Template 3'),
        # Add more templates as needed
    ]
    chosen_template = forms.ChoiceField(choices=template_choices, widget=forms.RadioSelect)
    