# import stripe
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import logout
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm

User = get_user_model()


def home_page_view(request):
    return render(request, 'home.html', {})


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context["form"] = LoginForm
            return redirect("/")
        else:
            print("Login Error")
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def charge_view(request):
    context = {}
    return render(request, 'charge.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        messages.Info(request, "Thanks for registering. You are now logged in.")
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)

        new_user.is_active = False
        new_user.save()

        # send_mail('Complete your registration',
        #           new_user.username + ' has registered. Please activate the account.',
        #           settings.EMAIL_HOST_USER,
        #           ['bontecouc@gmail.com'], fail_silently=False)
        return HttpResponseRedirect('registration/redirect')
    return render(request, "registration.html", context)


def registration_redirect(request):
    return render(request, "registration_redirect.html", {})

#     try:
#         charge = stripe.Charge.create(
#             amount={{amount}},
#             currency="usd",
#             customer={{customer}},
#             description={{description}},
#             metadata={{this.id}}
#         )
#     except stripe.error.CardError as e:
#         # Problem with the card
#         pass
#     except stripe.error.RateLimitError as e:
#         # Too many requests made to the API too quickly
#         pass
#     except stripe.error.InvalidRequestError as e:
#         # Invalid parameters were supplied to Stripe API
#         pass
#     except stripe.error.AuthenticationError as e:
#         # Authentication Error: Authentication with Stripe API failed (maybe you changed API keys recently)
#         pass
#     except stripe.error.APIConnectionError as e:
#         # Network communication with Stripe failed
#         pass
#     except stripe.error.StripeError as e:
#         # Stripe Error
#         pass
#     else:
# # success
