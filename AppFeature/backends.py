from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either 
    their email or username, with case insensitivity.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            username = username.strip().lower()  # Convert to lowercase

        try:
            # Identify if input is an email or username
            user = User.objects.get(email__iexact=username) if "@" in username else User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None

        # Validate password
        if user.check_password(password):
            return user
        return None
