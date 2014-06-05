#!/usr/bin/python
# Generate the entire group from the generators
G = [[2,3,4,5,6,7,0,1],[2,3,0,1,4,5,6,7]]
growing = True
while growing:
    growing = False
    nG = len(G)
    for iG in G[:nG]:
        for jG in G[:nG]:
            g = [iG[i] for i in jG]
            if not g in G:
                G.append(g)
                growing = True
print len(G)
