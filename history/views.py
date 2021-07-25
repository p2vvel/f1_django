from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Drivers

class DriverView(generic.DetailView):
    model = Drivers
    context_object_name = "driver"
    template_name = "driver.html"