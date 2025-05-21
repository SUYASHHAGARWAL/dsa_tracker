from django.shortcuts import render
from .models import Problem

def home(request):
    problems = Problem.objects.all()
    return render(request, 'problems/home.html', {'problems': problems})
