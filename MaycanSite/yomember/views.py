from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Comment, User
from .forms import QuestionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from common.models import Profile
from yomember import graph
# Create your views here.

def index(request):
    return render(request, 'yomember/competition_list.html')

def team(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'yomember/team.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'yomember/team_detail.html', context)

def userInfo(request, user_username):
    profile = Profile.objects.filter(name = user_username)
    # graph.start(profile)
    context = {'profile': profile}
    return render(request, 'yomember/userProfile.html', context)

def searchMember(request):

    kw = request.GET.get('kw', '')

    user_list = User.objects.all() # 등록된 모든 사용자의 리스트를 db의 User 테이블에서 가져옴

    if kw:
        user_list = user_list.filter(
            Q(username__icontains=kw)
        ).distinct()

    context = {'user_list': user_list, 'kw': kw}

    return render(request, 'yomember/searchMember.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('yomember:team')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'yomember/question_form.html', context)

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('yomember:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'yomember/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('yomember:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('yomember:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'yomember/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('yomember:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('yomember:detail', question_id=comment.question.id)
