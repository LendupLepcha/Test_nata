from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Zodiac, Aspects



def view_create(request):
    if request.method == 'POST':
        form = forms.TakeInput(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            global e_time
            e_time = instance.__class__.objects
            instance.save()
            return redirect('chart:show')
    else:
        form = forms.TakeInput()
    return render(request, 'chart/input.html', { "form": form})

def view_show(request):
    if e_time != 0:
        return render(request, 'chart/show.html', {'e_time': e_time})
    else:
         return HttpResponse('No e_time found')
