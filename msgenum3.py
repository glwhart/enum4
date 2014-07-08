#from scipy.special import binom as choose
import sys

def polya_count(G,colors):
    """ Given a group, and a "color vector" (list of number of colors
    of each label), use Polya's enumeration theorem to find how many 
    symmetrically-distinct configurations exist """
    cycles = {}
    for g in G:
        c = str(cycle_counter(g))
        if c in cycles:
            cycles[c] += 1
        else:
            cycles[c] = 1
    total = 0
    for i in cycles:
        v = eval(i)
        fitTimes = partition_cycles_into_color_vector(colors,v)
        total += fitTimes*cycles[i]
    nG = len(G)
    if total/nG != int(total/nG):
        print("total:",total," Group size:",nG)
        sys.exit("ERROR: function 'polya_count' gave a non-integer value")
    return int(total/len(G))


def cycle_counter(perm):
    """ Counts the number of disjoint cycles in a permutation """
    if not any(i==0 for i in perm):
        sys.exit("cycle_counter assumes that permutations use zero indexing")
    n = len(perm)
    mask = [0]*n
    cycList = []
    while any(i==0 for i in mask):
        #print("mask",mask)
        pos = mask.index(0)
        c = 0
        while True:
            c += 1
            #print("c,pos",c,pos)
            mask[pos] = 1
            pos = perm[pos]
            #print("perm[pos]",pos)
            if mask[pos] != 0: break
        cycList.append(c)
    cycList.sort()
    return cycList
        
    

def partition_cycles_into_color_vector(colors,cycles):
    """ Counts the number of ways that a list of  cycles can be partitioned
    match the number colors. That is, the number of ways the cycle
    vector can be "fit into" the color vector.  """

    nCo = len(colors) # Number of colors
    nCy = len(cycles) # Number of cycles
    count = 0  # Number of legal partitions found
    cyIdx = 0  # Index for the current cycle under consideration
    F = [-1]*nCy # Indicates which cycles have been stored in which color slot 
    S = [0]*nCo # Indicates the open slots in the color vector (that can still take cycles)
    m = cycles  
    while cyIdx >=0:
        # Check whether current cycle can fit into current partitioning
        if F[cyIdx]>-1: 
            S[F[cyIdx]] -= cycles[cyIdx]
        coIdx = F[cyIdx] + 1
        found = True
        if coIdx < nCo:
            # Advance the colorIdx if there are still colors to but we can't fit another cycle in
            # this color slot (second condition)
            while coIdx < nCo-1 and S[coIdx] + m[cyIdx] > colors[coIdx]:
                coIdx += 1
            # If we can fit another cycle in the current color slot
            if S[coIdx] + m[cyIdx] <= colors[coIdx]: 
                F[cyIdx] = coIdx
                S[coIdx] += m[cyIdx]
                if cyIdx == nCy-1:
                    count += 1
            else:
                found = False
        else:
            found = False
        if cyIdx == nCy-1 or found is not True:
            if found: # then remove current cycle from color slot
                S[coIdx] -= m[cyIdx]
            F[cyIdx] = -1
            cyIdx -= 1
        else:
            cyIdx += 1
    return count


def grouper(generators):
    """ Generate a group from its generators """
    # Modified from its first form to be a little faster (but isn't as succinct anymore)
    # The basic approach is to loop over all binary combinations of the generators to see if new
    # group elements arise. If they do, these are appended to the list. The checks are continued
    # until no new elements are generated. mG is introduced to avoid checking combinations that have
    # already been tried
    if not all(len(i)==len(generators[0]) for i in generators):
        sys.exit("ERROR: the generators passed to 'grouper' are not all same length")
    growing = True
    mG = 0 # Index marking which part of the table can be skipped
    while growing:
        growing = False
        nG = len(generators)
        print("nG",nG)
        # Loop over each possible pair of group elements to see if they create a new element
        for iDx,iG in enumerate(generators[:nG]):
            for jDx,jG in enumerate(generators[:nG]):
                if iDx < mG and jDx < mG: continue # Skip parts of the table already visited
                g = [iG[i] for i in jG]
                if not g in generators:
                    generators.append(g)
                    growing = True
        mG = nG # Store the number of group element we had at the beginning of the current checking
    return generators

def choose(n, k):
    """ Binomial coefficient. Computes the number of permutations of n things, taken k at a
    time. This implementation was taken from "Binomial Coefﬁcient Computation: Recursion or
    Iteration?" by  Yannis Manolopoulos, ACM SIGCSE Bulletin InRoads, Vol.34, No.4, December
    2002. http://delab.csd.auth.gr/papers/SBI02m.pdf 
    It is supposed to be robust against large, intermediate values and to have optimal
    complexity."""
    if k < 0 or k > n: 
        return 0
    if k==0 and n == 0:
        return 1
    t = 1
    if k < n-k:
        for i in range(n, n-k, -1):
            t = t*i/(n-i+1)
    else:
        for i in range(n,k,-1):
            t = t*i/(n-i+1)
    return t
        
def integer2coloring(y, m, a):
    """
    Take an integer and convert it into a binary coloring
    """
    if m < a or y > choose(m,a): # Check that we didn't give nonsense input
        print( "y=",y," m=",m," a=",a)
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

