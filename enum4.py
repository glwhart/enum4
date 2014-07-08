#!/usr/local/bin/python3
# This version of the program tries to solve the "surjective enumeration" problem with the order of
# the loops reversed from what we first envisioned. The inner loop will be over colors (traversing
# up and down the "tree") the outer loop will be over configurations for each color. This
# eliminatates the need for a complicated data structure for lists of hash tables

import sys
from tree import Tree
from msgenum3 import *
import time

### Could we make some headway on the restricted site problem (at least for spectators) by using
### groups that skipped those sites (left them unchanged)?


# List the generators
#generators =
generators = [[j -1 for j in i] for i in
 [[2,3,4,5,1,7,8,9,10,6],[2,1,3,4,5,7,6,8,9,10]]]
# [[2,3,4,1,5,6,7,8],[2,1,3,4,5,6,7,8],[1,2,3,4,6,7,8,5],[1,2,3,4,6,5,7,8]]]
#generators = [[2,3,4,5,6,7,8,9,0,1],[2,3,0,1,4,5,6,7,8,9]]
#generators = [[j -1 for j in i] for i in 
#[[2,3,4,5,6,7,1,8,9,10,11,12,13,14,15,16,17,18,19,20],[1,2,3,4,5,6,7,9,10,11,12,13,14,8,15,16,17,18,19,20],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,15,18,19,20],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,18]]]
#[[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12],[1,2,3,4,6,7,8,5,9,10,11,12],[1,2,3,4,6,5,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,10,11,9,12],[1,2,3,4,5,6,7,8,9,11,12,10]]]
#[[2,3,4,5,6,7,8,9,10,11,12,1],[7,2,3,4,5,6,1,8,9,10,11,12]]]
#[[2,3,4,1,5,6,7,8,9,10,11,12,13,14,15,16],[1,2,3,4,6,7,8,5,9,10, 11,12,13,14,15,16],[1,2,3,4,5,6,7,8,10,11,12,9,13,14,15,16],[1,2,3, 4,5,6,7,8,9,10,11,12,14,15,16,13]]]
colors = [2,2,2,2,2]
t = Tree(colors)
### Construct the cyclic permutation group of order n
# Set up an empty list of lists to store the stabilizers in
G = [[] for ilc in range(t.k)]

G[0] = grouper(generators)
nG = len(G[0])
print("Size of group:",nG)
#for g in G[0]:
#    print(" ".join('{}'.format(i+1) for i in g))
#sys.exit()
polya = polya_count(G[0],colors)

print("Number expected according to Polya counting theorem",polya)
survivors = []
t.increment_location(G)

f = open("timing.data","w+")
while t.loc != [-1]*t.k:
    # Construct the current labeling, all colors up to this depth
    labeling = t.coloring
    # Apply the permutations to the labeling, check index of each whether
    # idx < cIdx. If so, current coloring is a symmetric duplicate
    # Also collect the stabilizer while iterating over the group
    # elements

    for ig in G[t.depth]: # Loop over each element in the group (or the stabilizer)
        rlabeling = [labeling[ilc] for ilc in ig]
        # Now we need to reduce the coloring to zeros and current color only so that we can use the
        # coloring2integer routine
        if rlabeling == labeling: # current group operation is a member of the stabilizer
            G[t.depth+1].append(ig) # Add this group element to the stabilizer for the next depth
        short = []
        for i in rlabeling:
            if i==t.depth+1: # i.e., the current color
                short.append(1)
            elif i==0:
                short.append(0)
        rIdx = coloring2integer(short) # Index of "rotated" coloring       
        if rIdx < t.ccIdx: # Then we've hit this coloring before. Exit.
            # If you hit a duplicate, you want to go to the next branch *without*
            # incrementing. Incrementing may take you _down_ the tree, but you want to do across in
            # every case if you find a duplicate coloring. The problem with using the increment
            # function is that it always goes down if it can.
            t.next_branch(G)
            break
    else: # This is a surviving coloring. If we are at the bottom of the tree, then it is a complete
          # labeling and should be added to the survivor list.
        if t.depth == t.k-2: # Add current coloring to the surivor list.
            survivors.append(t.loc[:])
            #f.write(str(t.loc[:])+" "+str(time.perf_counter()-start)+" "+str(time.perf_counter()-start1)+"\n")
            #start = time.perf_counter()
        t.increment_location(G)
                                                  
# Print out the surviving labelings
#for i,iSurv in enumerate(survivors):
#    print("%s"%iSurv[:t.k-1],)
#    if i < len(survivors) -1:
#        if survivors[i][0] != survivors[i+1][0]:
#            print ()

print( "\n")
print( "Size of group",nG)
print("Number of survivors:  ",len(survivors))
print("Number Polya expected:",polya)
if polya != len(survivors):
    sys.exit("ERROR: Number of survivors differs from Polya counting")

sys.exit()
#--------------------------------------------------------------------------------
# Make a picture of the colorings and store it in a pdf file
import matplotlib
import matplotlib.pyplot

cfig = matplotlib.pyplot.figure(figsize=[8.5,11])
matplotlib.pyplot.subplots_adjust(left=0.001,right=.999,top=.999,bottom=.001)
c = cfig.add_subplot(111)
c.set_xlim([0,1000])
c.set_ylim([0,1000])
c.invert_yaxis()
c.set_axis_off() # This gets rid of the coordinate ax
c.set_aspect("equal")

textdict = {"ha" :"right",
            "va" : "bottom",
            "size" : 12,
            "fontname" : "Arial",
            "zorder" : 1}

pink = [1,.7,.7]
lightblue = [.8,.9,1]
lightgray = [.9,.9,.9]
darkgray = [.7,.7,.7]

xoffset = 10
xspacing = 10
radius = xspacing*.7
height = 20
colors = {1:"red", 2:"yellow", 3:"green", 4:"blue", 5:"white", 6:"black", 7:"purple", 0:"cyan"}
yspacing = 3*radius*1.4
yoffset = 10
yiter = yoffset
xiter = xoffset
for j,iSurv in enumerate(survivors):
    t.loc = iSurv
    labeling = t.coloring
    if yiter > 950:
        yiter -= 33*yspacing
        xiter += xspacing*t.n+5*xoffset
    else:
        yiter += yspacing
#    print(xiter,yiter)    
    for i in range(t.n):
        fc = colors[labeling[i]]
        p = matplotlib.patches.Rectangle([i*xspacing+xiter,yiter],radius,height,angle=0,fc=fc,ec=[0.5,0.5,0.5],linewidth=.1,zorder=0,clip_on=False)
        c.add_patch(p)
    c.text(xiter-xspacing,yiter,str(j+1),**textdict)

cfig.savefig("perms.pdf",bbox_inches="tight")
