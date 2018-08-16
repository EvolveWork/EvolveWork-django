from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect

from .forms import SignupForm

User = get_user_model()


def home_page_view(request, notification=None):
    context = {
        'notification': notification
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.add_message(request, messages.INFO, 'Account successfully created.')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
