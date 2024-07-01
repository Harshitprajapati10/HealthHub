import re  
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import CustomUser

from django.db import models

def home(request):
  user = request.user
  if user.is_authenticated:
    return render(request, "authentication/index.html")
  else:
    return redirect("signin")
  
def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        picture = request.FILES.get('profile_picture', None)
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        is_doctor = request.POST.get('is_doctor', False) 

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, "authentication/signup.html")

        if not re.match(r'^[a-zA-Z]+$', fname):
            messages.error(request, "First name must contain only letters.")
            return render(request, "authentication/signup.html")
        if not re.match(r'^[a-zA-Z]+$', lname):
            messages.error(request, "Last name must contain only letters.")
            return render(request, "authentication/signup.html")
        
        # Check password complexity
        if len(pass1) < 8 or \
           not re.search(r'[A-Z]', pass1) or \
           not re.search(r'[a-z]', pass1) or \
           not re.search(r'[0-9]', pass1) or \
           not re.search(r'[\W_]', pass1):
            messages.error(request, "Password must be at least 8 characters long and include a combination of uppercase, lowercase, numbers, and symbols.")
            return render(request, "authentication/signup.html")
        
        try:
            myuser = CustomUser.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.profile_picture = picture  
            myuser.address = address
            myuser.state = state
            myuser.city = city
            myuser.pincode = pincode
            myuser.is_doctor = is_doctor
            myuser.save()  

            messages.success(request, "Your account has been successfully created")
            print()
            return redirect("signin")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, "authentication/signup.html")

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
        
        # Check password match using password hashing
        if user.check_password(pass1):
            login(request, user)
            fname = user.first_name
            lname = user.last_name  
            username = user.username
            address = user.address  
            state = user.state  
            city = user.city  
            context = {
                'fname': fname,
                'lname': lname,
                'username': username,
                'address': address,
                'state': state,
                'city': city,
            }
            return render(request, "authentication/index.html", context)
            
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successsfully")
    return redirect('signin')



