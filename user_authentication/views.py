import datetime

import stripe
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from stripe.error import InvalidRequestError

from evolve_work import settings
from .forms import SignupForm

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page_view(request, notification=None):
    context = {
        'notification': notification,
    }
    return render(request, 'home.html', context)


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


def account(request):
    user = request.user
    if user.is_authenticated:
        if user.stripeId:
            try:
                customer = stripe.Customer.retrieve(user.stripeId)
                current_period_end = customer.subscriptions.get('data')[0].get('current_period_end')
                timestamp = datetime.datetime.fromtimestamp(current_period_end)
                return render(request, 'account.html', {'timestamp': timestamp, 'current_period_end': current_period_end})
            except InvalidRequestError:
                messages.warning(request, 'Looks like something went wrong. Please try again later.')
            except Exception:
                messages.warning(request, 'Looks like something went wrong. Please try again later.')
        return render(request, 'account.html', {})
    return redirect('login')
