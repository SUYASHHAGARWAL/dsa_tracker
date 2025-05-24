from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Problem
from .forms import ProblemForm


@login_required
def home(request):
    problems = Problem.objects.filter(user=request.user)  # only user's problems

    # apply filters (difficulty, platform, status)
    difficulty = request.GET.get('difficulty')
    platform = request.GET.get('platform')
    status = request.GET.get('status')
    sort = request.GET.get('sort')

    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    if platform:
        problems = problems.filter(platform=platform)
    if status:
        problems = problems.filter(status=status)

    if sort:
        if sort == "difficulty":
            problems = problems.order_by('difficulty')
        elif sort == "platform":
            problems = problems.order_by('platform')
        elif sort == "status":
            problems = problems.order_by('status')

    return render(request, 'home.html', {'problems': problems})


@login_required
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user = request.user
            problem.save()
            return redirect('home')
    else:
        form = ProblemForm()
    return render(request, 'problems/add_problems.html', {'form': form})




@login_required
def toggle_status(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    if problem.user != request.user:
        return redirect('home')  # Prevent others from toggling your problems
    if problem.status == 'Unsolved':
        problem.status = 'Solved'
    else:
        problem.status = 'Unsolved'
    problem.save()
    return redirect('home')



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # DEBUG: print form errors to console
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    print("Rendering login page")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        print("Inside elsw")
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')