from django.http import HttpResponse
from django.shortcuts import render
from models import *


def sign_up(request):
    buyers = NewUser.objects.all()
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        if password == repeat_password and int(age) >= 18 and username not in str(buyers):
            NewUser.objects.create(username=username, balance=2000.0, age=age)
            return HttpResponse(f'Добро пожаловать {username}!')
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают!'
        elif int(age) <= 18:
            info['error'] = 'Вам ещё нет 18!'
        elif username in str(buyers):
            info['error'] = 'Такой пользователь уже существует!'
    return render(request, 'templates/registration_view.html', context=info)


def info_view(request):
    return render(request, 'firstapp/info.html')