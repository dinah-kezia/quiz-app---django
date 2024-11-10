from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, QuizForm
from .models import Subject, Question, Choice, Score
from django.contrib import messages
# Register view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = RegisterForm()

    return render(request, 'quiz/register.html', {'form': form})
    

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('subjects') 
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = AuthenticationForm()

    return render(request, 'quiz/login.html', {'form': form})

# Subjects page
@login_required
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'quiz/subjects.html', {'subjects': subjects})

@login_required
def quiz(request, subject_id):
    if request.method == 'POST':
        form = QuizForm(request.POST, subject_id=subject_id)
        if form.is_valid():
            score = 0
            for field, value in form.cleaned_data.items():
                choice = Choice.objects.get(id=value)
                if choice.is_correct:
                    score += 1
            # Save the score
            Score.objects.create(user=request.user, score=score)
            return redirect('score')
    else:
        form = QuizForm(subject_id=subject_id)
    return render(request, 'quiz/quiz.html', {'form': form})

# Score page
@login_required
def score(request):
    score = Score.objects.filter(user=request.user).last()
    return render(request, 'quiz/score.html', {'score': score})
