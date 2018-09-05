import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge_view(request):
    user = request.user
    if user.is_authenticated and user.stripeId is None:
        context = {"stripe_key": settings.STRIPE_TEST_PUBLIC_KEY}
        return render(request, "charge.html", context)
    return redirect('account')


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
                    user.save()
                    load_stripe_form_data_into_user_model(request, user)
                except stripe.error.CardError as ce:
                    return False, ce
                else:
                    return redirect('charge_success')
    return redirect('account')


def load_stripe_form_data_into_user_model(request, user):
    user.stripeBillingAddressLine1 = request.POST.get('stripeBillingAddressLine1')
    user.zipCode = request.POST.get('stripeBillingAddressZip')
    user.billingAddressState = request.POST.get('stripeBillingAddressState')
    user.billingAddressCity = request.POST.get('stripeBillingAddressCity')
    user.billingAddressCountry = request.POST.get('stripeBillingAddressCountry')
    user.save()


@login_required()
def charge_success(request):
    return render(request, 'charge_success.html', {})


@login_required()
def cancel_subscription(request):
    return render(request, 'charge_cancel.html', {})


def handle_stripe_exception(exception):
    print('Exception Handled: ' + str(exception))


def get_customer_from_stripe_id(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripeId)
        return customer
    except Exception as exception:
        handle_stripe_exception(exception)


def get_subscription_id_from_customer_id(customer):
    try:
        subscription_id = customer.subscription.get('data')[0].get('id')
        return subscription_id
    except Exception as exception:
        handle_stripe_exception(exception)


def get_subscription_from_subscription_id(subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription
    except Exception as exception:
        handle_stripe_exception(exception)


@login_required()
def cancel_subscription_complete(request):
    try:
        customer = get_customer_from_stripe_id(request)
        subscription_id = get_customer_from_stripe_id(customer)
        subscription = get_subscription_from_subscription_id(subscription_id)
        subscription.cancel_at_period_end = True
        for k, v in subscription.items():
            print(k, v)
    except Exception as e:
        messages.error(request, "Looks like something went wrong. Are you sure you have a subscription set up?")
        print(e)
    return render(request, 'charge_cancel_complete.html', {})


def renew_subscription(request):
    context = {}
    return render(request, 'renew_subscription.html', context)


def renew_subscription_complete(request):
    context = {}
    return render(request, 'renew_subscription_complete.html', context)
