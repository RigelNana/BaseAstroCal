
import math
from math import sin,cos,asin
import datetime
import sympy as sp
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
'''
def HourMinuteSecond(minute):
    h = minute//60
    h1 = minute/60
    m = (h1-h)*60
    m1 = int(m)
    s = (m-m1)*60
    if(m>=10 and s>=10):
        return  str(int(h))+':'+str(int(m))+':'+str(s)
    elif (m<=10 and s>=10):
        return  str(int(h))+':0'+str(int(m))+':'+str(s)
    elif (m>=10 and s<=10):
        return  str(int(h))+':'+str(int(m))+':0'+str(s)
    else:
        return  str(int(h))+':0'+str(int(m))+':0'+str(s)
'''

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
    h = math.floor(time);
    min = math.floor(60.0*frac(time));
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
    p4 = round(result[1],8)
    
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
except TypeError:
    print('请检查您的输入是否正确')

dts2 = datetime.datetime.now().timestamp()
print('所花时间:'+str(dts2-dts))