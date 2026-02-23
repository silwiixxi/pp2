#401
n = int(input())
def squares(num):
    for i in range(1, num + 1):
        yield i * i
for value in squares(n):
    print(value)

#402
import sys
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i
def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    n = int(data)
    first = True
    for x in even_numbers(n):
        if first:
            sys.stdout.write(str(x))
            first = False
        else:
            sys.stdout.write(',' + str(x))
    if not first:
        sys.stdout.write('\n')
if __name__ == "__main__":
    main()

#403
import sys
def divisible_by_4_and_6(n):
    for i in range(0, n + 1, 12):
        yield i
def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    n = int(data)
    first = True
    for x in divisible_by_4_and_6(n):
        if first:
            sys.stdout.write(str(x))
            first = False
        else:
            sys.stdout.write(' ' + str(x))
    if not first:
        sys.stdout.write('\n')
if __name__ == "__main__":
    main()

#404
a,b=map(int,input().split())
def squares(a,b):
    for i in range(a,b+1):
        yield i*i
for x in squares(a,b):
    print(x)

#405
n=int(input())
def countdown(n):
    for i in range(n,-1,-1):
        yield i
for x in countdown(n):
    print(x)

#406
n=int(input())
def fib(n):
    a,b=0,1
    for i in range(n):
        yield a
        a,b=b,a+b
print(",".join(str(x) for x in fib(n)))

#407
s=input()
class Reverse:
    def __init__(self,string):
        self.string=string
        self.index=len(string)
    def __iter__(self):
        return self
    def __next__(self):
        if self.index==0:
            raise StopIteration
        self.index-=1
        return self.string[self.index]
for c in Reverse(s):
    print(c,end="")

#408
n=int(input())
def primes(n):
    for i in range(2,n+1):
        for j in range(2,int(i**0.5)+1):
            if i%j==0:
                break
        else:
            yield i
print(*primes(n))

#409
n=int(input())
def powers_of_two(n):
    for i in range(n+1):
        yield 2**i
print(*powers_of_two(n))

#410
lst=input().split()
n=int(input())
def limited_cycle(lst,n):
    for _ in range(n):
        for x in lst:
            yield x
print(*limited_cycle(lst,n))

#411
import json
a=json.loads(input())
b=json.loads(input())
def patch(src,upd):
    for k,v in upd.items():
        if v is None:
            if k in src: del src[k]
        elif isinstance(v,dict) and isinstance(src.get(k),dict):
            patch(src[k],v)
        else:
            src[k]=v
patch(a,b)
print(json.dumps(a,sort_keys=True,separators=(',',':')))

#412
import json
a = json.loads(input())
b = json.loads(input())
res = []
def f(x, y, path=""):
    if type(x) == dict and type(y) == dict:
        for k in sorted(set(x) | set(y)):
            p = path + "." + k if path else k
            if k not in x:
                res.append((p, "<missing>", json.dumps(y[k], separators=(',', ':'))))
            elif k not in y:
                res.append((p, json.dumps(x[k], separators=(',', ':')), "<missing>"))
            else:
                f(x[k], y[k], p)
    else:
        if x != y:
            res.append((path,
                        json.dumps(x, separators=(',', ':')),
                        json.dumps(y, separators=(',', ':'))))
f(a, b)
if not res:
    print("No differences")
else:
    for p, old, new in sorted(res):
        print(p, ":", old, "->", new)

#413
import json,re
data=json.loads(input())
q=int(input())
for _ in range(q):
    path=input()
    cur=data
    try:
        parts=re.findall(r'\w+|\[\d+\]',path)
        for p in parts:
            if p.startswith('['):
                idx=int(p[1:-1])
                cur=cur[idx]
            else:
                cur=cur[p]
print(json.dumps(cur,separators=(',',':')))
    except:
        print("NOT_FOUND")

#414
import sys
from datetime import datetime, timedelta, timezone
def parse_moment(s):
    date_str, offset_str = s.strip().split()
    year, month, day = map(int, date_str.split('-'))
    sign = offset_str[3]
    hhmm = offset_str[4:]
    hh, mm = map(int, hhmm.split(':'))
    delta = timedelta(hours=hh, minutes=mm)
    if sign == '-':
        delta = -delta
    tz = timezone(delta)
    local = datetime(year, month, day, 0, 0, tzinfo=tz)
    return local.astimezone(timezone.utc)
def main():
    line1 = sys.stdin.readline()
    line2 = sys.stdin.readline()
    if not line1 or not line2:
        return
    utc1 = parse_moment(line1)
    utc2 = parse_moment(line2)
    diff = abs(utc1 - utc2).days
    print(diff)
if __name__ == "__main__":
    main()

#415
import sys
from datetime import datetime, timedelta, timezone
def parse_line(s):
    s = s.strip()
    date_part, tz_part = s.split()
    y, m, d = map(int, date_part.split("-"))
    sign = 1 if tz_part[3] == '+' else -1
    hh = int(tz_part[4:6])
    mm = int(tz_part[7:9])
    tz = timezone(sign * timedelta(hours=hh, minutes=mm))
    local_midnight = datetime(y, m, d, 0, 0, 0, tzinfo=tz)
    return y, m, d, tz, local_midnight.astimezone(timezone.utc)
def is_leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
def bday_utc(bm, bd, birth_tz, year):
    if bm == 2 and bd == 29 and not is_leap(year):
        bd = 28
    return datetime(year, bm, bd, 0, 0, 0, tzinfo=birth_tz).astimezone(timezone.utc)
lines = sys.stdin.read().strip().splitlines()
_, bm, bd, birth_tz, _ = parse_line(lines[0])
cy, _, _, _, curr_utc = parse_line(lines[1])
cand = bday_utc(bm, bd, birth_tz, cy)
if cand < curr_utc:
    cand = bday_utc(bm, bd, birth_tz, cy + 1)
delta = int((cand - curr_utc).total_seconds())
if delta <= 0:
    print(0)
else:
    print((delta + 86400 - 1) // 86400)

#416
from datetime import datetime,timezone,timedelta
def parse(s):
    dt_str,tz=s.rsplit(" ",1)
dt=datetime.strptime(dt_str,"%Y-%m-%d %H:%M:%S")
    sign=1 if tz[3]=="+" else -1
    h,m=map(int,tz[4:].split(":"))
tzinfo=timezone(timedelta(hours=sign*h,minutes=sign*m))
    return dt.replace(tzinfo=tzinfo)
start=parse(input())
end=parse(input())
delta=int((end.astimezone(timezone.utc)-start.astimezone(timezone.utc)).total_seconds())
print(delta)

#417
import math
r=float(input())
x1,y1=map(float,input().split())
x2,y2=map(float,input().split())
dx=x2-x1
dy=y2-y1
a=dx*dx+dy*dy
b=2*(dx*x1+dy*y1)
c=x1*x1+y1*y1-r*r
disc=b*b-4*a*c
if disc<=0:
    print("0.0000000000")
else:
    t1=(-b-math.sqrt(disc))/(2*a)
    t2=(-b+math.sqrt(disc))/(2*a)
    t_min=max(0,min(t1,t2))
    t_max=min(1,max(t1,t2))
    if t_max<=t_min:
        print("0.0000000000")
    else:
        x_start=x1+dx*t_min
        y_start=y1+dy*t_min
        x_end=x1+dx*t_max
        y_end=y1+dy*t_max
        length=math.hypot(x_end-x_start,y_end-y_start)
        print(f"{length:.10f}")

#418
import sys
def main():
    line1 = sys.stdin.readline().strip()
    line2 = sys.stdin.readline().strip()
    if not line1 or not line2:
        return
    x1, y1 = map(float, line1.split())
    x2, y2 = map(float, line2.split())
    x = (x1 * y2 + x2 * y1) / (y1 + y2)
    print(f"{x:.10f} 0.0000000000")
if __name__ == "__main__":
    main()

#419
import math
def solve():
    try:
        r = float(input().strip())
        x1, y1 = map(float, input().split())
        x2, y2 = map(float, input().split())
    except EOFError:
        return
    dist_oa = math.sqrt(x1**2 + y1**2)
    dist_ob = math.sqrt(x2**2 + y2**2)
    dist_ab = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dx, dy = x2 - x1, y2 - y1
    t = -(x1 * dx + y1 * dy) / (dx**2 + dy**2) if (dx**2 + dy**2) > 0 else 0
    t = max(0, min(1, t))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    dist_to_origin = math.sqrt(closest_x**2 + closest_y**2)
    if dist_to_origin >= r - 1e-9:
        print(f"{dist_ab:.10f}")
    else:
        l1 = math.sqrt(max(0, dist_oa**2 - r**2))
        l2 = math.sqrt(max(0, dist_ob**2 - r**2))
        dot_product = x1 * x2 + y1 * y2
        cos_theta = dot_product / (dist_oa * dist_ob)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        theta = math.acos(cos_theta)
        alpha1 = math.acos(r / dist_oa)
        alpha2 = math.acos(r / dist_ob)
        theta_arc = theta - alpha1 - alpha2
        total_path = l1 + l2 + (r * max(0, theta_arc))
        print(f"{total_path:.10f}")
if __name__ == "__main__":
    solve()

#420
g=0
def outer():
	n=0
	def inner(cmds):
		nonlocal n
		global g
		for scope,val in cmds:
			if scope=="global":
				g+=val
			elif scope=="nonlocal":
				n+=val
			else:
				x=val
		return n
	cmds=[]
	for _ in range(int(input())):
		s,v=input().split()
		cmds.append((s,int(v)))
	n=inner(cmds)
	return n
n=outer()
print(g,n)

#421
n=int(input())
for _ in range(n):
	mod,attr=input().split()
	try:
		m=__import__(mod)
		for part in mod.split(".")[1:]:
			m=getattr(m,part)
	except:
print("MODULE_NOT_FOUND")
		continue
	if not hasattr(m,attr):
print("ATTRIBUTE_NOT_FOUND")
	elif callable(getattr(m,attr)):
		print("CALLABLE")
	else:
		print("VALUE")