from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.houses_list, name='houses_list'),
    path('<int:house_id>', views.houses_detail, name='houses_detail'),
    path('<int:house_id>/delete/', views.houses_delete, name='houses_delete'),
    path('create/', views.houses_create, name='houses_create'),
    path('<int:house_id>/update/', views.house_update, name='house_update'),
    path('<int:house_id>/upload/', views.upload_image, name='upload_image'),
]
