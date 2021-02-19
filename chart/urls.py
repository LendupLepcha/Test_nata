from django.urls import path
from . import views
app_name = 'chart'

urlpatterns = [
    path('create/', views.view_create, name = 'create'),
    path('show/', views.view_show, name = 'show'),
]