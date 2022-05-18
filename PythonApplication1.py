import random
import sys

commands=sys.argv
searchtype=commands[2]
initfile=commands[3]
numofsteps=commands[4]
numofsteps=int(numofsteps)

#numofsteps=96

with open(initfile) as f:lines = f.readlines()
M= (len(lines))
N=len(lines[0])-1
#print(N) #x row width 
#print(M) #y column height
#print(lines)


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

data= [[0 for x in range(N)] for x in range(M)]
#food=Grid(M, N, False)
#walls= Grid(M, N, False)
food=[[False for x in range(N)] for x in range(M)]
walls=[[False for x in range(N)] for x in range(M)]
#print('wallheight:',walls.height)
#print('wallwidth:',walls.width)
agentpositions=[]
foodpositions=[]
#print(data)
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
        return None
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
    if(not iswall([x,y-1])):
        directs.append('L')
    if(not iswall([x,y+1])):
        directs.append('R')
    if(not iswall([x+1,y])):
        directs.append('D')
    if(not iswall([x-1,y])):
        directs.append('U')    
    return directs
def movedirection (agentcoo):#returns directions towards closest food
    dirs=[]
    foodclosest=closestfood(food,agentcoo)
    if foodclosest is None:
        return legalmoves(agentcoo)
    foodid=foodclosest[1]
    foodx=foodpositions[foodid][0]
    foody=foodpositions[foodid][1]
    agentx=agentcoo[0]
    agenty=agentcoo[1]
    if((agenty-foody)>0):
        dirs.append('L')
    elif((agenty-foody)<0):
        dirs.append('R')
    if((agentx-foodx)<0):
        dirs.append('D')
    elif((agentx-foodx)>0):
        dirs.append('U')
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
#print('init cleanter:',cleanerposition)
#print('init agents: ',agentpositions)
for i in range(numofsteps):#main loop
    if(i%(numghosts+1)==0):#cleaner's turn
        if(isfood(cleanerposition)):#suck
            food[cleanerposition[0]][cleanerposition[1]]=False
            utility+=1
            callsutility+=1
            for j in range(len(foodpositions)):
                if(foodpositions[j]==cleanerposition):
                    #print('cleaner temizliyor :',foodpositions[j])
                    foodpositions.pop(j)
                    break
        else:
            if(i==0):
                print("Action:",movedirection(cleanerposition)[0])
            cleanerposition=moveoptimal(cleanerposition)
            #print('cleaner:',cleanerposition)
            if(cleanerposition in (el[1] for el in agentpositions)):
                utility=-100
                callsutility+=1
                break
    else:#competent turn
        turnnumber=(i%(numghosts+1))-1
        agentpost=agentpositions[turnnumber][1]
        agentnumber=agentpositions[turnnumber][0]
        if(isfood(agentpost)):#suck
            food[agentpost[0]][agentpost[1]]=False
            utility-=1
            callsutility+=1
            for k in range(len(foodpositions)):
                if(foodpositions[k]==agentpost):
                    #print('agent temizliyor :',foodpositions[k])
                    foodpositions.pop(k)
                    break
        else:
            if(agentnumber%2==0):#even move optimal
                agentpost=moveoptimal(agentpost)
                agentpositions[turnnumber][1]=agentpost
                #print('agents: ',agentpositions)
                if(cleanerposition in (el[1] for el in agentpositions)):
                    utility=-100
                    callsutility+=1
                    break
            if(agentnumber%2==1):#odd move random
                agentpost=moverandom(agentpost)
                agentpositions[turnnumber][1]=agentpost
                #print('agents: ',agentpositions)
                if(cleanerposition in (el[1] for el in agentpositions)):
                    utility=-100
                    callsutility+=1
                    break
print("Value: ",utility)
print("Util Calls: ",callsutility)
#print(closestfood(food,agentpositions[0]))