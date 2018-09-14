import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge_view(request):
    user = request.user
    if user.is_authenticated:
        if user.stripeId:
            return redirect('renew_subscription')
        if user.stripeId is None:
            context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
            return render(request, "charge.html", context)
    return redirect('account')


def checkout(request):
    user = request.user
    if user.is_authenticated:
        if user.stripeId is None:
            if request.method == 'POST':
                try:
                    new_customer = create_stripe_customer(request, user)
                    load_stripe_form_data_into_user_model(request, user)
                    user.set_stripe_id(new_customer.id)
                except stripe.error.CardError as ce:
                    return False, ce
                else:
                    user.save()
                    return redirect('charge_success')
    return redirect('account')


def create_stripe_customer(request, user):
    return stripe.Customer.create(
        email=user.email,
        plan='plan_DJBWu9zs91csmJ',
        card=request.POST.get("stripeToken")
    )


def load_stripe_form_data_into_user_model(request, user):
    user.stripeBillingAddressLine1 = request.POST.get('stripeBillingAddressLine1')
    user.zipCode = request.POST.get('stripeBillingAddressZip')
    user.billingAddressState = request.POST.get('stripeBillingAddressState')
    user.billingAddressCity = request.POST.get('stripeBillingAddressCity')
    user.billingAddressCountry = request.POST.get('stripeBillingAddressCountry')


@login_required()
def charge_success(request):
    return render(request, 'charge_success.html', {})


@login_required()
def cancel_subscription(request):
    return render(request, 'charge_cancel.html', {})


@login_required()
def cancel_subscription_complete(request):
    user = request.user
    try:
        customer = retrieve_stripe_customer(user)
        subscription_id = get_subscription_id_from_stripe_customer(customer)
        subscription = retrieve_stripe_subscription(subscription_id)
        # subscription.update(cancel_at_period_end=True) --- Documentation states to use this but it doesnt work
        subscription.cancel_at_period_end = True
        subscription.save()
        user.cancel_at_period_end = True
        user.save()
        # for k, v in subscription.items():
        #     print(k, v)
    except Exception as e:
        messages.error(request, "Looks like something went wrong. Are you sure you have a subscription set up?")
    return render(request, 'charge_cancel_complete.html', {})


def retrieve_stripe_customer(user):
    return stripe.Customer.retrieve(user.stripeId)


def get_subscription_id_from_stripe_customer(customer):
    return customer.subscriptions.get('data')[0].get('id')


def retrieve_stripe_subscription(subscription_id):
    return stripe.Subscription.retrieve(subscription_id)


def renew_subscription(request):
    return render(request, 'renew_subscription.html', {})


def renew_subscription_complete(request):
    return render(request, 'renew_subscription_complete.html', {})
