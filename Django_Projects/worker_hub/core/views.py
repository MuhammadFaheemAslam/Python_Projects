from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import Profile



def welcome(request):
    return render(request, 'core/welcome.html')


@login_required
def home(request):
    profile = get_object_or_404(Profile, user= request.user)
    
    context = {
        'profile': profile
    }
    
    return render(request, 'core/home.html', context)