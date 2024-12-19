from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from models import *


def sign_up(request):
    buyers = Buyer.objects.all()
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        if password == repeat_password and int(age) >= 18 and username not in str(buyers):
            Buyer.objects.create(username=username, balance=2000.0, age=age)
            return HttpResponse(f'Добро пожаловать {username}!')
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают!'
        elif int(age) <= 18:
            info['error'] = 'Вам ещё нет 18!'
        elif username in str(buyers):
            info['error'] = 'Такой пользователь уже существует!'
    return render(request, 'templates/registration_view.html', context=info)


def shop_view(request):
    return render(request, 'templates/menu.html')


def cart_view(request):
    return render(request, 'templates/cart.html')


def game_view(request):
    return render(request, 'templates/games.html')


def news_view(request):
    return render(request, 'templates/news.html', context='news')
# Create your views here.