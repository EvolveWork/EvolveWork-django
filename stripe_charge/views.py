import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user_authentication.forms import SignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge_view(request):
    user = request.user
    if user.is_authenticated and user.stripeId is None:
        context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
        return render(request, "charge.html", context)
    return redirect('account')


# def register_and_checkout(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             try:
#                 customer = stripe.Charge.create(
#                     amount=1500,
#                     currency='USD',
#                     email=form.cleaned_data['email'],
#                     card=form.cleaned_data['stripeId'],
#                 )
#
#                 form.save()
#                 return redirect('charge_success')
#             except stripe.error.CardError as e:
#                 form.add_error(e, 'This card has been declined')
#     else:
#         form = SignupForm()
#         months = range(1, 12)
#         years = range(2018, 2036)
#         publishable_api_key = settings.STRIPE_PUBLISHABLE_KEY
#         context = {
#             'form': form,
#             'months': months,
#             'years': years,
#             'publishable_api_key': publishable_api_key
#         }
#     return render(request, 'registration.html', context)


def checkout(request):
    user = request.user
    if user.is_authenticated:
        if user.stripeId is None:
            if request.method == 'POST':
                try:
                    new_customer = stripe.Customer.create(
                        email=user.email,
                        plan='plan_DJBWu9zs91csmJ',
                        card=request.POST.get("stripeToken")
                    )
                    user.stripeId = new_customer.id
                    user.stripeBillingAddressLine1 = request.POST.get('stripeBillingAddressLine1')
                    user.zipCode = request.POST.get('stripeBillingAddressZip')
                    user.billingAddressState = request.POST.get('stripeBillingAddressState')
                    user.billingAddressCity = request.POST.get('stripeBillingAddressCity')
                    user.billingAddressCountry = request.POST.get('stripeBillingAddressCountry')
                    user.save()
                except stripe.error.CardError as ce:
                    return False, ce
                else:
                    return redirect('charge_success')
    return redirect('account')


@login_required()
def charge_success(request):
    return render(request, 'charge_success.html', {})


@login_required()
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripeId)
        subscription_id = customer.subscriptions.get('data')[0].get('id')
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.cancel_at_period_end = True
        for k, v in subscription.items():
            print(k, v)
    except Exception as e:
        messages.error(request, "Looks like something went wrong. Are you sure you have a subscription set up?")
        print(e)
    return render(request, 'charge_cancel.html', {})
