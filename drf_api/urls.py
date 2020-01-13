from django.urls import path
from drf_api import views


urlpatterns = [
    
    path('user/signup/',views.Signup.as_view()), #link for signup class
    path('user/signin/',views.Signin.as_view()),  # link for signin class
    path('user/display/',views.Display.as_view()),
    path('user/update/',views.Update.as_view()),
    #path('/',views.user.as_view()),
    
]