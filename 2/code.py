import requests as req
from geopy.distance import geodesic as Geo
from datetime import datetime, timezone, timedelta

"""returns the list containing data of nearest road"""
"""ans = [Name, Distance, X, Y]"""
def getNear(x, y):
    url = f'http://0.0.0.0:5000/nearest/v1/driving/{x},{y}'
    params = {
        'number': '1'
    }
    res = req.get(url, params=params)
    ans = [0, 0, 0, 0] #(name, dis, x, y)
    if res.status_code == 200:
        data = res.json()
        ans[0] = data['waypoints'][0]['name']
        ans[1] = data['waypoints'][0]['distance']
        ans[2] = data['waypoints'][0]['location'][0]
        ans[3] = data['waypoints'][0]['location'][1]
    else:
        print("Error")
    return ans

"""returns distance of two location points"""
#change it to adopt to The Haversine Formula
def D(x1, y1, x2, y2):
    p1 = (x1, y1)
    p2 = (x2, y2)
    return Geo(p1, p2).meters


class Report:
    def __init__(self, x, y, sec, name):
        self.x = x
        self.y = y
        self.time = sec
        self.name = name

    def Loc(self):
        return (self.x, self.y)

class Police:
    def __init__(self, x, y, lastSeen, data, alive):
        self.x = x
        self.y = y
        self.lastSeen = lastSeen
        self.data = data
        self.alive = alive

    def Update(self):
        mx = 0
        best = ""
        for name, (cnt, sumX, sumY) in self.data.items():
            if cnt >= mx:
                mx = cnt
                best = name
        
        X = self.data[best][1] / float(mx)
        Y = self.data[best][2] / float(mx)
        L = getNear(x, y)
        if (self.x != L[2] or self.y != L[3]):
            self.x = L[2]
            self.y = L[3]
            return 1
        return 0
        



epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
target_timezone = timezone(timedelta(hours=3, minutes=30))
n = int(input())

P = []
for i in range(n):
    x, y, tm = input().split(',')
    x = float(x)
    y = float(y)
    x, y = y, x
    tm = tm[:-1]
    tm = tm[1:]
    tm_obj = datetime.fromisoformat(tm)
    tm_obj_utc = tm_obj.astimezone(timezone.utc)
    sec = int((tm_obj_utc - epoch).total_seconds())

    canPrint = 0
    for pol in P:
        if pol.alive and abs(pol.lastSeen - sec) > 3601:
             pol.alive = 0
             canPrint = 1

    near = getNear(x, y)
    r = Report(near[2], near[3], sec, near[0])
    #r.x, r.y, r.name, r.sec this is after near query
    cool = 0
    for pol in P:
        if (pol.alive and D(pol.x, pol.y, r.x, r.y) <= 450):
            if r.name not in pol.data:
                pol.data[r.name] = (1, r.x, r.y)
            else:
                F = pol.data[r.name]
                pol.data[r.name] = (F[0] + 1, F[1] + r.x, F[2] + r.y)
            
            pol.lastSeen = r.time
            canPrint |= pol.Update()
            cool = 1
            break
    
    
    if (not cool):
        pol = Police(r.x, r.y, r.time, {r.name: (1, r.x, r.y)}, True)
        P.append(pol)
        canPrint = 1


    if (canPrint):
        time_obj_utc = epoch + timedelta(seconds=sec)
        time_obj_local = time_obj_utc.astimezone(target_timezone)
        iso_format_str = time_obj_local.isoformat()
        print(f"{iso_format_str}")

        ans = []
        for pol in P:
            if pol.alive:
                ans.append((pol.x, pol.y))

        print(len(ans))
        for X, Y in ans:
            print(f"{Y}, {X}")
        print("------------------------------------------")
        print("------------------------------------------")

        
    