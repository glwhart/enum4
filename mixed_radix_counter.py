#!/usr/bin/python
colors = [4,2,2]
n = len(colors)
limit = [ilc-1 for ilc in colors]
config = [0]*n
print config
while config != limit:
    j = n - 1
    while True:
        if config[j] != colors[j]-1: break
        config[j] = 0
        j -= 1
        if (j < 0): break
    if (j < 0): break
    config[j] = config[j] + 1
    print config,"wheel",j
    
    
