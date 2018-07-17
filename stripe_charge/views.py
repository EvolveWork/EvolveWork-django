from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import BillingProfile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def charge_view(request):
    context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
    return render(request, "charge.html", context)


@login_required
def checkout(request):
    payee = BillingProfile(
        first_name="Cody",
        last_name="Bontecou",
        email="bontecouc@gmail.com",
    )

    if request.method == "POST":
        token = request.POST.get("stripeToken")

    try:
        charge = stripe.Charge.create(
            amount=2000,
            currency="usd",
            source=token,
            description="The product charged to the user"
        )

        payee.stripe_id = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        payee.save()
        return redirect('charge_success')


def charge_success(request):
    return render(request, 'charge_success.html', {})