import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user_authentication.forms import SignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge_view(request):
    if request.user.is_authenticated:
        context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
        return render(request, "charge.html", context)
    return redirect('home')


def register_and_checkout(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=1500,
                    currency='USD',
                    email=form.cleaned_data['email'],
                    card=form.cleaned_data['stripeId'],
                )

                form.save()
                return redirect('charge_success')
            except stripe.error.CardError as e:
                form.add_error(e, 'This card has been declined')
    else:
        form = SignupForm()
        months = range(1, 12)
        years = range(2018, 2036)
        publishable_api_key = settings.STRIPE_PUBLISHABLE_KEY
        context = {
            'form': form,
            'months': months,
            'years': years,
            'publishable_api_key': publishable_api_key
        }
    return render(request, 'registration.html', context)


def checkout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            payee = request.user
            try:
                #     customer = stripe.Customer.retrieve(payee.stripeId)
                #     customer.plan = 'plan_DJBWu9zs91csmJ'
                #     customer.card = request.POST.get("stripeToken")
                #     customer.save()
                # except stripe.error.InvalidRequestError as error:

                customer = stripe.Customer.create(
                    email=payee.email,
                    plan='plan_DJBWu9zs91csmJ',
                    card=request.POST.get("stripeToken")
                )
                payee.stripeId = customer.id
                payee.stripeBillingAddressLine1 = request.POST.get('stripeBillingAddressLine1')
                payee.zipCode = request.POST.get('stripeBillingAddressZip')
                payee.billingAddressState = request.POST.get('stripeBillingAddressState')
                payee.billingAddressCity = request.POST.get('stripeBillingAddressCity')
                payee.billingAddressCountry = request.POST.get('stripeBillingAddressCountry')
            except stripe.error.CardError as ce:
                return False, ce
            else:
                payee.save()
                return redirect('charge_success')
    return redirect('home')


@login_required()
def charge_success(request):
    return render(request, 'charge_success.html', {})


@login_required()
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripeId)
        subscription_id = customer.subscriptions.get('data')[0].get('id')
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.delete(at_period_end=True)
    except Exception as e:
        messages.error(request, "Looks like something went wrong. Are you sure you have a subscription set up?")
    return render(request, 'charge_cancel.html', {})
