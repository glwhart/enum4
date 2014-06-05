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


class tree(object):
    """Creates a tree structure and methods for manipulating it."""
    def __init__(self, colors):
        # Number of colors is also the depth of the tree
        self.k = len(colors)
        # Number of slots for colors
        self.n = sum(colors)
        # Permutation group associated with the tree
        self.group = []
        # Stabilizer group 
        self.stabilizer = []
        # Location in the tree
        self.loc = [-1]*self.k
        # Number branches at each depth
        self.branches =  [choose(sum(colors[ilc:]),colors[ilc]) for ilc in range(len(colors)-1)]
        # Number of locations visited so far
        self.nLoc = 0 
        # Depth of the current location
        self.depth = -1

    @property
    def increment_location(self):
        """ Increment the position (node) in a tree structure.
        Either move across branches at the same depth
        or moving down or up between levels """
        d = self.loc.index(-1) -1 # Depth of current location
        if d < self.k - 2: # Then we can still go down
            d += 1
            self.loc[d] = 0
        else:
            self.loc[d] += 1
            while self.loc[d] > self.branches[d]-1: # If end of branches at this depth, 
                d -= 1                      # go up until we can go down again
                self.loc[d+1] = -1
                if d < 0:
                    break # All done with the tree
                self.loc[d] += 1
        self.nLoc += 1
        return self.loc

### Could we make some headway on the restricted site problem (at least for spectators) by using
### groups that skipped those sites (left them unchanged)?

colors = [2,2,2] # Number of each color in the list
t = tree(colors)

# Construct the cyclic permutation group of order n
group = [range(t.n)]
for i in range(1,t.n):
    group.append([(j+i)%t.n for j in group[0]])

survivors = []

print "Branches",t.branches
print "loc",t.loc
t.increment_location
#print t.loc != [-1]*t.k
while t.loc != [-1]*t.k:
    # Check to see if this coloring has been visited already before
    d = t.loc.index(-1) - 1 # get the current depth
    
    print t.loc
    t.increment_location

#while
