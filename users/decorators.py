from django.http import JsonResponse
from .models import Token


def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            token = Token.objects.get(key=token_key)
            if token.is_expired():
                token.delete()
                return JsonResponse({"error": "Token expired"}, status=401)

            request.user = token.user
        except Token.DoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)
    return wrapper
