from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Problem
from .forms import ProblemForm, ExcelUploadForm
import pandas as pd


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
    if request.method == 'POST' and 'file' in request.FILES:
        excel_form = ExcelUploadForm(request.POST, request.FILES)
        if excel_form.is_valid():
            excel_file = request.FILES['file']
            
            # read the excel using pandas
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Problem.objects.create(
                    title=row['title'],
                    link=row['link'],
                    platform=row['platform'],
                    difficulty=row['difficulty'],
                    # if you added 'user' field
                    user=request.user
                )
            return redirect('home')
    else:
        excel_form = ExcelUploadForm()
    
    form = ProblemForm()
    return render(request, 'problems/add_problems.html', {'form': form, 'excel_form': excel_form})



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