from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'login_reg/index.html')

def success(request):
    context = {
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login_reg/success.html', context)

def create(request):
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('index:home')
    user = User.objects.create_user(request.POST)
    request.session['user_id'] = user.id
    #submit the validation request and create user here.
    print(request.POST)
    return redirect ('index:success')

def login(request):
    valid, response = User.objects.login_user(request.POST)
    if valid == True:
        request.session['user_id'] = response
        return redirect('index:success')
    else:
        messages.error(request, response)
    print(request.POST)
    return redirect('index:home')
    
