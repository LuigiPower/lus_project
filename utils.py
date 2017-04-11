import math

def calc_weights(wdic, cdic, call):
    for k, v in cdic.items():
        vals = k.split()
        target = vals[-1]
        c1 = v
        c2 = call[target]
        p = -math.log(c1/c2)
        wdic[k] = p

def inc(dic, key):
    if key not in dic:
        dic[key] = 1
    else:
        dic[key] += 1

