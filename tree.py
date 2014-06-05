from msgenum import integer2coloring, coloring2integer, choose
#from scipy.special import binom as choose

class Tree(object):
    """Creates a tree structure and methods for manipulating it."""
    def __init__(self, colors):
        # Keep the list of colors
        self.colors = colors # Would it be better to do self.k = len(self.colors)?? Ask Conrad
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

        
    @property
    def coloring(self):
        """ Generates the coloring associated with the current location in the tree """
        labeling = [0]*self.n
        for ik in range(self.loc.index(-1)): # Loop over colors to current depth
            # Find all slots in coloring that are still empty
            freeIndices = [ilc for ilc,jlc in enumerate(labeling) if jlc == 0]
            # Get the current index for ik-th color
            cIdx = self.loc[ik]
            # Get the coloring that corresponds to the current index so that we can add it to the labeling
            clabeling = integer2coloring(cIdx,len(freeIndices),self.colors[ik])
            # Load up labeling with the current color in the corrent slots
            for iIdx,jIdx in enumerate(freeIndices):
                if clabeling[iIdx] !=0:
                    labeling[jIdx] = ik + 1
        self.labeling = labeling
        return self.labeling

    def increment_location(self,G):
        """ Increment the position (node) in a tree structure.
        Either move across branches at the same depth
        or moving down or up between levels """
        d = self.loc.index(-1) -1 # Depth of current location
        if d < self.k - 2: # Then we can still go down
            d += 1
            self.loc[d] = 0
        else:
            self.loc[d] += 1
            G[d+1] = [] 
            while self.loc[d] > self.branches[d]-1: # If end of branches at this depth, 
                d -= 1                              # go up until we can go down again
                G[d+1] = [] 
                self.loc[d+1] = -1
                if d < 0:
                    break # All done with the tree
                self.loc[d] += 1
        self.nLoc += 1
    

    def next_branch(self,G):
        """ advance to next branch. Move up to higher level if necessary """
        d = self.loc.index(-1) -1 # Depth of current location
        self.loc[d] += 1 # Move one branch to the right      
        G[d+1] = [] # Reset the generator on level below
        while self.loc[d] > self.branches[d]-1: # If end of branches at this depth, 
            d -= 1                              # go up until we can go down again
            self.loc[d+1] = -1
            G[d+1] = [] # Reset the generator for new level
            if d < 0:
                break # All done with the tree
            self.loc[d] += 1
        self.nLoc += 1
        

    @property
    def depth(self):
        """ Returns the depth of the current location in the tree """
        return self.loc.index(-1) -1
    
    @property
    def ccIdx(self):
        """ Returns the index of the current color, i.e., the index of the branch of the current
    depth in the tree """
        return self.loc[self.depth]

def matchloc(alist,val):
    """ Returns the indices of elements in a list that match 'val'" """ 
    return  [ilc for ilc,jlc in enumerate(alist) if jlc==val]

