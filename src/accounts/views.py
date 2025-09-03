from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from quiz.models import ExamAttempt

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil automáticamente
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully!')
            login(request, user)
            return redirect('exam_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    recent_attempts = ExamAttempt.objects.filter(user=request.user)[:5]
    
    context = {
        'profile': profile,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})