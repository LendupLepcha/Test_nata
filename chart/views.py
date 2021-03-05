from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Zodiac, Aspects, User_info
from django.contrib.auth.decorators import login_required
from . import natal as nt
ts = nt.load.timescale()
from django.contrib import messages 
# from .models import Stat_Images
import pickle
np = nt.np
cv = nt.cv
file_to_read = open("media/images.pickle", "rb")
images_stat = pickle.load(file_to_read)
file_to_read.close()


@login_required(login_url="/accounts/login/")
def view_create(request):
    global e_u, time_e, point, aspect
    if request.method == 'POST':
        form = forms.TakeInput(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.user
            time = ts.utc(instance.year, instance.month, instance.day, instance.hour, instance.minute)
            instance.datetime = time.utc_jpl()
            # instance.author = request.user
            check_inst = User_info.objects.filter(name=instance.name,datetime=instance.datetime,latitude=instance.latitude,longitude=instance.longitude)
            if check_inst.exists():
                messages.error(request, "This data is already saved in database!!")
                return redirect('chart:create')
            instance.save()
            e_u = form.save(commit=False)
            
            if e_u != 0:
                t, row, tsp = nt.get_angles(e_u.year, e_u.month, e_u.day, e_u.hour, e_u.minute, e_u.latitude, e_u.longitude)
                point,aspect = nt.draw_chart(t, row, tsp, images_stat)
                
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

@login_required(login_url="/accounts/login/")
def view_show(request):
    # ts = nt.load.timescale()
    if e_u != 0:
       
        return render(request, 'chart/show.html', {'name':e_u.name,'aspect': aspect, 'point':point, 'time':time_e, 'lat':e_u.latitude, 'lon':e_u.longitude} )
    else:
         return HttpResponse('No e_u found')

@login_required(login_url="/accounts/login/")
def view_search(request):
    if request.method == 'POST':
            return redirect('chart:search_results')
    else:
        form = forms.Search_Input()
    return render(request, 'chart/search.html', {'form':form})

def view_search_results(request):
    # print(result['name'])
    if request.method == 'POST':
        form = forms.Search_Input(request.POST)
        if form.is_valid():
            stime = ts.utc(
                int(form.data['syear']),
                int(form.data['smonth']),
                int(form.data['sday']),
                int(form.data['shour']),
                int(form.data['sminute'])
            )
            sresult = {
                # 'name' : form.data['sname'],
                'time' : stime.utc_jpl(),
                'latitude' : form.data['slatitude'],
                'longitude' : form.data['slongitude']
            }
            # ui = User_info.objects.filter(datetime = sresult['time'], latitude = sresult['latitude'], longitude = sresult['longitude'])
            asp = Aspects.objects.filter(datetime = sresult['time'], lat = sresult['latitude'], lon = sresult['longitude'])
            zod = Zodiac.objects.filter(datetime = sresult['time'], lat = sresult['latitude'], lon = sresult['longitude'])
            if asp.exists() and zod.exists():
                # print('no time for that', sresult['time'])
                return render(request, 'chart/search_results.html', { 'asp':asp, 'zod':zod, 'results':sresult})
                
            else:
                # print(sresult['time'])
                messages.error(request, "NO DATA FOUND!!")
                # return HttpResponse('No such input in database')
                return redirect('chart:search')
    else:
        messages.error(request, "NO INPUT GIVEN!!")
        return redirect('chart:search')