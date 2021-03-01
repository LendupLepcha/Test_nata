


import numpy as np
import math
import pandas as pd
import cv2 as cv
import copy
from skyfield.api import E, N, W, wgs84, load, load_file, Star
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.units import Distance
from skyfield.almanac import find_discrete, sunrise_sunset

from .models import Stat_Images
# Global variables

si = Stat_Images.objects.get(ids = 100)


# img = cv.imread('static/chart_frame_equal_house.jpg', 0 )
ims = np.asarray(bytearray(si.chart_frame.read()), dtype="uint8")
img = cv.imdecode(ims, 0)
# img = cv.imread(si.chart_frame, 0)
# print('here')
# print(img)
image_original=copy.deepcopy(img)
# grid_img = cv.imread('static/aspect_grid_frame_withceres.jpg', 0)
ims = np.asarray(bytearray(si.aspact_frame.read()), dtype="uint8")
grid_img = cv.imdecode(ims, 0)
# grid_img = si.aspact_frame
grid_original=copy.deepcopy(grid_img)
font = cv.FONT_HERSHEY_SIMPLEX


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


ts = load.timescale()



planets=[
    'sun',
    'moon',
    'mercury barycenter',
    'venus barycenter',
    'mars barycenter',
    'jupiter barycenter',
    'saturn barycenter',
    'uranus barycenter',
    'neptune barycenter',
    'pluto barycenter'
]
Planet_names = [
    'sun',
    'moon',
    'mercury',
    'venus',
    'mars',
    'jupiter',
    'saturn',
    'uranus',
    'neptune',
    'pluto',
    'ceres'
]
zodiacs = {
        'Aries': [0, 30],
        'Taurus': [30, 60],
        'Gemini': [60, 90],
        'Cancer': [90, 120],
        'Leo': [120, 150],
        'Virgo': [150, 180],
        'Libra': [180, 210],
        'Scorpio': [210, 240],
        'Sagittarius': [240, 270],
        'Capricorn': [270, 300],
        'Aquarius': [300, 330],
        'Pisces': [330, 360]
}
zodiac = pd.DataFrame(zodiacs)
eph = load_file('media/de421.bsp')




earth = eph['earth']
coordinates = wgs84.latlon( 27.3314 , 88.6138)
location = earth + coordinates
# gg = gangtok.at(time_p)
P= {}
for i, j in zip(planets, Planet_names[:-1]):
    P[j] = eph[i]




with load.open('media/MPCORB.excerpt.DAT') as f:
    minor_planets = mpc.load_mpcorb_dataframe(f)
row_ceres=minor_planets.iloc[0]
sun = eph['sun']
ceres = sun + mpc.mpcorb_orbit(row_ceres, ts, GM_SUN)



# # Draw intersect of a line and circle (Given angle from center)
def intersect_circle(angle,r):
#     m = 3.14
    signx = -1
    signy = -1
    quad = 1
    if(angle == 360):
        angle = 0
        
    if(angle>=270):
        signy = 1
        angle = angle - 270
        quad = 4
    elif(angle>=180):
        signx = 1
        signy = 1
        angle = angle - 180
        quad = 3
    elif(angle>=90):
        signx = 1
        angle = angle - 90
        quad = 2
    m=math.tan(math.radians(angle))
#     print(m)
    x = math.sqrt((r*r)/(1+(m*m)))
    y = m * x
    if(quad % 2 ==0):
        x, y = y, x
#     print('x,y',x,y)
    xx = signx * math.floor(x)
    yy = signy * math.floor(y)
    return xx,yy






def insert_image(imgA, p_name, x, y):
    # local = 'static/'+p_name+'.jpg'
    # obj = cv.imread(local, 0)
    obj = local[p_name]
    length, bredth = obj.shape
    len_half, bre_half = int(length/2), int(bredth/2)
    p = q = 0
    for i in range(y-len_half, y+len_half):
        q=0
        for j in range(x-bre_half, x+bre_half):
            if(obj[p][q]<240):
                imgA[i][j] = 0
            q=q+1
        p=p+1
    return imgA


# # Draw arrow pointing the angle location



def locate_arrow(angle,image,p_name,inner=True):
    
#     p_name = 
    if (inner): # inner (True) means arrow from inside the circle
        r, r_b, r_a = 250, 232, 228
    else:
        r, r_b, r_a = 302, 320, 324
#     x, y = intersect_circle(angle,r)
    x, y = intersect_circle(angle, r) # for arrow head
    # _clock
#     x_base, y_base = intersect_circle(angle,r_b)
    x_base, y_base = intersect_circle(angle, r_b) # for arrow base
    # _clock
    xa, ya = intersect_circle(angle, r_a) #  for text
    # _clock
    img = cv.arrowedLine(image, (x_base+349,349-y_base), (x+349,349-y), 0, 1, tipLength= .5)
#     img = cv.putText(img,p_name[:2],(xa+349,349-ya), font, .3,(0),1,cv.LINE_AA);
#     img = cv.rectangle(img, (xa+349-7,349-ya-7), (xa+349+7,349-ya+7), 0, 1)
    img = insert_image(image, p_name, xa+349, 349-ya)
    return img


# # Read angles of planets



def get_angles(y, m, d, h, mins, lat, lon):
    # print('Enter Date and Time')
    # y = int(input('Year: '))
    # m = int(input('month: '))
    # d = int(input('day: '))
    # h = int(input('hour: '))
    # mins = int(input('minute:'))
    # sec = int(input('second: '))
    tx = ts.utc(y, m, d, h, mins)
    tsp = [ts.utc(y, m, d), ts.utc(y, m, d+1)]
    print('Date : ', tx.utc_jpl())
    print('Enter Location')
    # lat = float(input('Latitude:'))
    # lon = float(input('Longitude:'))
    coordinates = wgs84.latlon( lat, lon)
    location = earth + coordinates
    gg = location.at(tx)
    row = {}
    for i in Planet_names[:-1]:
        q = P[i]
        ra, dec, dist = gg.observe(q).apparent().ecliptic_latlon()
#         row[i] = ra.hours * 360 / 24
        row[i] = dec.degrees
    ra, dec, distance = gg.observe(ceres).ecliptic_latlon()
#     row['ceres'] = ra.hours *360 / 24
    row['ceres'] = dec.degrees
    rowpd = pd.DataFrame([row], columns = Planet_names)
#     print(rowpd)
    return tx, rowpd, tsp;



def check_row(degree, name, row):
    a = copy.deepcopy(row)
#     i = list(Planet_names).index(name)
#     r = a.pop(i)
    n = list(Planet_names).index(name) 
    #print(n)
    a = a.drop(name)
    for j in range(n):
        if abs(degree-a[j])<2:
            return False
    return True


# ## aspect_grid function



def aspect_grid(row, p_names):
    grid = [[0 for i in range(len(row))] for j in range(len(row))]
    for i in range(len(row)):
        for j in range(i):
            s=-1
            diff = abs(row[i] - row[j])
            if(diff>=50 and diff<=70) or (diff>=290 and diff<=310):
                if (diff>70):
                    diff = diff - 240
                s = 60
            elif (diff>=80 and diff<=100) or (diff>=260 and diff<=280):
                if (diff>100):
                    diff = diff - 180
                s = 90
            elif (diff>=110 and diff<=130) or (diff>=230 and diff<=250):
                if (diff>130):
                    diff = diff - 120
                s = 120
            elif (diff>=170 and diff<=190):
                s = 180
            elif(diff>=350 or diff<=10):
                if (diff>350):
                    diff = diff - 350
                s = 0
            if(s == -1):
                grid[i][j] = -1
            else:
                a = diff - s
                if(a < 0):
                    b = 'a'
                else: 
                    b = 's'
                cell = [s, b, abs(a)]
                grid[i][j] = cell
    return grid
            




def draw_grid(row, grid, img2):
    x = 80
    y = 80
    for i in range(len(row)):
        for j in range(i):
            if(isinstance(grid[i][j], list)):
                gdata = grid[i][j]
                if(gdata[0] == 90):
                    sname = 'square'
                elif(gdata[0] == 60):
                    sname = 'sextile'
                elif(gdata[0] == 120):
                    sname = 'trine'
                elif(gdata[0] == 180):
                    sname = 'opposition'
                elif(gdata[0] == 0):
                    sname = 'conjunction'
#                 sname = 'images/' + sname + '.jpg'
#                 print(sname)
                string = gdata[1].upper()+' '+str(int(round(gdata[2])))
                img2 = insert_image(img2, sname, x+22+(j*45), y-27+(i*45))
                cv.putText(img2,string,(x+12+(j*45), y-12+(i*45)), font, .3,(0),1,cv.LINE_AA);
    return img2


# # Calc rising sign



def rising(time, tsp):
    t, y = find_discrete(tsp[0], tsp[1], sunrise_sunset(eph, coordinates))
    for i, j in zip(t, y):
        if(j == 1):
            rise_t = i
    astro = location.at(rise_t).observe(sun).apparent()
    alt, az , dist = astro.altaz()
#     print('Altitude', alt)
#     print('Azimuth',az)
    horizon = location.at(time).from_altaz(alt_degrees = alt.degrees, az_degrees = az.degrees, distance = Distance(au = 1.3) )
    lat, lon, distance = horizon.ecliptic_latlon()
    As = lon.degrees
#     print(dist)
    return As


# # Draw houses



def houses(image, t, tsp):
    As = rising(t, tsp)
    
    for i in range(12):
        thick = 1
        angle = As + (i * 30)
        if(angle >= 360 ):
            angle = angle - 360
        if(i%3 == 0):
            thick = 2
        hangle = angle+15
        if(hangle>=360):
            hangle= hangle - 360
        x1, y1 = intersect_circle(angle,250)
        x, y = intersect_circle(angle,125)
        xh, yh = intersect_circle(hangle,135)
        cv.line(image,(x1+349, 349-y1),(x+349, 349-y),0,thick)
        txt = str(i+1)
        cv.putText(image,txt,(xh+343, 352-yh), font, .3,(0),1,cv.LINE_AA)
        if(i == 0):
            x0, y0 = intersect_circle(As,270)
            cv.putText(image,'As',(x0+343, 352-y0), font, .5,(0),1,cv.LINE_AA);
    return As, image


# # Chart point Report



def show_report(row, As, grid, t):
    planet = row.to_frame()
    planet = planet.T
    houses = {}
    langle = 0
    hangle = As
    for i in range(12):
        langle = hangle
        hangle = hangle + 30
        if(hangle>=360):
            hangle = hangle - 360
        houses[i+1] = [langle, hangle]
    house = pd.DataFrame(houses)
    # zodiac = pd.DataFrame(zodiacs)
    planet.insert(0, "Ascendant", [As], True) 
    # planet['Ascendant'] = As
    points = []
    # for zs in zodiac:
    #     if(angle >= zodiac[j][0] and angle < zodiac[j][1]):
    #             de = angle - zodiac[j][0]
    #             zz = zs 
    # points.append(['Ascendant', zz, de, 1, As])

    for i in planet:
        angle = planet[i][0]
        if angle>=360:
            angle = angle - 360
        d = 0
        h = '' 
        z = ''
        for j, k in zip(zodiac,house):
            if(angle >= zodiac[j][0] and angle < zodiac[j][1]):
                d = angle - zodiac[j][0]
                z = j
                
            if(angle >= house[k][0] and angle < house[k][1]):
                h = k
            elif(angle >= 330 or angle < 30):
                for q in house:
                    if house[q][0] >= 330 and house[q][1]<30:
                        h = q
                        break
        if( i == 'Ascendent'):
            h = 1
        points.append([i, z, d, h, angle])  
#     pointr = pd.DataFrame(points, columns=['point', 'zodiac', 'zodiac_longitude', 'house', 'RA'])
    aspect_report = []
    for i in range(len(Planet_names)):
        for j in range(i):
            if isinstance(grid[i][j], list):
                if(grid[i][j][1] == 'a'):
                    deg_type = 'Applying'
                else:
                    deg_type = 'Separating'
                aspect_report.append([Planet_names[i], Planet_names[j], grid[i][j][0], deg_type, grid[i][j][2]])
#     aspectr = pd.DataFrame(aspect_report, columns = ['body1', 'body2', 'shape', 'degree_type', 'degree'])
    return points,aspect_report



# # Main Func



def draw_chart(t, rows, tsp):

#     t, rows, tsp = get_angles()
    row = rows.loc[0]
    print('...1')
    image = copy.deepcopy(image_original)
    grid_image=copy.deepcopy(grid_original)
    
    inner_s = True
    # print(Planet_names)
    
    for i, j in zip(row, Planet_names) :
        inner_s = check_row(i, j, row)
        image = locate_arrow(i, image, p_name = j, inner = inner_s)
    print('...2')
    As, image = houses(image, t, tsp)
    print('...3')
    grid = aspect_grid(row, Planet_names)
    grid_image = draw_grid(row, grid, grid_image)
    print('...4')
    point, aspect = show_report(row, As, grid, t)  #As
    print('...5')
    cv.imwrite('media/natal_chart.jpg', image)
    cv.imwrite('media/aspect_grid.jpg', grid_image)
#     print(point)
#     print(aspect)
    return point, aspect

#     cv.imshow('Aspect_grid',grid_image)
#     cv.imshow('Natal_Chart', image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

