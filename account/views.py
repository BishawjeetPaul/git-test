from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
# This function for showing homepage
def index_page(request):
    return render(request, "account/index_page.html")


# This function was user registration
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,  
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                return redirect('register')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
    return render(request, 'account/registration.html')


# This function was user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Invalid Email or Password")
            return redirect('login')
    else:
        return render(request, 'account/login.html')
