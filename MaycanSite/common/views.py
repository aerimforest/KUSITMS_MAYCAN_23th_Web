from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm, ProfileForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('common:profile') # 회원가입 후 프로필 등록 페이지로 이동
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        profileForm = ProfileForm(request.POST, request.FILES)
        if profileForm.is_valid():
            profileForm = profileForm.save(commit=False)
            profileForm.save()
            return redirect('index')
    else:
        profileForm = ProfileForm()
    
    return render(request, 'common/profile.html', {'profileForm': profileForm})
