from django.shortcuts import render, redirect
from users.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(password=raw_password)
            # login(request, user)
            username = form.cleaned_data['username']
            password = form.cleaned_data.get('password')
            messages.success(request, f'Account created for {username}')
            user.set_password(password)
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('all_products')
            return redirect('all_products')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
