from django import forms
from .models import Profile, WorkExperience, Education, Skill, Certification

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','profile_picture','birthday', 'headline', 'bio', 'location', 'contact_email', 'contact_phone', 'contact_website', 'github_url']

    
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Headline'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone'}),
            'contact_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub URL'}),
        }
        
        

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'role', 'start_date', 'end_date', 'description']
        
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job Description'}),
        }

    
    

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'field_of_study', 'start_year', 'end_year']
        
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter school name'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter degree'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter field of study'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Start year', 'min': 1900, 'max': 2100}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'End year', 'min': 1900, 'max': 2100}),
        }
        
    
    
    

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
        }

    


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter certification name'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter issuing organization'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        