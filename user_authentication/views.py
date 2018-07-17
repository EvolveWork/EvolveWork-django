# import stripe
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignupForm
from .tokens import account_activation_token

User = get_user_model()


def home_page_view(request):
    return render(request, 'home.html', {})


@login_required
def charge_view(request):
    context = {}
    return render(request, 'charge.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Evolve Co-working account.'
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [to_email], fail_silently=False)

            return HttpResponse('signup_confirm')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def signup_confirm(request):
    return render(request, 'registration/signup_confirm.html', {})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
