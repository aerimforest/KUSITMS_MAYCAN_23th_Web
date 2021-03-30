from django.urls import path
from . import views

app_name = 'yomember'

urlpatterns = [
    path('', views.index, name='index'),
    path('searchMember', views.searchMember, name='searchMember'),
    path('team', views.team, name='team'),
    path('team/<int:question_id>/', views.detail, name='detail'),
    path('searchMember/<str:user_username>/', views.userInfo, name='userInfo'),
    path('team/create/', views.question_create, name='question_create'),
    path('team/comment/create/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('team/comment/modify/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('team/comment/delete/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
]