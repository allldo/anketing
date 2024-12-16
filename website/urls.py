from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html'), name='default_login'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('moderator/general-info/', views.edit_general_info, name='edit_general_info'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('survey/<int:survey_id>/', views.view_survey, name='view_survey'),
    path('survey/', views.fill_survey, name='fill_survey'),
    path('edit_survey/', views.edit_survey, name='edit_survey'),
    path('edit_survey/<int:survey_id>/', views.edit_survey, name='edit_survey'),

]