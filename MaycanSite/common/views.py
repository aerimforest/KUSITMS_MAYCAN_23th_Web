from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm, ProfileForm
from common import lstm_model, total
import sqlite3
from os.path import basename # 파일명 추출
from pathlib import Path
import os

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
            print("카카오톡: "+str(profileForm.name))
            filename, fileExtension = os.path.splitext(profileForm.kakaoTalk)
            print("파일명: "+ str(filename))
            profileForm = profileForm.save(commit=False)
            profileForm.save()
            # 사용자가 올린 txt 파일 csv로 변환 -> filename}.csv 생성
            total.create_csv(filename)

            # 변환된 csv 파일로 predict -> filename}_result.csv 생성
            lstm_model.predict(filename) 

            # predict 결과 db 저장
            total.init(profileForm.kakaoTalk)
            profileForm.value0 = total.get_result(0)
            profileForm.value1 = total.get_result(1)
            profileForm.valueName = total.get_result('name') # name 자리에 뭐가 들어가야 함?

            return redirect('index')
    else:
        profileForm = ProfileForm()
    
    return render(request, 'common/profile.html', {'profileForm': profileForm})
