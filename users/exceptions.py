from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        error_messages = []
        for field, messages in response.data.items():
            # Extract the first error message
            error_messages.append(f"{messages[0]}")

        response.data = {
            "status": "error",
            "message": error_messages[0] if error_messages else "Validation failed"
        }

    return response
