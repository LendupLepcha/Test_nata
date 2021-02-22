from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Zodiac, Aspects
from . import natal as nt
ts = nt.load.timescale()

def view_create(request):
    global e_u
    if request.method == 'POST':
        form = forms.TakeInput(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            time = ts.utc(instance.year, instance.month, instance.day, instance.hour, instance.minute)
            instance.datetime = time.utc_jpl()
            # instance.author = request.user
            global e_u, time_e, point, aspect
            e_u = form.save(commit=False)
            instance.save()
            if e_u != 0:
                t, row, tsp = nt.get_angles(e_u.year, e_u.month, e_u.day, e_u.hour, e_u.minute, e_u.latitude, e_u.longitude)
                point,aspect = nt.draw_chart(t, row, tsp)
                time_e = t.utc_jpl()
                
                for i in aspect:
                    asp= Aspects()
                    asp.body1 = i[0]
                    asp.body2 = i[1]
                    asp.shape = i[2]
                    asp.degree_type = i[3]
                    asp.degree = i[4]
                    asp.lat = e_u.latitude
                    asp.lon = e_u.longitude
                    asp.entry_time = e_u.entry_time
                    asp.name = e_u.name
                    asp.datetime = e_u.datetime
                    asp.save()
                for i in point:
                    zod = Zodiac()
                    zod.lat = e_u.latitude
                    zod.lon = e_u.longitude
                    zod.entry_time = e_u.entry_time
                    zod.name = e_u.name
                    zod.datetime = e_u.datetime
                    zod.point = i[0]
                    zod.zodiac = i[1]
                    zod.z_longitude = i[2]
                    zod.house = i[3]
                    zod.RA = i[4]
                    zod.save()
            return redirect('chart:show')
    else:
        form = forms.TakeInput()
    return render(request, 'chart/input.html', { "form": form})


def view_show(request):
    # ts = nt.load.timescale()
    if e_u != 0:
       
        return render(request, 'chart/show.html', {'aspect': aspect, 'point':point, 'time':time_e, 'lat':e_u.latitude, 'lon':e_u.longitude})
    else:
         return HttpResponse('No e_u found')
