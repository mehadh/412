from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

#my urls all in the app ok these are url
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/', ShowProfileSelfView.as_view(), name='show_profile_self'),
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]
