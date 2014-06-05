#!/usr/bin/python
# This version of the program tries to solve the "surjective enumeration" problem with the order of
# the loops reversed from what we first envisioned. The inner loop will be over colors (traversing
# up and down the "tree") the outer loop will be over configurations for each color.
import sys
#from tree import Tree
from msgenum import integer2coloring, coloring2integer, choose

colors = [4,2,2] # Number of each color in the list
n = sum(colors) # n is the total number of slots in the labelings
k = len(colors) # k is the number of different colors in each labeling

# Make an empty list of groups, one list for each color
G = [[] for ilc in range(k)]

[G[0].append(i) for i in [[2,3,4,5,6,7,0,1],[2,3,0,1,4,5,6,7]]]
#G[0].append([(i+1)%t.n for i in range(t.n)])
growing = True
while growing:
    growing = False
    nG = len(G[0])
    for iG in G[0][:nG]:
        for jG in G[0][:nG]:
            g = [iG[i] for i in jG]
            if not g in G[0]:
                G[0].append(g)
                growing = True

survivors = []
loc = [0]*k
limit = [choose(sum(colors[ilc:]),colors[ilc]) for ilc in range(len(colors))]
ic = 0
nc = reduce(lambda x,y:x*y, limit)
print "limit",limit
while loc != limit and ic < nc:
    ic += 1
    j = k - 1 # j is the digit pointer indicating which wheel is turning (that is, it indicates the
    # active color). It always starts at the far right.
 
    # Construct the current labeling, all colors up to this depth
    labeling = [0]*n
    for ik in range(k-j+1): # loop over all colors up to current depth
        freeIndices = [ilc for ilc,jlc in enumerate(labeling) if jlc == 0]
        cIdx = loc[ik] # reading on the ik-th wheel of the odometer
        # color the labeling with the ik-th color according to the current index for this color
        clabeling = integer2coloring(cIdx,len(freeIndices),colors[ik])
        # Load up the labeling with the current color in the open slots
        for icIdx,jcIdx in enumerate(freeIndices):
            if clabeling[icIdx] != 0:
                labeling[jcIdx] = ik + 1
    print "j",j, "ic",ic,"loc", loc, labeling
    while True:
        if loc[j] != limit[j]-1: break # This wheel is not read to roll over yet, so advance it below
        # roll over current wheel
        loc[j] = 0
        j -= 1
        if j<0: break
    if j<0: break
    loc[j] += 1

    #temp# Apply the permutations to the labeling, check index of each whether
    #temp# idx < cIdx. If so, current coloring is a symmetric duplicate
    #temp# Also collect the stabilizer while iterating over the group
    #temp# elements
    #tempprint "<<<location: ",t.loc
    #tempfor ig in G[t.depth]: # Don't skip the identity, we need it at the next depth
    #temp    rlabeling = [labeling[ilc] for ilc in ig]
    #temp    # Now we need to reduce the coloring to zeros and current color only so that we can use the
    #temp    # coloring2integer routine
    #temp    if rlabeling == labeling: # current group operation is a member of the stabilizer
    #temp        G[t.depth+1].append(ig) # Add this group element to the stabilizer for the next depth
    #temp        print ig, "added to stabilizer"
    #temp    short = []
    #temp    for i in rlabeling:
    #temp        if i==t.depth+1: # i.e., the current color
    #temp            short.append(1)
    #temp        elif i==0:
    #temp            short.append(0)
    #temp    rIdx = coloring2integer(short)        
#   #temp     print "rIdx",rIdx,"short",short
    #temp    if rIdx < t.ccIdx: # Then we've hit this coloring before. Exit.
    #temp        print "found duplicate"
    #temp        t.decrement_depth()
    #temp        G[t.depth+1] = []             # Need to reset the stabilizer too
    #temp        break
    #tempelse: # This is a surviving coloring. If we are at the bottom of the tree, then it is a complete
    #temp      # labeling and should be added to the survivor list.
    #temp    if t.depth == t.k-2: # Add current coloring to the surivor list.
    #temp        survivors.append(t.loc[:])
    #temp        G[t.depth+1] = []             # Need to reset the stabilizer too
#   #temp     print "stabilizer:", G[t.depth+1]
    #tempif t.loc == [-1]*t.k: # We are at the very end of the tree. We're all done
    #temp    break
    #temp# If we are on the last branch at this layer we don't want to increment to the next node (why not?)
    #tempif t.ccIdx <= rIdx: # current color index 
    #temp    print "incrementing: ccInd",t.ccIdx,
    #temp    t.increment_location()


#    else: # This was the last branch at this level and we need to reset the stabilizer too
#        print "clearing the stabilizer"
#        G[t.depth+1] = []
                                                  
for i,iSurv in enumerate(survivors):
    print "%s"%iSurv,
    if i < len(survivors) -1:
        if survivors[i][0] != survivors[i+1][0]:
            print 
print "\n"
print "number of survivors:",len(survivors)
if sys.argv[1] == "ps":
    for i in survivors:
        print i
#
#import matplotlib
#import matplotlib.pyplot
#
#cfig = matplotlib.pyplot.figure(figsize=[8.5,11])
#matplotlib.pyplot.subplots_adjust(left=0.001,right=.999,top=.999,bottom=.001)
#c = cfig.add_subplot(111)
#c.set_xlim([0,1000])
#c.set_ylim([0,1000])
#c.invert_yaxis()
#c.set_axis_off() # This gets rid of the coordinate ax
#c.set_aspect("equal")
#
#textdict = {"ha" :"center",
#            "va" : "center",
#            "size" : 12,
#            "fontname" : "Arial",
#            "zorder" : 1}
#
#pink = [1,.7,.7]
#lightblue = [.8,.9,1]
#lightgray = [.9,.9,.9]
#darkgray = [.7,.7,.7]
#
#xoffset = 10
#radius = 10
#xspacing = 2*radius*1.2
#colors = {1:"red", 2:"yellow", 3:"green", 0:"cyan"}
#yspacing = 2*radius*1.4
#yoffset = 10
#yiter = yoffset
#xiter = xoffset
#for j,iSurv in enumerate(survivors):
#    t.loc = iSurv
#    labeling = t.coloring
#    if yiter > 950:
#        yiter -= 33*yspacing
#        xiter += xspacing*t.n+5*xoffset
#    else:
#        yiter += yspacing
#        
#    for i in range(t.n):
#        fc = colors[labeling[i]]
#        p = matplotlib.patches.Circle([i*xspacing+xiter,yiter],radius,fc=fc,ec=[0.5,0.5,0.5],linewidth=.1,zorder=0)
#        c.add_patch(p)
#    c.text(xiter-xspacing,yiter,str(j+1),**textdict)
#
##c.text(0,0,"HERE",**textdict)
#
#cfig.savefig("perms.pdf",bbox_inches="tight")
