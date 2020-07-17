import math
from math import sin,cos,asin
import datetime
import sympy as sp

class calsk():
    def nowtime(self):
        dt=datetime.datetime.now()
        dts = dt.timestamp()
        utctm = datetime.datetime.utcfromtimestamp(dts)
        ut = utctm.hour + utctm.minute/60 + utctm.second/3600
        return utctm.day,utctm.month,utctm.year,ut
    def JulDay(self,d,m,y,u):
        if m <= 2:
            m = m+12
            y = y-1
        A = math.floor(y/100)
        JD =  math.floor(365.25*(y+4716)) + int(30.6001*(m+1)) + d - 13 - 1524.5 + u/24.0
        return JD

    jd = 0
    def setdate(self,day,month,year,hour):
        self.jd = JulDay(day,month,year,hour)
        
#jd = JulDay(utctm.day,utctm.month,utctm.year,ut)

#此处可以稍加变换，算其他天
    def GM_Sidereal_Time(self,jd):
        MJD = jd - 2400000.5
        MJD0 = math.floor(MJD)
        ut0 = (MJD - MJD0)*24.0
        t_eph  = (MJD0-51544.5)/36525.0
        return  6.697374558 + 1.0027379093*ut0 + (8640184.812866 + (0.093104 - 0.0000062*t_eph)*t_eph)*t_eph/3600.0


    def frac(self,X):
        X = X - math.floor(X)
        if (X<0):
            X = X + 1.0
        return X

    def LM_Sidereal_Time(self,longitude,jd):
        GMST = GM_Sidereal_Time(jd)
        LMST =  24.0*frac((GMST + longitude/15.0)/24.0)
        return HoursMinutesSeconds(LMST)

    def LM_Sidereal_Time_Numeric(self,longitude,jd):
        GMST = GM_Sidereal_Time(jd)
        LMST =  24.0*frac((GMST + longitude/15.0)/24.0)
        return LMST

    def HoursMinutesSeconds(self,time):
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

    def Hour_Angle(self,alpha,longitude,jd):
        if LM_Sidereal_Time_Numeric(longitude,jd) - alpha < 0:
            return LM_Sidereal_Time_Numeric(longitude,jd) - alpha+24
        elif LM_Sidereal_Time_Numeric(longitude,jd) - alpha > 24:
            return LM_Sidereal_Time_Numeric(longitude,jd) - alpha-24
        else:
            return LM_Sidereal_Time_Numeric(longitude,jd) - alpha


    

    def CalVerticalAngle(self,lat,dec,ha):
        sina = sin(math.radians(lat))*sin(math.radians(dec))+cos(math.radians(lat))*cos(math.radians(dec))*cos(math.radians(ha))
        verang = asin(sina)/math.pi*180
        return verang

    def Hour_Angle_Degree(self,alpha,longitude,jd):
        if Hour_Angle(alpha,longitude,jd)*60>=360:
            return Hour_Angle(alpha,longitude,jd)*15-360
        else:
            return Hour_Angle(alpha,longitude,jd)*15


    def Azimuth(self,lat,dec,ha,vt):
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