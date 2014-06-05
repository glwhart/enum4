#!/usr/bin/python
import sys

        
def integer2coloring(y, m, a):
    """
    Take an integer and convert it into a binary coloring
    """
    if m < a or y > choose(m,a): # Check that we didn't give nonsense input
        print "y=",y," m=",m," a=",a
        sys.exit("bad call to integer2coloring")
    # This follows the algorithm in the enum3 paper, Comp Mat Sci 59 101 (2010) exactly
    I = y
    t = a
    ell = m
    configlist = [-1]*m
    #while any([i==-1 for i in configlist]):
    while ell > 0:
        if choose(ell-1,t-1) <= I:
            configlist[m-ell] = 0
            I -= choose(ell-1,t-1)
        else:
            configlist[m-ell] = 1
            t -= 1
        ell -= 1
    return configlist    

def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    (This probably isn't good for large values of n and k, but OK for our purposes --GH)
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

loc = [19,4,-1]
colors = [4,2,2]
n = sum(colors)

labeling = [0]*n
branches = [choose(sum(colors[ilc:]),colors[ilc]) for ilc in range(len(colors)-1)]

for ik in range(loc.index(-1)):
    print loc[ik]
    freeIndices = [ilc for ilc,jlc in enumerate(labeling) if jlc == 0]
    print freeIndices
    cIdx = loc[ik]
    clabeling = integer2coloring(cIdx,len(freeIndices),colors[ik])
    print clabeling
    # Load up labeling with the new color
    for iIdx,jIdx in enumerate(freeIndices):
        if clabeling[iIdx] !=0:
            labeling[jIdx] = ik + 1
    print labeling

# No need to throw in the missing colors. We just want to use the
# colors at this depth of the tree

#for iLast in [ilc for ilc,jlc in enumerate(labeling) if jlc==0]:
#    print iLast
#    labeling[iLast] = len(colors)
#print labeling

