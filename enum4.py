#!/usr/bin/python
# This version of the program tries to solve the "surjective enumeration" problem with the order of
# the loops reversed from what we first envisioned. The inner loop
# will be over colors, the outer loop will be over configurations for
# each color. This version doesn't use a tree structure but uses a
# mixed-radix number (odometer with wheels that don't match) to
# generate each configuration).
import sys
from msgenum import integer2coloring, coloring2integer, choose

def generate_labeling(n,cc,loc):
    """
    Generate a coloring, to depth of color cc, that is n spaces long, for the current location in
    the odometer
    """
    labeling = [0]*n
    for ik in range(cc): # loop over all colors up to current depth
        freeIndices = [ilc for ilc,jlc in enumerate(labeling) if jlc == 0]
        cIdx = loc[ik] # reading on the ik-th wheel of the odometer
        # color the labeling with the ik-th color according to the current index for this color
        clabeling = integer2coloring(cIdx,len(freeIndices),colors[ik])
        # Load up the labeling with the current color in the open slots
        for icIdx,jcIdx in enumerate(freeIndices):
            if clabeling[icIdx] != 0:
                labeling[jcIdx] = ik + 1
    return labeling

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
loc = [0]*(k-1)
loc.append(-1) # Start at 0...0(-1) so that first increment goes to 00...0
limit = [choose(sum(colors[ilc:]),colors[ilc]) for ilc in range(len(colors))]
it = 0
nIts = reduce(lambda x,y:x*y, limit)
print "limit",limit
while loc != limit and it < nIts:
    it += 1
    j = k - 1 # j is the "wheel number"---digit pointer indicating which wheel is turning (that is,
              # it indicates the active color). It always starts at the far right. 
    while True: # Update the reading on the odometer
        if loc[j] != limit[j]-1: break # This wheel is not read to roll over yet, so advance it below
        # roll over current wheel
        loc[j] = 0
        j -= 1
        if j<0: break
    if j<0: break
    loc[j] += 1
    print "***<<< Location >>>***", loc
    print "<<< wheel number >>>",j
#    if j > 0: # if j == 0, then we are on the last color, but there's only one way to do that, so we
        # can skip the loop

    # Maybe loop over each color for each odometer reading. If at any depth, we encounter a duplicate
    # coloring, then we advance the odometer from the current wheel and reset the stabilizer at the
    # current level
    

    for ic in range(k): # loop over each color and see if the current location has any duplicate
        # colorings. If so, jump the odometer ahead.

    # Construct the current labeling, all colors up to this depth
    #print "j",j, "it",it,"loc", loc, labeling
    labeling = generate_labeling(n,ic,loc)
        print "labeling",labeling
        # Apply the permutations to the labeling, check index of each whether
        # idx < cIdx. If so, current coloring is a symmetric duplicate
        # Also collect the stabilizer while iterating over the group
        # elements
        print "<<< GROUP check"
        print "group size",len(G[])
        print "location",loc,"labeling",labeling
        for cg,ig in enumerate(G[k-(j+1)]): # Don't skip the identity, we need it at the next depth
            rlabeling = [labeling[ilc] for ilc in ig]
            print "rlabeling",rlabeling
            # Now we need to reduce the coloring to zeros and current color only so that we can use the
            # coloring2integer routine
            if rlabeling == labeling: # current group operation is a member of the stabilizer
                G[k-j].append(ig) # Add this group element to the stabilizer for the next depth
                print "ig",cg, "added to stabilizer:",ig
            short = []
            for i in rlabeling:
                if i==k-j: # i.e., the current color
                    short.append(1)
                elif i==0:
                    short.append(0)
            rIdx = coloring2integer(short)        
            #print "rIdx",rIdx,"loc[k-j],",loc[k-j],"short",short
            if rIdx < loc[k-j]: # Then we've hit this coloring before. Exit.
                print "found duplicate"
                G[k-j] = []             # Need to reset the stabilizer too
                break
        else: # This is a surviving coloring. If we are at the bottom of the tree, then it is a complete
              # labeling and should be added to the survivor list.
            print "done with group: j:",j
            if j == 2: # Add current coloring to the surivor list.
                print "Adding survivor:",loc
                survivors.append(loc[:])
            print "stabilizers",[len(ilc) for ilc in G ]
            print "k",k,"j",j
        G[k-j-1] = []             # Need to reset the stabilizer too
                                                  
for i,iSurv in enumerate(survivors):
    print "%s"%iSurv,
    if i < len(survivors) -1:
        if survivors[i][0] != survivors[i+1][0]:
            print 
print "\n"
print "number of survivors:",len(survivors)
#tempif sys.argv[1] == "ps":
#temp    for i in survivors:
#temp        print i
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
#textdic<t = {"ha" :"center",
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
