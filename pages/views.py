from django.shortcuts import render, HttpResponse


def home_view(request):
    return render(request, 'pages/index.html')


def shop_view(request):
    return render(request, 'pages/shop.html')
