from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    age = models.IntegerField()
    workHistory = models.TextField()
    blog = models.URLField(blank=True) # 선택 사항
    kakaoTalk = models.FileField()
    cdate = models.DateTimeField(auto_now_add=True) # 게시물 생성 날짜