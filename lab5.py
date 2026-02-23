#501
import re
s=input()
if re.match(r'Hello',s):
    print("Yes")
else:
    print("No")

#502
import re
s=input()
sub=input()
if re.search(re.escape(sub),s):
    print("Yes")
else:
    print("No")

#503
import re
s=input()
p=input()
print(len(re.findall(re.escape(p),s)))

#504
import re
s=input()
print(*re.findall(r'\d',s))

#505
import re
s=input()
if re.match(r'^[A-Za-z].*\d$',s):
    print("Yes")
else:
    print("No")

#506
import re
s=input()
m=re.search(r'\S+@\S+\.\S+',s)
print(m.group() if m else "No email")

#507
import re
s=input()
p=input()
r=input()
print(re.sub(re.escape(p),r,s))

#508
import re
s=input()
pattern=input()
print(*re.split(pattern,s),sep=",")

#509
import re
s=input()
print(len(re.findall(r'\b\w{3}\b',s)))

#510
import re
s=input()
print("Yes" if re.search(r'cat|dog',s) else "No")

#511
import re
s=input()
print(len(re.findall(r'[A-Z]',s)))

#512
import re
s=input()
print(*re.findall(r'\d{2,}',s))

#513
import re
s=input()
print(len(re.findall(r'\w+',s)))

#514
import re
s=input()
pattern=re.compile(r'^\d+$')
print("Match" if pattern.fullmatch(s) else "No match")

#515
import re
s=input()
print(re.sub(r'\d', lambda m: m.group()*2, s))

#516
import re
s=input()
m=re.match(r'Name: (.+), Age: (.+)',s)
print(m.group(1),m.group(2))

#517
import re
s=input()
print(len(re.findall(r'\b\d{2}/\d{2}/\d{4}\b',s)))

#518
import re
import sys
try:
    s = sys.stdin.readline().rstrip('\n')
    p = sys.stdin.readline().rstrip('\n')
except:
    pass
escaped_pattern = re.escape(p)
matches = re.findall(escaped_pattern, s)
count = len(matches)
print(count)

#519
import re
s=input()
pattern=re.compile(r'\b\w+\b')
print(len(pattern.findall(s)))