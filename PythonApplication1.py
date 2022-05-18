import random
import sys

commands=sys.argv
initfile2=commands[3]
numsteps=commands[4]

numofsteps=48

with open('inp.txt') as f:lines = f.readlines()
M= (len(lines))
N=len(lines[0])-1
#print(N) #x row width 
#print(M) #y column height
#print(lines)


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.
    The __str__ method constructs an output that is oriented like a pacman board.
    """
    def __init__(self, height, width, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for x in range(width)] for y in range(height)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def getitem(self, i,j=None):
        if(j==None):return self.data[i]
        else: return self.data[i][j]

    def setitem(self, key, item):
        self.data[key] = item

    #def __str__(self):
    #    out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
    #    out.reverse()
    #    return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None: return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item =True ):
        return sum([x.count(item) for x in self.data])

    def asList(self, key = True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: list.append( (x,y) )
        return list

    def packBits(self):
        """
        Returns an efficient int list representation
        (width, height, bitPackedInts...)
        """
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currentInt)
                currentInt = 0
        bits.append(currentInt)
        return tuple(bits)

    def _cellIndexToPosition(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        """
        Fills in data from a bit-level representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height: break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0: raise ValueError ("must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools

def reconstituteGrid(bitRep):
    if type(bitRep) is not type((1,2)):
        return bitRep
    width, height = bitRep[:2]
    return Grid(width, height, bitRepresentation= bitRep[2:])

data= [[0 for x in range(N)] for x in range(M)]
#food=Grid(M, N, False)
#walls= Grid(M, N, False)
food=[[False for x in range(N)] for x in range(M)]
walls=[[False for x in range(N)] for x in range(M)]
#print('wallheight:',walls.height)
#print('wallwidth:',walls.width)
agentpositions=[]
foodpositions=[]
print(data)
numghosts=0
utility=0
for i in range(M):
    for j in range(N):
        #print('i ve j: ',i,j)
        if(lines[i][j]=='x' or lines[i][j]=='X'):
            data[i][j]='x'
            walls[i][j]=True
        elif(lines[i][j]=='c' or lines[i][j]=='C'):
            data[i][j]='c'
            cleanerposition=[i, j]
        elif(lines[i][j]=='.'):
            data[i][j]='.'
            foodpositions.append([i,j])
            food[i][j]=True
        elif(lines[i][j]==' '):
            data[i][j]=0
        else:
            data[i][j]=int(lines[i][j])
            agentpositions.append( [int(lines[i][j]), [i, j] ] )
            numghosts+=1

#print(agentpositions[0])
#print(foodpositions)

def closestfood(foods,agentcoo):#returns [md to food, food id]
    agentxy=agentcoo
    distances=[]
    for i in range(len(foodpositions)):
        foodxy=foodpositions[i]
        distances.append([manhattanDistance(agentxy,foodxy),i])
    distances.sort()
    if(not distances):#no food
        distances=[1]
    return(distances[0])
#print(closestfood(food,agentpositions[0]))
def iswall(coordinates):
    x=coordinates[0]
    y=coordinates[1]
    return(walls[x][y])
def isfood(coordinates):
    x=coordinates[0]
    y=coordinates[1]
    return(food[x][y])
def legalmoves(agentcoo):
    directs=[]
    x=agentcoo[0]
    y=agentcoo[1]
    if(not iswall([x-1,y])):
        directs.append('U')
    if(not iswall([x,y-1])):
        directs.append('L')
    if(not iswall([x+1,y])):
        directs.append('D')
    if(not iswall([x,y+1])):
        directs.append('R')
    return directs
def movedirection (agentcoo):#returns directions towards closest food
    dirs=[]
    foodclosest=closestfood(food,agentcoo)
    foodid=foodclosest[1]
    foodx=foodpositions[foodid][0]
    foody=foodpositions[foodid][1]
    agentx=agentcoo[0]
    agenty=agentcoo[1]
    if((agenty-foody)>0):
        dirs.append('L')
    elif((agenty-foody)<0):
        dirs.append('R')
    if((agentx-foodx)>0):
        dirs.append('U')
    elif((agentx-foodx)<0):
        dirs.append('D')
    if(dirs==[]):
        dirs.append('St')
    return(dirs)

def moveoptimal(agentcoo):
    opdirs=movedirection(agentcoo)
    if(opdirs[0]=='L'):
        agentcoo[1]=(agentcoo[1]-1)
    elif(opdirs[0]=='R'):
        agentcoo[1]=(agentcoo[1]+1)
    elif(opdirs[0]=='U'):
        agentcoo[0]=(agentcoo[0]-1)
    elif(opdirs[0]=='D'):
        agentcoo[0]=(agentcoo[0]+1)
    return agentcoo
def moverandom(agentcoo):
    opdirs=legalmoves(agentcoo)
    direction=opdirs[random.randrange(len(opdirs))]
    if(direction=='L'):
        agentcoo[1]=(agentcoo[1]-1)
    elif(direction=='R'):
        agentcoo[1]=(agentcoo[1]+1)
    elif(direction=='U'):
        agentcoo[0]=(agentcoo[0]-1)
    elif(direction=='D'):
        agentcoo[0]=(agentcoo[0]+1)
    return agentcoo
callsutility=0
#print(legalmoves(agentpositions[0][1]))
#print(movedirection(agentpositions[0][1]))
print('init cleanter:',cleanerposition)
print('init agents: ',agentpositions)
for i in range(numofsteps):#main loop
    print('adım',i)
    if(i%(numghosts+1)==0):#cleaner's turn
        if(isfood(cleanerposition)):#suck
            food[cleanerposition[0]][cleanerposition[1]]=False
            utility+=10
            callsutility+=1
            for j in range(len(foodpositions)):
                if(foodpositions[j]==cleanerposition):
                    print('cleaner temizliyor :',foodpositions[j])
                    foodpositions.pop(j)
                    break
        else:
            cleanerposition=moveoptimal(cleanerposition)
            print('cleaner:',cleanerposition)
            if(cleanerposition in agentpositions):
                utility=-100
                callsutility+=1
                break
    else:#competent turn
        turnnumber=(i%(numghosts+1))-1
        agentpost=agentpositions[turnnumber][1]
        agentnumber=agentpositions[turnnumber][0]
        if(isfood(agentpost)):#suck
            food[agentpost[0]][agentpost[1]]=False
            utility-=10
            callsutility+=1
            for k in range(len(foodpositions)):
                if(foodpositions[k]==agentpost):
                    print('agent temizliyor :',foodpositions[k])
                    foodpositions.pop(k)
                    break
        else:
            if(agentnumber%2==0):#even move optimal
                agentpost=moveoptimal(agentpost)
                agentpositions[turnnumber][1]=agentpost
                print('agents: ',agentpositions)
                if(cleanerposition in agentpositions):
                    utility=-100
                    callsutility+=1
                    break
            if(agentnumber%2==1):#odd move random
                agentpost=moverandom(agentpost)
                agentpositions[turnnumber][1]=agentpost
                print('agents: ',agentpositions)
                if(cleanerposition in agentpositions):
                    utility=-100
                    callsutility+=1
                    break
print(utility)
print(callsutility)
#print(closestfood(food,agentpositions[0]))