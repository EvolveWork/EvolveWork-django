import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import BillingProfile

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def charge_view(request):
    context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
    return render(request, "charge.html", context)


@login_required
def checkout(request):
    if request.method == "POST":
        payee = BillingProfile(
            name=request.POST.get('stripeBillingName'),
            email=request.POST.get('stripeEmail'),
            stripeBillingAddressLine1=request.POST.get('stripeBillingAddressLine1'),
            zipCode=request.POST.get('stripeBillingAddressZip'),
            billingAddressState=request.POST.get('stripeBillingAddressState'),
            billingAddressCity=request.POST.get('stripeBillingAddressCity'),
            billingAddressCountry=request.POST.get('stripeBillingAddressCountry')
        )
        try:
            customer = stripe.Customer.create(
                email=payee.email,
                plan='plan_DJBWu9zs91csmJ',
                card=request.POST.get("stripeToken")
            )
            payee.stripeId = customer.id

        except stripe.error.CardError as ce:
            return False, ce

        else:
            payee.save()
            return redirect('charge_success')


def charge_success(request):
    return render(request, 'charge_success.html', {})


def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripeId)
        customer.cancel_subscription(at_period_end=True)
        messages.add_message(request, messages.INFO,
                             'Subscription canceled. Your access to Evolve Coworking ends ' +
                             str(customer.current_period_end))
    except Exception as e:
        messages.error(request, e)

    return render(request, 'home.html', {})
