from django.shortcuts import render

def view_create(request):
    return render(request, 'chart/input.html')
