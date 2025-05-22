from django.shortcuts import render, redirect
from .models import Problem
from .forms import ProblemForm

def home(request):
    problems = Problem.objects.all()

    difficulty = request.GET.get('difficulty')
    platform = request.GET.get('platform')

    print("Difficulty Filter:", difficulty)
    print("Platform Filter:", platform)

    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    if platform:
        problems = problems.filter(platform=platform)

    return render(request, 'problems/home.html', {'problems': problems})


def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProblemForm()
    return render(request, 'problems/add_problems.html', {'form': form})
