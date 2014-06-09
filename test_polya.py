#!/usr/local/bin/python3
from msgenum3 import *

colors = [6,3,3]
generators = [[j -1 for j in i] for i in
              [[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12],[1,2,3,4,6,7,8,5,9,10,11,12],[1,2,3,4,6,5,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,10,11,9,12],[1,2,3,4,5,6,7,8,9,11,12,10]]]
#generators = [[j -1 for j in i] for i in
#              [[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12]]]
#generators =  [[j -1 for j in i] for i
#               in [[2,3,4,1,5,6,7,8],[2,1,3,4,5,6,7,8],[1,2,3,4,6,5,8,7],[1,2,3,4,6,7,5,8]]]
generators = [[j -1 for j in i] for i in
[[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,
11,12],[1,2,3,4,6,7,8,5,9,10,11,12],[1,2,3,4,6,5,7,8,9,10,11,12],
[1,2,3,4,5,6,7,8,10,11,9,12],[1,2,3,4,5,6,7,8,9,11,12,10]]]
#[[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12],[1,2,3,4,6,5,8,7,9,10,11,12],[1,2,3,4,8,7,6,5,9,10,11,12],
#[1,2,3,4,5,6,7,8,10,9,11,12],[1,2,3,4,5,6,7,8,10,11,12,9]]]
#[[2,3,4,5,1,7,8,9,10,6],[2,1,3,4,5,7,6,8,9,10]]]
print("Finding the group")
G = grouper(generators)
print("Size of group:",len(G))
print("Sum of colors:",sum(colors))
print("Perm length:",len(G[0]))

if sum(colors) != len(G[0]):
    print("argh")
    sys.exit()

# Get the cycle lengths for each permutation in the group G
cycles = {}
for g in G:
    c = str(cycle_counter(g))
    if c in cycles:
        cycles[c] += 1
    else:
        cycles[c] = 1
for c,v in enumerate(cycles):
    print(cycles[v],v, c)

total = 0
for i in cycles:
    v = eval(i)
    fitTimes = partition_cycles_into_color_vector(colors,v)
    total += fitTimes*cycles[i]
    print(i,fitTimes,cycles[i]) 

print(total/len(G))
