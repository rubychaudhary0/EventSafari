
from django.shortcuts import render, redirect



# Create your views here.

#the landing page
def home(request):
    return render(request, 'home.html')

