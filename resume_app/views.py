import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.middleware.csrf import get_token
from django.contrib.auth import login as auth_login
from weasyprint import HTML
from .forms import (
    SignUpForm, WorkExperienceForm, EducationForm,
    SkillsForm, ContactInfoForm, LanguageFormSet, AdditionalCourse 
)
from .models import (
    ContactInfo, WorkExperience, Education, Skills, Language, Resume
)


def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_app/resume_list.html', {'resumes': resumes})

# Setup logger
logger = logging.getLogger(__name__)

def handle_form(request, form_class, success_url, instance=None):
    form = form_class(request.POST or None, instance=instance)
    print("Form received:", form.is_valid())  # Debugging line to check form validity
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, f"{form_class.__name__[:-4]} saved successfully!")
        return redirect(success_url)
    else:
        print("Form errors:", form.errors)  # Debugging line to print form errors
    return form

# -------- Views --------

# My Account View
@login_required
def my_account(request):
    return render(request, 'my_account.html')

def index(request):
    login_form = AuthenticationForm(request, data=request.POST or None)
    signup_form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if 'login' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('resume_list')
            else:
                messages.error(request, "Invalid login credentials. Please try again.")

        elif 'signup' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.set_password(signup_form.cleaned_data['password1'])
                user.save()
                login(request, user)
                
                # Automatically create a Resume object for the new user
                Resume.objects.create(user=user, name=f"{user.first_name} {user.last_name}")
                ContactInfo.objects.create(user=user, email=user.email, first_name=user.first_name, last_name=user.last_name)
            
                messages.success(request, f"Sign-up successful! Welcome, {user.username}!")
                return redirect('next_steps')  # Redirect to the next steps page
            else:
                messages.error(request, "There was an error with your sign-up. Please correct the errors below.")
                print("Signup form errors:", signup_form.errors) # Ensure that `user` is not accessed here
            
            print("CSRF Cookie:", request.COOKIES.get("csrftoken"))
            print("CSRF Token in POST:", request.POST.get("csrfmiddlewaretoken"))

                
    return render(request, 'index.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })


# Logout
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('index')


@login_required
def resume_list(request):
    user = request.user

    if request.method == 'POST':
        # If "Create New Resume" is clicked, delete the existing resume
        Resume.objects.filter(user=user).delete()
        ContactInfo.objects.filter(user=user).delete()
        WorkExperience.objects.filter(user=user).delete()
        Education.objects.filter(user=user).delete()
        Skills.objects.filter(user=user).delete()
        AdditionalCourse.objects.filter(user=user).delete()
        Language.objects.filter(user=user).delete()

        # Create a new resume
        new_resume = Resume.objects.create(
            user=user,
            name=f"Resume for {user.first_name} {user.last_name}".strip() or f"Resume for User ({user.username})",
            email=user.email,
            phone="",
            summary="",
            address="",
            chosen_template="default"
        )
        return redirect('contact_info')  # Adjust to redirect to the first step of the form flow

    resumes = Resume.objects.filter(user=user)
    return render(request, 'resume_app/resume_list.html', {'resumes': resumes, 'user': user})


def preview_resume(request):
    # Retrieve the most recent resume or the previous resume
    try:
        resume = Resume.objects.filter(user=request.user).order_by('-created_at').first()
    except Resume.DoesNotExist:
        resume = None

    return render(request, 'preview_resume.html', {'resume': resume})

@login_required
def next_steps(request):
    return render(request, 'resume_app/next_steps.html')


def contact_info(request):
    # Create or fetch the ContactInfo object
    contact_info, created = ContactInfo.objects.get_or_create(user=request.user)
    
    # Instantiate the form
    form = ContactInfoForm(request.POST or None, instance=contact_info)

    if request.method == 'POST':
        if form.is_valid():
            # Save the form if it is valid
            form.save()
            # Redirect to the next page
            return redirect('work_experience')  # Replace with your actual URL name
        else:
            # Handle form errors if needed
            print(form.errors)  # You can log the errors for debugging

    return render(request, 'resume_app/contact_info.html', {'form': form})


@login_required
def work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.user = request.user  # Assign logged-in user to the form
            work_experience.save()
            return redirect('education')  # Redirect to education page after saving
    else:
        form = WorkExperienceForm()

    return render(request, 'resume_app/work_experience.html', {'form': form})


# Education (Step 3)
@login_required
def education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user  # Assign logged-in user to the education form
            education.save()
            return redirect('skills')  # After education, go to skills page
        else:
            print(form.errors)  # Print form errors if the form is invalid
    else:
        form = EducationForm()

    return render(request, 'resume_app/education.html', {'form': form})

@login_required
def skills(request):
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            skills_data = form.cleaned_data['skills']
            skills_instance = Skills(user=request.user, skill=skills_data)  # Use 'skill' instead of 'skills'
            skills_instance.save()
            return redirect('additional_courses')  # After skills, go to additional courses page
    else:
        form = SkillsForm()

    return render(request, 'resume_app/skills.html', {'form': form})

def additional_courses(request):
    if request.method == 'POST':
        course_names = request.POST.getlist('course_name[]')
        institutions = request.POST.getlist('institution[]')

        # Create AdditionalCourse instances without completion_date
        for course_name, institution in zip(course_names, institutions):
            AdditionalCourse.objects.create(
                user=request.user,
                course_name=course_name,
                institution=institution
            )
        
        return redirect('languages_known')  # Redirect to languages known page after saving the courses
    else:
        form = AdditionalCourse()

    return render(request, 'resume_app/additional_courses.html', {'form': form})




@login_required
def languages_known(request):
    user = request.user
    if request.method == 'POST':
        languages = request.POST.getlist('language[]')  # Get the list of languages
        proficiencies = request.POST.getlist('proficiency[]')  # Get the list of proficiency levels

        # Check if both lists have matching lengths
        if len(languages) == len(proficiencies):
            for language, proficiency in zip(languages, proficiencies):
                if language.strip():  # Only save if the language field is not empty
                    Language.objects.create(user=user, language=language, proficiency_level=proficiency)
            messages.success(request, "Languages added successfully!")
            return redirect('preview_resume')
        else:
            messages.error(request, "Languages and proficiency levels do not match.")

    return render(request, 'resume_app/languages_known.html')


         

@login_required
def preview_resume(request):
    user = request.user
    try:
        # Fetch the most recent resume or create a new one if none exists
        resume = Resume.objects.filter(user=user).order_by('-id').first()

        if not resume:
            messages.error(request, "No resume found. Please create a new resume.")
            return redirect('resume_list')

        contact_info = ContactInfo.objects.filter(user=user).first()
        work_experience = WorkExperience.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        skills = Skills.objects.filter(user=user)
        additional_courses = AdditionalCourse.objects.filter(user=user)
        languages_known = Language.objects.filter(user=user)

        context = {
            'resume': resume,
            'contact_info': contact_info,
            'work_experience': work_experience,
            'education': education,
            'skills': skills,
            'additional_courses': additional_courses,
            'languages_known': languages_known,
        }

        return render(request, 'resume_app/preview_resume.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('resume_list')


@login_required
def download_resume(request, resume_id):
    try:
        user = request.user
        resume = Resume.objects.get(id=resume_id, user=user)
        contact_info = ContactInfo.objects.get(user=user)
        work_experience = WorkExperience.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        skills = Skills.objects.filter(user=user)
        additional_courses = AdditionalCourse.objects.filter(user=user)
        languages_known = Language.objects.filter(user=user)

        context = {
            'resume': resume,
            'contact_info': contact_info,
            'work_experience': work_experience,
            'education': education,
            'skills': skills,
            'additional_courses': additional_courses,
            'languages_known': languages_known,
        }

        # Render the resume to a string using the preview_resume template
        html_content = render_to_string('resume_app/preview_resume.html', context)

        # Convert HTML to PDF using WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf()

        # Create a response to download the PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.name}_resume.pdf"'

        # Optionally log the user out after download (can be removed if you want the user to remain logged in)
        logout(request)

        return response

    except Resume.DoesNotExist:
        messages.error(request, "Resume not found. Please create a resume first.")
        return redirect('resume_list')  # Redirect to the resume list page if the resume doesn't exist


# Privacy Policy Page
def privacy_policy(request):
    return render(request, 'resume_app/privacy_policy.html')

# Terms and Conditions Page
def terms_conditions(request):
    return render(request, 'resume_app/terms_conditions.html')

# Accessibility Page
def accessibility(request):
    return render(request, 'resume_app/accessibility.html')

# Contact Us Page
def contact_us(request):
    return render(request, 'resume_app/contact_us.html')


def save_template_choice(request):
    if request.method == 'POST':
        selected_template = request.POST.get('template_id')  # Get the template ID from POST
        if selected_template:
            # Save template to session
            request.session['selected_template'] = selected_template
            messages.success(request, "Template saved successfully!")
        else:
            messages.error(request, "Failed to save the template.")
    return redirect('preview_resume')

@login_required
def choose_template(request):
    user = request.user
    work_experience = WorkExperience.objects.filter(user=user)
    education = Education.objects.filter(user=user)
    skills = Skills.objects.filter(user=user)
    additional_courses = AdditionalCourse.objects.filter(user=user)
    languages_known = Language.objects.filter(user=user)
    contact_info = ContactInfo.objects.get(user=user)

    if request.method == 'POST':
        selected_template = request.POST.get('template_choice')

        if selected_template:
            # Create or update the user's Resume
            resume, created = Resume.objects.get_or_create(user=user)
            resume.chosen_template = selected_template
            resume.name = f"{user.first_name} {user.last_name}"
            resume.email = user.email
            resume.phone = contact_info.phone_number
            resume.address = contact_info.address
            resume.skills = ", ".join([skill.skill for skill in skills])  # Join skills with commas
            resume.save()

            # Redirect to the preview page to show the resume with user's input
            return redirect('preview_resume')  # This should go to the preview page directly
        else:
            messages.error(request, "Please select a template to continue.")

    # Redirect to preview resume page if no template selection page is available
    return redirect('preview_resume')  # Redirect directly to the preview resume page



def some_view(request):
    # Debugging CSRF values
    print("CSRF Cookie:", request.COOKIES.get("csrftoken"))
    print("CSRF Token in POST:", request.POST.get("csrfmiddlewaretoken"))
    print("CSRF Token from get_token():", get_token(request))
    
    return HttpResponse("Check the console for CSRF token details.")