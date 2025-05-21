from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("login/", views.login_view),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.current_user, name='current_user'),
]
