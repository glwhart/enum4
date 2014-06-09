#!/usr/local/bin/python3
from msgenum3 import *

colors = [3,3,3,3]
generators = [[j -1 for j in i] for i in
              [[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12],[1,2,3,4,6,7,8,5,9,10,11,12]]]

#,[1,2,3,4,6,5,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,10,11,9,12],[1,2,3,4,5,6,7,8,9,11,12,10]]]
G = grouper(generators)
print("Size of group:",len(G))


if sum(colors) != len(G[0]):
    print("argh")

cycles = {}
for g in G:
    c = str(cycle_counter(g))
    if c in cycles:
        cycles[c] += 1
    else:
        cycles[c] = 1
for c,v in enumerate(cycles):
    print(cycles[c],v, c)
