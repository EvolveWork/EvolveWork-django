import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def charge_view(request):
    context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
    return render(request, "charge.html", context)


@login_required
def checkout(request):
    if request.method == "POST":
        payee = request.user
        try:

            # Solution to not creating a new customer everytime:
            # Do a customer.retrieve on the payee's stripeId in the try.
            # Exception could be made to do what's going on currently.

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


def charge_success(request):
    return render(request, 'charge_success.html', {})


def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripeId)
        subscription_id = customer.subscriptions.get('data')[0].get('id')
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.delete(at_period_end=True)
    except Exception as e:
        messages.error(request, e)

    return render(request, 'home.html', {})
