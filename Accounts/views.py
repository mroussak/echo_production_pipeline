from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from Accounts.forms import RegisterForm

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.username = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('apps')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})