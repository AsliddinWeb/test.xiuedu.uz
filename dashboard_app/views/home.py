from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout


# Home count models
from student_app.models import *
from quiz_app.models import *

# Change password
from django.contrib.auth import update_session_auth_hash
from ..forms.auth import CustomPasswordChangeForm, LoginForm

@login_required(login_url='login_page')
@user_passes_test(lambda u: u.is_staff)
def dashboard_home(request):
    grades = Grade.objects.all().count
    groups = Group.objects.all().count
    students = Student.objects.all().count

    subjects = Subject.objects.all().count
    quizs = Quiz.objects.all().count
    results = Result.objects.all().count

    ctx = {
        'grades': grades,
        'groups': groups,
        'students': students,

        'subjects': subjects,
        'quizs': quizs,
        'results': results
    }
    return render(request, 'dashboard/home.html', ctx)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)

                messages.success(request, 'Tizimga muvaffaqqiyatli kirdingiz!')
                return redirect('dashboard_home')

            else:
                messages.error(request, "Login yoki parol xato!")
        else:
            messages.error(request, "Ma'lumot kiritishda xatolik!")

    return render(request, 'dashboard/auth/login.html', context={'form': form})

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Ma\'lumot kiritishda xatolik!')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'dashboard/auth/change_password.html', {
        'form': form
    })


