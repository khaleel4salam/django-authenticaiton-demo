from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


@login_required
def index(request):
    return render(request, "user.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    message = ""
    if request.method == "POST":
        # Extract username, not email
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = "Invalid username or password."

    return render(request, 'login.html', {'message': message})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')