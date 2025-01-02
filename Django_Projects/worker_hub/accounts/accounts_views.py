from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import logging

# Configure logger for error tracking
logger = logging.getLogger(__name__)
User = get_user_model()


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  
                user.save()
                email_sent = send_activation_email(request, user)
                if email_sent:
                    messages.success(request, "Account created successfully! Check your email to confirm your account.",'success')
                    return redirect('login')
                else:
                    messages.error(request, "Account not created, Because there was an error sending the activation email. Please contact support.", "danger")
                    user.delete()  
                    return redirect('register')
                
            except Exception as e:
                user.delete() 
                # Log unexpected exceptions
                logger.error(f"Unexpected error during registration: {str(e)}")
                messages.error(request, f"An unexpected error occurred. Please try again later. {str(e)}", "danger")
                return redirect('register')
        else:
            # If form is invalid, add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}", "danger")
                    break
                break
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/auth/register.html', {'form': form})





def send_activation_email(request, user):
    """Send account activation email and return True if successful."""
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        activation_link = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )
        email_subject = "Activate Your Worker Hub Account"
        message = f"Hi {user.username},\n\nThank you for registering at Worker Hub.\n\nPlease click the link below to activate your account:\n\n{activation_link}"
        send_mail(
            email_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        return True
    except Exception as e:
        logger.error(f"Error sending activation email to {user.email}: {str(e)}")
        return False



def activate_account(request, uidb64, token):
    """Handle account activation."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated! You can now log in.", "success")
            return redirect('login')
        else:
            messages.error(request, "Invalid or expired activation link.", "danger")
            return redirect('register')
    except get_user_model().DoesNotExist:
        logger.error("User not found during activation.")
        messages.error(request, "Invalid activation link.", "danger")
        return redirect('register')
    except Exception as e:
        logger.error(f"Error during account activation: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again later.", "danger")
        return redirect('register')


def activation_sent(request):
    """Render activation sent page."""
    return render(request, 'accounts/auth/activation_sent.html')


"""
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if a user with the given email exists
            user = User.objects.filter(email=email).first()
            if user:
                # Check if the password is correct
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('home')  # Replace 'home' with your desired success URL
                else:
                    messages.error(request, "Incorrect password. Please try again.", "danger")
            else:
                messages.error(request, "No account found with this email. Please register.", "danger")
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            messages.error(request, "An unexpected error occurred. Please try again later.", "danger")

    return render(request, 'accounts/auth/login.html')
"""

def custom_login(request):
    """Handle user login with error messages displayed under corresponding fields."""
    email_error = None
    password_error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.filter(email=email).first()
            if user:
                if authenticate(request, email=email, password=password):
                    login(request, user)
                    return redirect('home')  # Replace 'home' with your desired success URL
                else:
                    password_error = "Incorrect password. Please try again."
            else:
                email_error = "No account found with this email. Please register."
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            email_error = "An unexpected error occurred. Please try again later."

    return render(request, 'accounts/auth/login.html', {
        'email_error': email_error,
        'password_error': password_error,
    })