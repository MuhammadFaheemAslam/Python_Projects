from accounts.models import CustomUser
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50) 
    headline = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/blank-profile-picture.png')
    birthday = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True) 
    city = models.CharField(max_length=100, blank=True, null=True)  
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_website = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('he/him', 'He/Him'), ('she/her', 'She/Her'), ('they/them', 'They/Them')], default='he/him')
    current_position = models.CharField(max_length=255, null=True, blank=True) 


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('profile', 'company_name', 'role', 'start_date')
        


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField(blank=False, null=False)
    end_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('profile', 'school_name', 'degree', 'field_of_study')


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('profile', 'name')


class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField(blank=False)
    expiration_date = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = ('profile', 'name', 'issuing_organization', 'issue_date')
