from django.test import TestCase

# Create your tests here.
# def send_activation_email(request, user):
#     """Send account activation email and return True if successful."""
#     try:
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         domain = get_current_site(request).domain
#         activation_link = f'http://{domain}/accounts/authentication/activate/{uid}/{token}/'
#         email_subject = "Activate Your Worker Hub Account"
#         message = f"Hi {user.username},\n\nThank you for registering at Worker Hub.\n\nPlease click the link below to activate your account:\n\n{activation_link}"
#         send_mail(
#             email_subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email]
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Error sending activation email to {user.email}: {str(e)}")
#         return False
