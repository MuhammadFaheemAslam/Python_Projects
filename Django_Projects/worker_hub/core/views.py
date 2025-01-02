from django.shortcuts import render
from django.contrib.auth.decorators import login_required




def welcome(request):
    return render(request, 'core/welcome.html')


@login_required
def home(request):

    return render(request, 'core/home.html')