from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from urllib.parse import urlencode
from django.urls import reverse
from .forms import ProfileForm, WorkExperienceForm, EducationForm, SkillForm, CertificationForm
from .models import Profile, WorkExperience, Education, Skill, Certification


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Initialize forms for adding new sections
    work_experience_form = WorkExperienceForm(request.POST or None)
    education_form = EducationForm(request.POST or None)
    skill_form = SkillForm(request.POST or None)
    certification_form = CertificationForm(request.POST or None)
    
    # Get the latest education, skills, and certifications
    latest_education = profile.educations.order_by('-end_year').first()
    skills = profile.skills.all()  
    certificates = profile.certifications.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        headline = request.POST.get('headline')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        profile.gender = request.POST.get("gender")
        location = f'{city}, {country}'

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.first_name = first_name
        profile.last_name = last_name
        profile.headline = headline
        profile.bio = bio
        profile.country = country
        profile.city = city
        profile.postal_code = postal_code
        profile.location = location
        profile.save()
    
        messages.success(request, 'Profile updated successfully.','success')

        return redirect('edit_profile')  # Redirect to the same page after saving

    # Gender choices for select input
    gender_choices = Profile._meta.get_field('gender').choices

    context = {
        'profile': profile,
        'gender_choices': gender_choices,
        'work_experience_form': work_experience_form,
        'education_form': education_form,
        'skill_form': skill_form,
        'certification_form': certification_form,
        'latest_education': latest_education,
        'skills': skills,
        'certificates': certificates,
    }

    return render(request, 'profiles/edit_profile.html', context)


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    work_experiences = profile.work_experiences.all().order_by('-start_date')
    educations = profile.educations.all().order_by('-start_year')
    skills = profile.skills.all()
    certifications = profile.certifications.all().order_by('-issue_date')

    context = {
        'profile': profile,
        'work_experiences': work_experiences,
        'educations': educations,
        'skills': skills,
        'certifications': certifications,
    }

    return render(request, 'profiles/view_profile.html', context)


##################################  working for experience  #################################################

@login_required
def add_work_experience(request):
    profile = get_object_or_404(Profile, user=request.user)
    next_url = request.GET.get('next', 'view_profile') 

    if request.method == 'POST':
        work_experience_form = WorkExperienceForm(request.POST)
        if work_experience_form.is_valid():
            try:
                work_experience = work_experience_form.save(commit=False)
                work_experience.profile = profile
                
                start_date = work_experience_form.cleaned_data['start_date']
                end_date = work_experience_form.cleaned_data['end_date']
                
                if end_date and start_date > end_date:
                    messages.error(request, 'Start date must be earlier than end date.', 'danger')
                    return redirect(f"{reverse('add_work_experience')}?{urlencode({'next': next_url})}")
                    
                else:
                    work_experience.save()
                    
                    if work_experience.end_date is None:
                        profile.current_position = f"{work_experience.role} at {work_experience.company_name}"
                        profile.save()
                        
                    messages.success(request, 'Work experience added successfully.','success')
                    return redirect(f"{reverse('add_work_experience')}?{urlencode({'next': next_url})}")
               
            except IntegrityError:
                messages.error(request, 'You have already added this work experience.', 'danger')
                return redirect(f"{reverse('add_work_experience')}?{urlencode({'next': next_url})}")

    else:
        work_experience_form = WorkExperienceForm()
        
        context = {
        'profile': profile,
        'form': work_experience_form,
        'next': next_url,
    }

    return render(request, 'profiles/experience/add_work_experience.html', context)

#edit all work experiences
@login_required
def edit_allwork_experience(request):
    profile = get_object_or_404(Profile, user=request.user)
    work_experience = profile.work_experiences.all().order_by('-start_date')
    
    context = {
        'profile': profile,
        'work_experiences': work_experience,
    }
  
    return render(request, 'profiles/experience/edit_allwork_experience.html', context)

# Edit Work Experience
@login_required
def edit_work_experience(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    work_experience = get_object_or_404(WorkExperience, pk=pk, profile__user=request.user)
    
    if request.method == 'POST':
        work_experience_form = WorkExperienceForm(request.POST, instance=work_experience)
        if work_experience_form.is_valid():
            start_date = work_experience_form.cleaned_data['start_date']
            end_date = work_experience_form.cleaned_data['end_date']
                    
            if end_date and start_date > end_date:
                messages.error(request, 'Start date must be earlier than end date.', 'danger')
                return redirect('edit_work_experience', pk=pk)
                
            else:                
                if work_experience.end_date is None:
                    profile.current_position = f"{work_experience.role} at {work_experience.company_name}"
                    profile.save()
                
                work_experience_form.save()
                messages.success(request, 'Work experience updated successfully.')
                return redirect('view_profile')
    else:
        work_experience_form = WorkExperienceForm(instance=work_experience)
    
    context = {
        'profile': profile,
        'form': work_experience_form
    }

    return render(request, 'profiles/experience/edit_work_experience.html', context)

# Delete Work Experience
@login_required
def delete_work_experience(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    work_experience = get_object_or_404(WorkExperience, pk=pk, profile__user=request.user)
    
    if request.method == 'POST':
        work_experience.delete()
        messages.success(request, 'Work experience deleted successfully.')
        return redirect('view_profile')

    context ={
        'url_path': 'edit_allwork_experience', 
        'type': 'Work Experience',
        'profile': profile
        }
    return render(request, 'profiles/delete_confirmation.html', context)


##########################################  working for education  ##########################################################
@login_required
def add_education(request):
    profile = get_object_or_404(Profile, user=request.user)
    next_url = request.GET.get('next', 'view_profile') 

    if request.method == 'POST':
        form = EducationForm(request.POST)
        try:
            if form.is_valid():
                education = form.save(commit=False)
                education.profile = profile
                start_year = form.cleaned_data['start_year']
                end_year = form.cleaned_data['end_year']
                if end_year and start_year > end_year:
                    messages.error(request, 'Start year must be earlier than end year.', 'danger')
                    return redirect(f"{reverse('add_education')}?{urlencode({'next': next_url})}")
                else:
                    education.save()
                    messages.success(request, 'Education added successfully.', 'success')
                    return redirect(f"{reverse('add_education')}?{urlencode({'next': next_url})}")
            
        except IntegrityError:
            messages.error(request, 'You have already added this work experience.', 'danger')
            return redirect(f"{reverse('add_education')}?{urlencode({'next': next_url})}")
            
    else:
        form = EducationForm()
        
        context = {
        'profile': profile,
        'form': form,
        'next': next_url,
    }
    return render(request, 'profiles/education/add_education.html', context)


@login_required
def edit_alleducation(request):
    profile = get_object_or_404(Profile, user=request.user)
    educations = profile.educations.all().order_by('-start_year')
    
    context = {
        'profile': profile,
        'educations': educations,
    }
    return render(request, 'profiles/education/edit_alleducation.html', context)

    
# Edit Education
def edit_education(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            start_year = form.cleaned_data['start_year']
            end_year = form.cleaned_data['end_year']
            if end_year and start_year > end_year:
                messages.error(request, 'Start year must be earlier than end year.', 'danger')
                return redirect('edit_education',pk=pk) 
            else:       
                form.save()
                messages.success(request, 'Education detail is updated successfully.')
                return redirect('edit_education',pk=pk) 
    else:
        form = EducationForm(instance=education)
        
    context = {
    'profile': profile,
    'form': form
    }

    return render(request, 'profiles/education/edit_education.html',  context)

# Delete Education
@login_required
def delete_education(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    education = get_object_or_404(Education, pk=pk, profile__user=request.user)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education deleted successfully.")
        return redirect('view_profile')
    
    context = {
        'profile': profile,
        'url_path': 'edit_alleducation', 
        'type': 'Education'
        }
    return render(request, 'profiles/delete_confirmation.html', context)



#####################################   kills working starts from here   ###############################################################
@login_required
def add_skill(request):
    profile = get_object_or_404(Profile, user=request.user)
    next_url = request.GET.get('next', 'view_profile') 

    if request.method == 'POST':
        skill_form = SkillForm(request.POST)
        if skill_form.is_valid():
            #check if the skill already exists for the current profile
            skill_name = skill_form.cleaned_data['name']
            existing_skill = profile.skills.filter(name=skill_name).first()
            
            if existing_skill:
                messages.error(request, 'You already have this skill.', 'danger')
                return render(request, 'profiles/skills/add_skill.html', {'form': skill_form})
            
            else:
                #if skill not exist save it
                skill = skill_form.save(commit=False)
                skill.profile = profile
                skill.save()
                messages.success(request, 'Skill added successfully.')
                
            # return redirect('edit_profile')
            return redirect(f"{reverse('add_skill')}?{urlencode({'next': next_url})}")
    else:
        skill_form = SkillForm()
        
        context = {
        'profile': profile,
        'form': skill_form,
        'next': next_url,
    }

    return render(request, 'profiles/skills/add_skill.html', context)

# Edit all skills

@login_required
def edit_allskills(request):
    profile = get_object_or_404(Profile, user=request.user)
    skill = profile.skills.all()
    
    context = {
        'profile': profile,
        'skill': skill
    }
    
    return render(request, 'profiles/skills/edit_allskills.html', context)

# Edit Skill
@login_required
def edit_skill(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
    if request.method == "POST":
        skill_name = request.POST.get('name')
        skill.name = skill_name
        skill.save()

        messages.success(request, "Skill updated successfully.")
        return redirect('view_profile')
    context = {
        'profile': profile,
        'skill': skill
    }
    
    return render(request, 'profiles/skills/edit_skill.html', context)

# Delete Skill
@login_required
def delete_skill(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully.")
        return redirect('view_profile')
    
    context = {
        'profile': profile,
        'object': skill,
        'type': 'Skill',
        'url_path': 'edit_allskills', 
    }

    return render(request, 'profiles/delete_confirmation.html', context)



#####################################Certification working start from here   ##############################
@login_required
def add_certification(request):
    profile = get_object_or_404(Profile, user=request.user)
    next_url = request.GET.get('next', 'view_profile') 

    if request.method == 'POST':
        certification_form = CertificationForm(request.POST)
        try:   
            if certification_form.is_valid():
                certification = certification_form.save(commit=False)
                certification.profile = profile
                
                issue_date = certification_form.cleaned_data['issue_date']
                expire_date = certification_form.cleaned_data['expiration_date']
                if issue_date > expire_date:
                        messages.error(request, 'Issue date must be earlier than Expira date.', 'danger')
                        return redirect(f"{reverse('add_certification')}?{urlencode({'next': next_url})}")
                else:
                    certification.save()
                    messages.success(request, 'Certification added successfully.','success')
                    return redirect(f"{reverse('add_certification')}?{urlencode({'next': next_url})}")
            
        except IntegrityError:
            messages.error(request, 'You have already added this course', 'danger')
            # return redirect('add_certification')
            return redirect(f"{reverse('add_certification')}?{urlencode({'next': next_url})}")

    else:
        certification_form = CertificationForm()
        context = {
        'profile': profile,
        'form': certification_form,
        'next': next_url,
        }

    return render(request, 'profiles/certificates/add_certification.html', context)

@login_required
def edit_allcertifications(request):
    profile = get_object_or_404(Profile, user=request.user)
    certifications = profile.certifications.all().order_by('-issue_date')
    
    context = {
        'profile': profile,
        'certifications': certifications
    }
    
    return render(request, 'profiles/certificates/edit_allcertifications.html', context)


# Edit Certification
@login_required
def edit_certification(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    certification = get_object_or_404(Certification, pk=pk, profile__user=request.user)
    
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            issue_date = form.cleaned_data['issue_date']
            expire_date = form.cleaned_data['expiration_date']
            
            if issue_date > expire_date:
                messages.error(request, 'Issue date must be earlier than Expira date.', 'danger')
                return redirect('edit_certification', pk=pk) 
            else:
                form.save()
                messages.success(request, "Certification updated successfully.")
                return redirect('view_profile')
    else:
        form = CertificationForm(instance=certification)
        
    context = {
        'profile': profile,
        'form': form
    }

    return render(request, 'profiles/certificates/edit_certification.html', context)

# Delete Certification
@login_required
def delete_certification(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    certification = get_object_or_404(Certification, pk=pk, profile__user=request.user)
    if request.method == "POST":
        certification.delete()
        messages.success(request, "Certification deleted successfully.")
        return redirect('view_profile')
    
    context = {
        'profile': profile,
        'object': certification,
        'type': 'Certification',
        'url_path': 'edit_allcertifications', 
    }

    return render(request, 'profiles/delete_confirmation.html', context)



######################################  contact info working starts from here     #################################
@login_required
def contact_info(request):
    profile_instance = get_object_or_404(Profile, user=request.user)

    context = {
        'profile': profile_instance
    }

    return render(request, 'profiles/contact_info.html', context)


@login_required
def edit_contact_info(request):
    # Get or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("contact_info")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
        
    context = {
        'profile': form
    }

    return render(request, "profiles/edit_contact_info.html", context)