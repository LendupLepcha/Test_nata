from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Zodiac, Aspects
from . import natal as nt


def view_create(request):
    global e_u
    if request.method == 'POST':
        form = forms.TakeInput(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            global e_u
            e_u = form.save(commit=False)
            instance.save()
            return redirect('chart:show')
    else:
        form = forms.TakeInput()
    return render(request, 'chart/input.html', { "form": form})

def view_show(request):
    if e_u != 0:
        t, row, tsp = nt.get_angles(e_u.year, e_u.month, e_u.day, e_u.hour, e_u.minute, e_u.latitude, e_u.longitude)
        point,aspect = nt.draw_chart(t, row, tsp)
        
        return render(request, 'chart/show.html', {'aspect': aspect, 'point':point})
    else:
         return HttpResponse('No e_u found')
