from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
from drf_api.models import Person
import re
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.
def check(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        return False

class Signup(APIView):   # class for signup
    def get(self,request):
      userid=request.GET.get('userid')
      details= Person.objects.filter(userid=userid).first() 
      user={'fname':details.fname,'lname':details.lname}
      print(user)
      return Response(user,status.HTTP_200_OK)
   
    def post(self,request): 
      fname=request.data.get('fname')
      lname=request.data.get('lname')
      email=request.data.get('email')
      details= Person.objects.filter(email=email, flag=1).first()  #checking email is unique or not
      if details:
          return Response({"message": "Email is already exist"}, status=status.HTTP_400_BAD_REQUEST)
      password=request.data.get('password')
      userdob=request.data.get('userdob')
      check1 = check(email)
      if not fname or not lname or not password or not userdob or not email: #checking is any of the field is empty
         return Response({"message": "Please fill required fields"}, status=status.HTTP_400_BAD_REQUEST)
      #checking email pattern
      elif not check1:                                                                              
         return Response({"message": "Bad email"}, status=status.HTTP_400_BAD_REQUEST)
      password_hash = make_password(password)
      # print( fname,lname,email,password,dob)
      Person.objects.create(fname=fname,lname=lname,email=email,password=password_hash,userdob=userdob)
       
      #print(x.userid,x.fname)
      return Response({"result":"successful signup"},status.HTTP_200_OK)

class Signin(APIView):
    def post(self, request):
      email = request.POST.get('email')
      password = request.POST.get('password')
      details = Person.objects.filter(email=email, flag=1).first() #email verification from database
      if details:
         if not email or not password:
            return Response({'message': 'Missing email/password'}, status=status.HTTP_400_BAD_REQUEST)
         if check_password(password, details.password):
            return Response({'message': 'Signin succesful'}, status=status.HTTP_200_OK)
         else:
            return Response({'message': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)
      else:
            return Response({'message': "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)