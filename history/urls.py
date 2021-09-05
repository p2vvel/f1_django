"""f1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from . import views


app_name="history"
urlpatterns = [
    path("", views.index, name="index"),
    path("driver/<slug:nick>", views.DriverView.as_view(), name="driver_details"),
    path("team/<slug:nick>", views.ConstructorView.as_view(), name="constructor_details"),
    path("circuit/<slug:nick>", views.CircuitView.as_view(), name="circuit_details"),
    #easier to find race by id rather than making slugs for every race
    path("race/<int:pk>", views.RaceView.as_view(), name="race_details"),
    path("season/<int:pk>", views.SeasonView.as_view(), name="season_details"),
    path("seasons/", views.SeasonsListView.as_view(), name="seasons_list"),
    path("drivers/", views.drivers_current, name="drivers_list"),
    re_path(r"drivers/alphabetical/(?P<letter>[a-zA-Z]{1})/", views.drivers_alphabetical, name="drivers_alphabetical"),
]