import datetime

import stripe
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect

from evolve_work import settings
from .forms import SignupForm

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page_view(request, notification=None):
    context = {
        'notification': notification,
        'stripe_key': settings.STRIPE_TEST_PUBLIC_KEY
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.add_message(request, messages.INFO, 'Account successfully created.')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def account(request):
    user = request.user
    if user.stripeId:
        customer = stripe.Customer.retrieve(user.stripeId)
        current_period_end = customer.subscriptions.get('data')[0].get('current_period_end')
        timestamp = datetime.datetime.fromtimestamp(current_period_end)
        return render(request, 'account.html', {'current_period_end': timestamp})
    return render(request, 'account.html', {'current_period_end': 'N/A'})
