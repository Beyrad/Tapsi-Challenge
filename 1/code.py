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

epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
n = int(input())

#Inputing Data
reps = []
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

    near = getNear(x, y)
    r = Report(near[2], near[3], sec, near[0])
    reps.append(r)

#Grouping Reports
c = 0
k = len(reps)
label = [0] * k
group = []
for i in range(k):
    cool = 0
    for j in range(i):
        if (D(reps[i].x, reps[i].y, reps[j].x, reps[j].y) <= 450):
            label[i] = label[j]
            group[label[i]].append(i)           
            cool = 1 
            break
    if cool == 0:
        group.append([])
        label[i] = c
        group[label[i]].append(i)
        c += 1
    

#Finding best answer in each group
for G in group:
    cnt = {}
    mx = 0
    best = ""
    for i in G:
        R = reps[i]
        if R.name in cnt:
            cnt[R.name] += 1
        else:
            cnt[R.name] = 1
            
        if (cnt[R.name] >= mx):
            mx = cnt[R.name]
            best = R.name

    sumX = 0.0
    sumY = 0.0
    for i in G:
        R = reps[i]
        if (R.name == best):
            sumX += R.x
            sumY += R.y
    
    sumX /= float(mx)
    sumY /= float(mx)
    L = getNear(sumX, sumY)
    X = L[2]
    Y = L[3]
    print(X, Y)


