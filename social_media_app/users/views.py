from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
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

def home(request):
    return render(request, 'users/home.html')
