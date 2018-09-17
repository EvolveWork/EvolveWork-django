import stripe
from django.contrib.auth import login
from django.shortcuts import render, redirect

from evolve_work import settings
from .forms import SignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page_view(request):
    return render(request, 'home.html', {})


def logout(request):
    if request.user.is_authenticated:
        return render(request, 'logout.html', {})
    return redirect('home')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
