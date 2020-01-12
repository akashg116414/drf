from django.urls import path
from drf_api import views


urlpatterns = [
    #path('api_home/', views.home, name='blog-home'),
    path('user/signup/',views.Signup.as_view()), #link for signup class
    path('user/signin/',views.Signin.as_view()),  # link for signin class
    #path('/',views.user.as_view()),
    
]