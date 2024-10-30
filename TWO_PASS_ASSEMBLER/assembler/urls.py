from django.urls import path
from . import views

urlpatterns = [
    path('', views.assembler_view, name='assembler_view'),
]
