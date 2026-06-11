from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage/index.html')

def nowhere(request):
    return render(request, 'homepage/nowhere.html')