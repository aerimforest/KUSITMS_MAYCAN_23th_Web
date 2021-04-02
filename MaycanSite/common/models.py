from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=50) # 사용자 이름
    college = models.CharField(max_length=100) # 대학
    major = models.CharField(max_length=100) # 전공
    age = models.IntegerField() # 나이
    workHistory = models.TextField() # 이력 
    blog = models.URLField(blank=True) # 개인 블로그(선택 사항)
    kakaoName = models.CharField(max_length=50) # 카카오톡 프로필 이름
    kakaoTalk = models.FileField() # 카카오톡 대화 파일
    value0 = models.TextField(null=True, blank=True) # 참여성 비율
    value1 = models.TextField(null=True, blank=True) # 참여성 비율
    valueName = models.TextField(null=True, blank=True) # 성실성 비율
    contribution = models.FloatField(null=True, blank=True) # 최종 기여도
    standard = models.FloatField(null=True, blank=True) # 기준 점수
    cdate = models.DateTimeField(auto_now_add=True) # 게시물 생성 날짜