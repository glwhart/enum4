#!/usr/bin/python
# This version of the program tries to solve the "surjective enumeration" problem with the order of
# the loops reversed from what we first envisioned. The inner loop will be over colors (traversing
# up and down the "tree") the outer loop will be over configurations for each color.
import sys

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

def coloring2integer(coloring):
    """
    Take a coloring list and convert it into an integer
    """
    m = len(coloring)
    # Find the rightmost 1 in the list
    coloring.reverse()
    rm1 = m - coloring.index(1) # Finds the leftmost 1 (but we reversed the list)
    coloring.reverse() # Put the list back in the correct order
    
    z = coloring[:rm1].count(0) # Number of zeros with at least one "1" to their right
    x = 0
    templist = coloring
    for i in range(z): # Loop over the zeros with a 1 to their right
        p0 = templist.index(0) # Position of first zero in the temporary list
        n1r = templist[p0:].count(1) # Number of 1s to the right of leftmost zero
        templist = templist[p0+1:] # Throw away the leftmost zero
        x += choose(len(templist),n1r-1) # Compute the binomial coefficient for this "digit" of the number
    return x

    
    


colors = [4,2,2] # Number of each color in the list
n = sum(colors)  # Number of entries in the list
k = len(colors)  # Number of different colors 

### Could we make some headway on the restricted site problem (at least for spectators) by using
### groups that skipped those sites (left them unchanged)?

# Construct the cyclic permutation group of order n
group = [range(n)]
for i in range(1,n):
    group.append([(j+i)%n for j in group[0]])

survivors = []

### Traverse a tree

# Compute the number of branches at each depth
c = [choose(sum(colors[ilc:]),colors[ilc]) for ilc in range(len(colors)-1)]
if len(c) != k-1: sys.exit("Something is wrong")

treeLoc = [-1]*k # Leftmost of the tree
ic = 0 # Number of leaves visited
nLeaves = reduce(lambda x,y:x*y, c)
while True:
    iDepth = treeLoc.index(-1) -1
    if iDepth < k - 2: # Then we can still go down
        iDepth += 1
        treeLoc[iDepth] = 0
    else:
        treeLoc[iDepth] += 1
        while treeLoc[iDepth] > c[iDepth]-1: # If end of branches at this depth, 
            iDepth -= 1                      # go up until we can go down again
            treeLoc[iDepth+1] = -1
            if iDepth < 0:
                break # All done with the tree
            treeLoc[iDepth] += 1
        ic = ic + 1
        if iDepth < 0: break
    print treeLoc

#    if ic > 1000: break
if nLeaves != ic:
    print "ERROR: Something went wrong. Wrong number of leaves on tree"

