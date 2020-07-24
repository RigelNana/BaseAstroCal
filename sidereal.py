# 0赤经0赤纬 单解 修
# 方位角180度时会变成0度
import math
from math import sin, cos, asin, atan2, floor, degrees, radians
import datetime

dt=datetime.datetime.now()
dts = dt.timestamp()
utctm = datetime.datetime.utcfromtimestamp(dts)
ut = utctm.hour + utctm.minute/60 + utctm.second/3600
day = int(input('请输入日\n'))
month = int(input('请输入月\n'))
year = int(input('请输入年\n'))
hour = float(input('请输入小时（ps:要纯小时格式，把分钟和秒化成小数\n这是utc时间，在北京时间的基础上减8即可)\n'))


def JulDay(d,m,y,u):
    if m <= 2:
        m = m+12
        y = y-1
    A = math.floor(y/100)
    JD =  math.floor(365.25*(y+4716)) + int(30.6001*(m+1)) + d - 13 - 1524.5 + u/24.0;
    return JD
jd = JulDay(day,month,year,hour)
#jd = JulDay(utctm.day,utctm.month,utctm.year,ut)

#此处可以稍加变换，算其他天
def GM_Sidereal_Time():
    MJD = jd - 2400000.5
    MJD0 = math.floor(MJD)
    ut0 = (MJD - MJD0)*24.0
    t_eph  = (MJD0-51544.5)/36525.0
    return  6.697374558 + 1.0027379093*ut0 + (8640184.812866 + (0.093104 - 0.0000062*t_eph)*t_eph)*t_eph/3600.0
def calT(JDE):
    T = (JDE-2451545)/36525
    return T

def SunPos():
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
    R = 1.000001018*(1-e**2) / (1+e*cos(radians(v)))
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

    return alpha,delta,EPSILON,R,THETA
def frac(X):
    X = X - math.floor(X)
    if (X<0):
        X = X + 1.0
    return X

def LM_Sidereal_Time(longitude):
    GMST = GM_Sidereal_Time()
    LMST =  24.0*frac((GMST + longitude/15.0)/24.0)
    return HoursMinutesSeconds(LMST)

def LM_Sidereal_Time_Numeric(longitude):
    GMST = GM_Sidereal_Time()
    LMST =  24.0*frac((GMST + longitude/15.0)/24.0)
    return LMST

def HoursMinutesSeconds(time):
    h = math.floor(time)
    min = math.floor(60.0*frac(time))
    secs = (60.0*(60.0*frac(time)-min))

    if (min>=10): 
        String=str(h)+':'+str(min)
    else:
        String=str(h)+':0'+str(min)
    if (secs<10):
        String = String + ':0'+str(secs)
    else:
        String = String + ':'+str(secs)
    return String

def Hour_Angle(alpha,longitude):
    if LM_Sidereal_Time_Numeric(longitude) - alpha < 0:
        return LM_Sidereal_Time_Numeric(longitude) - alpha+24
    elif LM_Sidereal_Time_Numeric(longitude) - alpha > 24:
        return LM_Sidereal_Time_Numeric(longitude) - alpha-24
    else:
        return LM_Sidereal_Time_Numeric(longitude) - alpha


    

def CalVerticalAngle(lat,dec,ha):
    sina = sin(math.radians(lat))*sin(math.radians(dec))+cos(math.radians(lat))*cos(math.radians(dec))*cos(math.radians(ha))
    verang = asin(sina)/math.pi*180
    return verang

def Hour_Angle_Degree(alpha,longitude):
    if Hour_Angle(alpha,longitude)*60>=360:
        return Hour_Angle(alpha,longitude)*15-360
    else:
        return Hour_Angle(alpha,longitude)*15


def Azimuth(lat,dec,ha,vt):
    
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    cosA = (sp.sin(math.radians(lat))*sp.sin(math.radians(vt))-sp.sin(math.radians(dec)))/(sp.cos(math.radians(lat))*cos(math.radians(vt)))
    #print(cosA)
    result = sp.solve(sp.cos(x)-cosA,x)
    #print(result)
    sinA = (sp.cos(math.radians(dec))*sp.sin(math.radians(ha)))/sp.cos(math.radians(vt))
    result2 = sp.solve(sp.sin(y)-sinA,y)
    #print(result2)
    p1 = round(result[0],8)
    p2 = round(result[1],8)
    p3 = round(result2[0],8)
    p4 = round(result2[1],8)
    
    if(p1 == p2 or p1 == p3 or p1 == p4):
        f = math.degrees(p1)
        if(f>=180):
            f = f-180
        else:
            f = f+180
        return f
    elif(p2==p3 or p2==p4):
        f = math.degrees(p2)
        if(f>=180):
            f = f-180
        else:
            f = f+180
        return f
        
    else:
        f = math.degrees(p3)
        if(f>=180):
            f = f-180
        else:
            f = f+180
        return f
        


    
try:
    longi = float(input('请输入您的经度\n'))
    lati = float(input('请输入您的纬度\n'))
    ra = float(input('请输入所求恒星的赤经\n'))
    dec = float(input('请输入所求恒星的赤纬\n'))
    dts3 = datetime.datetime.now().timestamp()
    print('\n')
    print('------------made by 5LaaLi------------')
    print('儒略日:'+str(jd))
    print('地方恒星时:'+LM_Sidereal_Time(longi))
    print('时角:'+str(Hour_Angle(ra,longi)))
    print('高度角:'+str(CalVerticalAngle(lati,dec,Hour_Angle_Degree(ra,longi))))
    print('方位角:'+str(Azimuth(lati,dec,Hour_Angle_Degree(ra,longi),CalVerticalAngle(lati,dec,Hour_Angle_Degree(ra,longi)))))
    print('太阳高度角:'+str(CalVerticalAngle(lati,SunPos()[1],Hour_Angle_Degree(SunPos()[0],longi))))
    print('太阳方位角:'+str(Azimuth(lati,SunPos()[1],Hour_Angle_Degree(SunPos()[0],longi),CalVerticalAngle(lati,SunPos()[1],Hour_Angle_Degree(SunPos()[0],longi)))))
    print('黄赤交角:'+str(SunPos()[2]))
    print('地日距离:'+str(SunPos()[3]*149597870)+'km')
    print('太阳黄经:'+str(SunPos()[4]))
except TypeError:
    print('请检查您的输入是否正确')

dts2 = datetime.datetime.now().timestamp()
print('所花时间:'+str(dts2-dts))