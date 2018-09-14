s = '12345678904'
o = []
while s:
    o.append(s[:5])
    s = s[5:]
print(o)