from django.urls import path
from . import views

urlpatterns = [
    # Homepage (Handles both login and signup)
    path('', views.homepage, name='homepage'),
    path('login/', views.homepage, name='login'),  # Redirects to the homepage for login

    # Logout
    path('logout/', views.logout, name='logout'),

    # My Account
    path('my-account/', views.my_account, name='my_account'),

    # Resume List
    path('resume-list/', views.resume_list, name='resume_list'),

    # Template Selection and Resume Flow
    path('choose-template/', views.choose_template, name='choose_template'),
    path('next-steps/', views.next_steps, name='next_steps'),
    path('save-template-choice/', views.save_template_choice, name='save_template_choice'),
    path('preview-resume/', views.preview_resume, name='preview_resume'),  # Corrected this URL path
    path('download-resume/<int:resume_id>/', views.download_resume, name='download_resume'),

    # Form Flow Steps
    path('contact-info/', views.contact_info, name='contact_info'),
    path('work-experience/', views.work_experience, name='work_experience'),
    path('education/', views.education, name='education'),
    path('skills/', views.skills, name='skills'),
    path('additional-courses/', views.additional_courses, name='additional_courses'),
    path('languages-known/', views.languages_known, name='languages_known'),

    # Static Information Pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
