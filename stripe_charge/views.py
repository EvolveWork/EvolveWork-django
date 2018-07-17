import datetime

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf

from .forms import StripeBillingForm

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def charge_view(request):
    if request.method == 'POST':
        form = StripeBillingForm(request.POST)
        if form.is_valid():
            try:
                # Amount is dealt with in units. 499 = $4.99 when currency = USD
                charge = stripe.Charge.create(
                    amount=499,
                    currency='USD',
                    customer=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id']
                )
                form.save()
                redirect('/')
            except stripe.CardError as e:
                # Problem with the card
                form.add_error("The card has been declined")
        else:
            # success
            form = StripeBillingForm()

        context = {}
        context.update(csrf(request))
        context['form'] = form
        context['publishable'] = settings.STRIPE_PUBLISHABLE_KEY
        context['months'] = range(1, 12)
        context['years'] = range(2011, 2036)
        context['soon'] = datetime.date.today() + datetime.timedelta(days=30)

        return render_to_response('charge.html', context)
