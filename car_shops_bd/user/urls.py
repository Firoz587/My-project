from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update_profile/', views.update_profile, name='update_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),    
    path('profile/reset_password/', views.reset_password, name='reset_password'),
]