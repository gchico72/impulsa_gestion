from django.shortcuts import render


def index(request):
    return render(request, 'cooperadora/index.html', {})
