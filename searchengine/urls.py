from django.urls import path 

from . import views

urlpatterns = [
               path('', views.searchResults),
               path('search', views.searchResults, name="search"),
               path('placeholder/', views.placeholder)
               ]