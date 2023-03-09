from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('search', views.get_docs),
    path('complete-query', views.complete)
]
