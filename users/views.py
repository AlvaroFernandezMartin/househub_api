from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from users.decorators import auth_required
from .models import Token
import json
from django.contrib.auth.models import User


@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        if hasattr(user, 'token'):
            if user.token.is_expired():
                user.token.delete()
            else:
                token = user.token
        if not hasattr(user, 'token'):
            token = Token.objects.create(user=user)

        response = JsonResponse({"message": "Authenticated"})
        response.set_cookie(
            key="auth_token",
            value=str(token.key),
            httponly=True,
            max_age=24 * 60 * 60,  
            samesite='Lax',
            secure=False  
        )
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def logout_view(request):
    response = JsonResponse({"message": "Logged out"})
    response.delete_cookie("auth_token")
    return response



@auth_required
def current_user(request):
    user = request.user
    return JsonResponse({
        "id": request.user.id,
        "username": request.user.username,
        "is_superuser": request.user.is_superuser, 
    })

    
    
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created successfully"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=405)