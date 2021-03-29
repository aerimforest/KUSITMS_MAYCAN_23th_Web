from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from common.views import *
from django.conf.urls.static import static
from django.conf import settings
app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sighup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)