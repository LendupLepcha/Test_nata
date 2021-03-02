from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Zodiac, Aspects
from . import natal as nt
ts = nt.load.timescale()
from .models import Stat_Images

np = nt.np
cv = nt.cv
si = Stat_Images.objects.get(ids = 100)
ims = np.asarray(bytearray(si.chart_frame.read()), dtype="uint8")
img = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.aspact_frame.read()), dtype="uint8")
grid_img = cv.imdecode(ims, 0)
local = {}
ims = np.asarray(bytearray(si.sun.read()), dtype="uint8")
local['sun'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.moon.read()), dtype="uint8")
local['moon'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.mercury.read()), dtype="uint8")
local['mercury'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.venus.read()), dtype="uint8")
local['venus'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.mars.read()), dtype="uint8")
local['mars'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.jupiter.read()), dtype="uint8")
local['jupiter'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.saturn.read()), dtype="uint8")
local['saturn'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.uranus.read()), dtype="uint8")
local['uranus'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.neptune.read()), dtype="uint8")
local['neptune'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.pluto.read()), dtype="uint8")
local['pluto'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.ceres.read()), dtype="uint8")
local['ceres'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.conjunction.read()), dtype="uint8")
local['conjunction'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.opposition.read()), dtype="uint8")
local['opposition'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.square.read()), dtype="uint8")
local['square'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.sextile.read()), dtype="uint8")
local['sextile'] = cv.imdecode(ims, 0)
ims = np.asarray(bytearray(si.trine.read()), dtype="uint8")
local['trine'] = cv.imdecode(ims, 0)

def view_create(request):
    global e_u, time_e, point, aspect
    if request.method == 'POST':
        form = forms.TakeInput(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            time = ts.utc(instance.year, instance.month, instance.day, instance.hour, instance.minute)
            instance.datetime = time.utc_jpl()
            # instance.author = request.user
            instance.save()
            e_u = form.save(commit=False)
            
            if e_u != 0:
                t, row, tsp = nt.get_angles(e_u.year, e_u.month, e_u.day, e_u.hour, e_u.minute, e_u.latitude, e_u.longitude)
                point,aspect = nt.draw_chart(t, row, tsp, img, grid_img, local)
                
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
       
        return render(request, 'chart/show.html', {'name':e_u.name,'aspect': aspect, 'point':point, 'time':time_e, 'lat':e_u.latitude, 'lon':e_u.longitude} )
    else:
         return HttpResponse('No e_u found')
