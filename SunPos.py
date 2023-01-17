import math
from math import sin, cos, asin, atan2, floor, degrees, radians
import datetime
dt = datetime.datetime.now()
dts = dt.timestamp()
utctm = datetime.datetime.utcfromtimestamp(dts)
ut = utctm.hour + utctm.minute/60 + utctm.second/3600


def JulDay(d, m, y, u):
    if m <= 2:
        m = m+12
        y = y-1
    A = floor(y/100)
    JD = floor(365.25*(y+4716)) + int(30.6001*(m+1)) + \
        d - 13 - 1524.5 + u/24.0
    return JD


def calT(JDE):
    T = (JDE-2451545)/36525
    return T

#力学时
jd = JulDay(utctm.day, utctm.month, utctm.year, ut)
T_A = calT(jd)

#太阳平黄经
L0 = 280.46645 + 36000.76983*T_A + 0.0003032*(T_A**2)
if L0 > 360:
    L0 -= floor(L0/360)*360
elif L0 < 0:
    L0 += abs(floor(L0/360))*360
#太阳平近点角
M = 357.52910 + 35999.05030*T_A - 0.0001559*(T_A**2)-0.00000048*(T_A**3)
if M > 360:
    M -= floor(M/360)*360
elif M < 0:
    M += abs(floor(M/360))*360
#地球轨道离心率
e = 0.016708617 - 0.000042037*T_A - 0.0000001236*(T_A**2)
#太阳中心差
C = (1.914600 - 0.004817*T_A - 0.000014*(T_A**2)) * (sin(radians(M))) + \
    ((0.019993 - 0.000101*T_A) * sin(2*radians(M))) + (0.000290*sin(3*radians(M)))
#真黄经
THETA = C+L0
#真近点角
v = M + C
#地日距离
R = 1.000001018*(1-e**2) / (1+e*cos(v))
#章动修正、光行差修正
OMEGA = 125.04 - 1934.136*T_A
#视黄经
THETA_A = THETA - 0.00569 - 0.00478*sin(OMEGA)


U = T_A/100
#真黄赤交角
EPSILON = 23.43929111-1.3002583*U-1.55*(U**2) + 1999.25*(U**3) - 51.38*(U**4) - 249.67*(
    U**5) - 39.05*(U**6) + 7.12*(U**7) + 27.87*(U**8) + 5.79*(U**9) + 2.45*(U**10)
#J2000坐标系下的黄经
THETA_2000 = THETA-0.01397*(utctm.year-2000)

#太阳赤经（度）
alpha = degrees(atan2(cos(radians(EPSILON)) *
                      sin(radians(THETA)), cos(radians(THETA))))
if alpha < 0:
    alpha += 360
#太阳赤经（时）
alpha /= 15
#太阳赤纬
delta = degrees(asin(sin(radians(EPSILON))*sin(radians(THETA))))

print("太阳赤经:"+str(alpha), "太阳赤纬:"+str(delta),
      '\n'+"地日距离:"+str(R)+"au", "现黄赤交角:"+str(EPSILON))
