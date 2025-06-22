from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Missing token
        if isinstance(exc, NotAuthenticated):
            response.data = {
                "error": "Authentication credentials were not provided."
            }
        # Invalid token
        elif isinstance(exc, (AuthenticationFailed, InvalidToken, TokenError)):
            response.data = {
                "error": "Invalid or expired token."
            }
    return response 