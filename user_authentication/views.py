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


# def load_subscription_data(user):
#     customer_api_call = stripe.Customer.retrieve(user.stripeId)
#     subscription_id = customer_api_call.subscriptions.get('data')[0].get('id')
#     current_period_end = customer_api_call.subscriptions.get('data')[0].get('current_period_end')
#     renewal_date = datetime.datetime.fromtimestamp(current_period_end)
#     cancel_at_period_end = customer_api_call.subscriptions.get('data')[0].get('cancel_at_period_end')
#     # plan_id = customer_api_call.subscriptions.get('data')[0].get('items').get('data')[0].get('plan').get('id')
#
#     user.subscription_id = subscription_id
#     user.renewal_date = renewal_date
#     user.cancel_at_period_end = cancel_at_period_end
#     user.plan = Plan.objects.get(nickname='Cheap_test_monthly')
#     user.save()
