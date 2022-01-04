from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature


# Create your views here.


def index(request):
    return render(request, 'index.html')


def counter(request):
    features = Feature.objects.all()
    return render(request, 'counter.html', {'features': features})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already In Use')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Sorry! USERNAME already exist. Please try another')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                return redirect('login')

        else:
            messages.info(request, 'passwords does not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('counter')

        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
