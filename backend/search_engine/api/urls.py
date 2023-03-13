from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search),
    path('search/suggestions', views.get_suggestions)
]
