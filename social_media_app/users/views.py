from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import User, Follow
import os

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            if request.FILES.get('profile_picture'):
                uploaded_file = request.FILES['profile_picture']
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                request.user.profile.profile_picture = fs.url(filename)
                request.user.profile.save()

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    context = {
        'user': user,
        'is_following': is_following,
    }
    return render(request, 'users/user_profile.html', context)

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('user_profile', username=username)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('user_profile', username=username)
