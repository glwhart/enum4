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

    
    

### Test the routines for the case of 10 slots and 3 "red" (and 7 non-red)

colors = [2,3,2] # Number of each color in the list
n = sum(colors) # Number of entries in the list
k = len(colors) # Number of different colors 

### Could we make some headway on the restricted site problem (at least for spectators) by using
### groups that skipped those sites (left them unchanged)?

# Construct the cyclic permutation group of order n
group = [range(n)]
for i in range(1,n):
    group.append([(j+i)%n for j in group[0]])

survivors = []

cIndx = [0]*k

while True:
    j = k - 1 # j is the current color 0<=j<k
    
    
 # Use this to keep track of where we are in the tree
#for ir in range(choose(n,colors[0])): # Outer loop over configurations of color 1
#
#    for ik in range(k): # Loop over colors
        
# mixed radix counter
digit = [idig-1 for idig in colors]
counter = [0]*k
counter[k-1] = -1 # Start one back so that first reading is all zeros
ic = 0
while True:
    j = k - 1
    while True:
        if counter[j] != digit[j]: break
        counter[j] = 0
        j = j - 1
        if j < 0: break
    if j < 0: break
    counter[j] += 1
    print counter
    ic += 1
#for ic in range(k):
#    m = sum(colors[ic:k]) # Number of slots for this color
#    a = colors[ic] # Number of this color
#    hashtable = [0]*choose(m,a) # Empty hash table for permutations of this color
#    print "ic = ",ic," m = ",m,"  a = ",a
#    for i in range(choose(m,a)):
##    print "i,hash",i, hashtable[i]
#        if hashtable[i] == 0: # Skip things already in the list 
#            hashtable[i] = 2
#            # Cross out duplicates
#            for iOp in range(1,len(group)): # Skip the identity by starting at 1
#                #            print "i,iOp",i,iOp
#                testl = integer2coloring(i,m,a) # get the i-th coloring
#                #            print "original list",testl
#                idx = coloring2integer([testl[j] for j in group[iOp]])
#                #            print "idx",idx
#                if idx < i:
#                    sys.exit("Problem: equivalent coloring occurred earlier in the table")
#                hashtable[idx] = 1
#    print "Number of unique colorings for color ",ic,": " , hashtable.count(2)
#
## Have Rod check the case of m = 10, a = 3, and cyclic permgroup of 10
