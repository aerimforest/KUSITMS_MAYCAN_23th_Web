from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from common.models import Profile

# test
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=['name', 'college', 'major', 'age', 'workHistory', 'blog', 'kakaoName', 'kakaoTalk', 'value0', 'value1', 'valueName', 'contribution', 'standard']