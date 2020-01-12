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
 # This class is to execute the sign-up process which involves acceptig user details like
        # first name,
        # last name,
        # dob,
        # email (needs to be unique and is checked for validity)
        # password (becrypt is used to encrypt it)
        # The following outputs are expected:
        # <Created 201>
        # {"Message": "Signed up succesfully!"}

        # <Bad request 400>
        # {"Message": "Fill the empty fields"}
        # (if any field is not filled)

        # <Bad request 400>
        # {"Message": "User already exists"}
        # (if email address already exists in the database)

        # <Bad request 400>
        # {"Message": "Invalid email address"}
        # (if email is not valid)

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
      password=request.data.get('password')
      userdob=request.data.get('userdob')
      check1 = check(email)
      if details:
          return Response({"message": "Email is already exist"}, status=status.HTTP_400_BAD_REQUEST)
      if not fname or not lname or not password or not userdob or not email: #checking is any of the field is empty
         return Response({"message": "Please fill required fields"}, status=status.HTTP_400_BAD_REQUEST)
      elif not check1:                                                                              
         return Response({"message": "Bad email"}, status=status.HTTP_400_BAD_REQUEST)
      password_hash = make_password(password)
      Person.objects.create(fname=fname,lname=lname,email=email,password=password_hash,userdob=userdob)
      return Response({"result":"successful signup"},status.HTTP_200_OK)

class Signin(APIView):
     # This class is to execute the sign-up process which involves acceptig user details including
    # user email (this is checked for validity and whether this address exists in the database)
    # password (bcrypt is used to compare this password with the hashed password stored in the database)
    # Outputs include:
    # <Created 201>
    # {"Message": "Authentication successful!", "Your user id":"id"}
    # (if the user exists in the database, the user-id of the user is shared for him to use)

    # <Bad request 400>
    # {"Message": "Fill the empty fields"}
    # (if any field is not filled)

    # <Bad request 400>
    # {"Message": "Invalid email address"}
    # (if email is not valid)

    # <Bad request 400>
    # {"message": "User doesn't exist"}
    # (if the email is not in the database)

    # <Bad request 400>
    # {"message": "Invalid credentials"}
    # (if the passwords don't match)
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
         
class Display(APIView):
    # This class is for the user to see their details which are retrieved from the database
    # On entering their userid (received during Sign-in), they can get their details.
    # Outputs received:
    # <Bad request 400>
    # {"Message": "Fill the empty fields"}
    # (if any field is not filled)

    # <Bad request 400>
    # {"message": "User doesn't exist"}
    # (if the userid is not in the database)

    # <Created 201>
    # {"Your details: First-name:": userdetails.fname, "Last-name:": userdetails.lname, "Date of birth:": userdetails.userdob, "Email:": userdetails.useremail}
    def get(self, request):
        id = request.GET.get('userid')
        if not id:
            return Response({"Message": "Please fill the empty field"}, status.HTTP_400_BAD_REQUEST)
        else:
            userdetails = Person.objects.filter(userid=id).first()
            if not userdetails:
                return Response({"Message": "User doesn't exist"}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Your details: First-name:": userdetails.fname, "Last-name:": userdetails.lname, "Date of birth:": userdetails.userdob, "Email:": userdetails.useremail}, status.HTTP_200_OK)


class Update(APIView):
    def post(self, request):
        # This function is to execute updation of user details using the id they are given after Sign-in
        # The user-id is compulsorily accepted for retrieving that particular user's details.
        # The updated values are accepted for updation in the database.
        # Outputs possible:
        # <Bad request 400 >
        # {"Message": "Please enter the user id you were given"}
        # (If user doesn't enter the user id)

        # <Bad request 400 >
        # {"Message": "User doesn't exist / You can't update your user id"}
        # (If user id is not present in the database or a different id is entered by user)

        # <Bad request 400 >
        # {"Message": "Please fill the field you want to update"}
        # (If the user doesn't enter any updated value)

        # <Created 201 >
        # {"Message": "User details updated successfully!"}
        # (User details are updated)

        id = request.data.get('userid')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        dob = request.data.get('userdob')
        password = request.data.get('password')
        if not id:
            return Response({"Message": "Please enter the user id you were given"}, status.HTTP_400_BAD_REQUEST)
        else:
            details = Person.objects.filter(userid=id).first()
            if not details:
                return Response({"Message": "User doesn't exist / You can't update your user id"}, status.HTTP_400_BAD_REQUEST)
            else:
                if not fname and not lname and not dob and not password:
                    return Response({"Message": "Please fill the field you want to update"}, status.HTTP_400_BAD_REQUEST)
                else:
                    if fname:
                        details.fname = fname
                    if lname:
                        details.lname = lname
                    if dob:
                        details.userdob = dob
                    if password:
                        details.password = password
                    details.save()
                    return Response({"Message": "User details updated successfully!"}, status.HTTP_200_OK)
