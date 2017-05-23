import sys

class CSP:
    
    def __init__(self,inputString):  
        CSP.digits = '123456789'
        CSP.rows = 'ABCDEFGHI'
        CSP.columns = '123456789'
        #all the squares on the board
        CSP.squares = CSP.cartesianProduct(CSP.rows, CSP.columns)

        unitList = []
        unitList.extend( [CSP.cartesianProduct(CSP.rows,c) for c in CSP.columns] )
        unitList.extend( [CSP.cartesianProduct(r,CSP.columns) for r in CSP.rows] )
        unitList.extend( [CSP.cartesianProduct(x,y) for x in ['ABC','DEF','GHI'] for y in ['123','456','789']] )

        CSP.peers = dict( (s,[u for u in unitList if s in u]) for s in CSP.squares )
        for key in CSP.peers.iterkeys():
            value = CSP.peers[key]
            CSP.peers[key] = set([s for unit in value for s in unit]) - set([key])

        self.domain = dict( (s, CSP.digits) for s in CSP.squares )
        
        #initialize the domain for the squares
        i = 0
        for row in CSP.rows:
            for column in CSP.columns:
                if(inputString[i] != '0'):
                    s = row+column
                    if self.assignmentAndConstraintPropagation(self.domain,s,inputString[i]) is False:
                        print 'Invalid input string.'
                        sys.exit()
                i = i + 1

    @staticmethod
    def cartesianProduct(X, Y):
        return [x+y for x in X for y  in Y]

    def mrv(self,squares):
        (n,s) = min([ ( len( self.domain[square] ), square ) for square in squares if len( self.domain[square] ) > 1])
        return s

    def isSolved(self,domain):
        if all( len( domain[s] ) == 1 for s in CSP.squares ):
        	return True
        else:
        	return False

    #in this method, you assign a value and check if it's a legal assignment
    def assignmentAndConstraintPropagation(self,domain,s,value):
        domain[s] = value
        #check if you can delete this value from its peers
        if all( self.delete(domain,p,value) for p in self.peers[s] ):
            return True
        else:
            return False

    #this method deletes value from s
    def delete(self,domain,s,value):
        values = domain[s]
        if value not in values:
            return True

        #value is the only digit so cannot delete
        elif len(values) == 1:
            return False

        else:
            domain[s] = domain[s].replace(value,'')
            if len(domain[s]) == 1:
            	value = domain[s]
                if not all(self.delete(domain,p,value) for p in CSP.peers[s]):
                    return False
        return True

    def setDomain(self,domain):
        self.domain = domain.copy()

    def backtrackingSearch(self):
        #this copy is important as it is used to restore the state whenever one of branches reaches a dead end
        domainCopy = self.domain.copy()
        if self.isSolved(domainCopy):
            return domainCopy

        s = self.mrv(CSP.squares)
        values = domainCopy[s]
        for value in values:
        	self.setDomain(domainCopy)
        	if self.assignmentAndConstraintPropagation(self.domain,s,value):
	            #assignment was successful
	        	result = self.backtrackingSearch()
	        	if result is not False:
	        		return result
        return False

    def display(self,assignment):
        line = '------+------+------'
        for r in CSP.rows:

            print ''.join( assignment[r+c].center(2) + ('|' if c in '36' else '') for c in CSP.columns )
            if r in 'CF': print line
        print '\n'

def main(argv):
    if(len(argv) != 1):
        print 'Usage: python sudoku.py <input-string>'
        sys.exit()

    csp = CSP(argv[0])
    csp.backtrackingSearch()
    csp.display(csp.domain)

if __name__ == '__main__':
    main(sys.argv[1:])

