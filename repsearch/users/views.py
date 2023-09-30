from django.shortcuts import render, redirect
from .models import Profile, Skill
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import search_profiles, paginate_profiles


# Create your views here.

# Все профили пользовател
def profiles(request):
    prof, search_query = search_profiles(request)
    custom_range, prof = paginate_profiles(request, prof, 3)
    context = {
        'profiles': prof,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/index.html', context)


# Профиль конкретного пользователя
def user_profile(request, pk):
    prof = Profile.objects.get(id=pk)

    top_skill = prof.skill_set.exclude(
        description__exact="")  # получаем доступ к классу Skill обращаемся к классу Skill "skill_set"
    # в нижнем регистре (т.к. таблицы в БД в нижнем регистре), и исключаем элементы если description пустой "exclude()"

    other_skills = prof.skill_set.filter(description="")  # берем элементы у которых дескрипшин пустой

    context = {
        'profile': prof,
        'top_skills': top_skill,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Username does not exist")
            # print("Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is incorrect")
            # print("Username or password is incorrect")

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "An error has occurred during registration")

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()
    repairs = prof.repair_set.all()

    context = {
        'profile': prof,
        'skills': skills,
        'repairs': repairs
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'users/delete.html', context)


@login_required(login_url='login')
def inbox(request):
    return render(request, 'users/inbox.html')
