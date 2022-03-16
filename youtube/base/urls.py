from django.urls import path
from .views import home, search

urlpatterns = [
    path('', home),
    path('search/', search),
]