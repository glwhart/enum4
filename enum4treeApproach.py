#!/usr/local/bin/python3
# This version of the program tries to solve the "surjective enumeration" problem with the order of
# the loops reversed from what we first envisioned. The inner loop will be over colors (traversing
# up and down the "tree") the outer loop will be over configurations for each color.
import sys
from tree import Tree
from msgenum3 import integer2coloring, coloring2integer, grouper

### Could we make some headway on the restricted site problem (at least for spectators) by using
### groups that skipped those sites (left them unchanged)?

colors = [2,2,2,2,2,2] # Number of each color in the list
colors = [4,4,4]
t = Tree(colors)

### Construct the cyclic permutation group of order n
# Set up an empty list of lists to store the stabilizers in
G = [[] for ilc in range(t.k)]

# List the generators
#generators = [[1,2,0,4,5,3,7,8,6],[3,1,2,6,4,5,0,7,8],[1,0,2,3,4,5,6,7,8]]
#generators = [[2,3,4,5,1,7,8,9,10,6],[2,1,3,4,5,7,6,8,9,10]]
#generators = [[j -1 for j in i] for i in [[2,3,4,1,5,6,7,8],[2,1,3,4,5,6,7,8],[1,2,3,4,6,7,8,5],[1,2,3,4,6,5,7,8]]]
generators = [[j -1 for j in i] for i in [[2,1,4,3,5,6,7,8,9,10,11,12],[4,3,2,1,5,6,7,8,9,10,11,12],[1,2,3,4,6,7,8,5,9,10,11,12],[1,2,3,4,6,5,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,10,11,9,12],[1,2,3,4,5,6,7,8,9,11,12,10]]]
#generators = [[j -1 for j in i] for i in [[2,3,4,5,1,7,8,9,10,6],[2,1,3,4,5,7,6,8,9,10]]]
# Generate the group from the generators
###[G[0].append(i) for i in generators]
####[G[0].append(i) for i in [[2,3,4,5,6,7,0,1],[2,3,0,1,4,5,6,7]]]
####[G[0].append(i) for i in [[1,2,3,4,0,6,7,8,9 ,5],[1,0,2,3,4,6,5,7,8,9 ]]] 
####G[0].append([(i+1)%t.n for i in range(t.n)])
###growing = True
###while growing:
###    growing = False
###    nG = len(G[0])
###    # Loop over each possible pair of group elements to see if they create a new element
###    for iG in G[0][:nG]:
###        for jG in G[0][:nG]:
###            g = [iG[i] for i in jG]
###            if not g in G[0]:
###                G[0].append(g)
###                growing = True
###g = len(G[0])
G[0] = grouper(generators)
print("Size of group:",len(G[0]))

survivors = []
t.increment_location(G)
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
        t.increment_location(G)
                                                  
# Print out the surviving labelings
for i,iSurv in enumerate(survivors):
    print("%s"%iSurv[:t.k-1],)
    if i < len(survivors) -1:
        if survivors[i][0] != survivors[i+1][0]:
            print ()

print( "\n")
print( "Size of group",g)
print( "number of survivors:",len(survivors))

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

textdict = {"ha" :"center",
            "va" : "center",
            "size" : 12,
            "fontname" : "Arial",
            "zorder" : 1}

pink = [1,.7,.7]
lightblue = [.8,.9,1]
lightgray = [.9,.9,.9]
darkgray = [.7,.7,.7]

xoffset = 10
radius = 10
xspacing = 2*radius*1.2
colors = {1:"red", 2:"yellow", 3:"green", 4:"blue", 5:"white", 6:"black", 7:"purple", 0:"cyan"}
yspacing = 2*radius*1.4
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
        
    for i in range(t.n):
        fc = colors[labeling[i]]
        p = matplotlib.patches.Circle([i*xspacing+xiter,yiter],radius,fc=fc,ec=[0.5,0.5,0.5],linewidth=.1,zorder=0)
        c.add_patch(p)
    c.text(xiter-xspacing,yiter,str(j+1),**textdict)

cfig.savefig("perms.pdf",bbox_inches="tight")
