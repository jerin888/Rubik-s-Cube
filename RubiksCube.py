
from collections import defaultdict, deque
import random
import sys
import time



# different moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php

MOVES = {
    "U": [2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23],
    "U'": [1,  3,  0,  2,  8,  9,  6,  7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19,  4,  5, 22, 23],
    "R": [0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23],
    "R'": [0, 22,  2, 20,  5,  7,  4,  6,  8,  1, 10,  3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
    "F": [0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9, 6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
    "F'": [0,  1,  4,  6, 13,  5, 12,  7,  9, 11,  8, 10, 17, 19, 14, 15, 16,  3, 18,  2, 20, 21, 22, 23],
    "D": [0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7],
    "D'": [0,  1,  2,  3,  4,  5, 22, 23,  8,  9,  6,  7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
    "L": [23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
    "L'": [8,  1, 10,  3,  4,  5,  6,  7, 12,  9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20,  2, 22,  0],
    "B": [5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21],
    "B'": [18, 16,  2,  3,  4,  0,  6,  1,  8,  9, 10, 11, 12, 13,  7,  5, 14, 17, 15, 19, 21, 23, 20, 22],
}
  # for normalisation
OPP ={"W":"Y","Y":"W","G":"B","B":"G","O":"R","R":"O"}
  #to print moves into template
MOVES_PRINT=[0,1,2,3,16,17,8,9,4,5,20,21,18,19,10,11,6,7,22,23,12,13,14,15]
INVERSE={"U":"U'","R":"R'","F":"F'","D":"D'","L":"L'","B":"B'",  "U'":"U","R'":"R","F'":"F","D'":"D","L'":"L","B'":"B"}
COMPLEMENTS={"U":"D'","D'":"U",
             "U'":"D","D":"U'",
             "L'":"R","R":"L'",
             "L":"R'","R'":"L",
             "F":"B'","B'":"F",
             "F'":"B","B":"F'",
             

}
m=["R", "U", "U'", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]

    


'''
sticker indices:

      0  1
      2  3
16 17  8  9   4  5  20 21
18 19  10 11  6  7  22 23
      12 13
      14 15

face colors:

    0
  4 2 1 5
    3

moves:
[ U , U', R , R', F , F', D , D', L , L', B , B']
'''

CORNERS={
  "WGO":[[2,8,17],[0,0,1]],
  "WGR":[[3,9,4],[0,1,1]],
  "YGO":[[12,10,19],[1,0,1]],
  "YGR":[[13,11,6],[1,1,1]],
  "WBO":[[0,20,16],[0,0,0]],
  "WBR":[[1,21,5],[0,1,0]],
  "YBO":[[14,22,18],[1,0,0]],
  "YBR":[[15,23,7],[1,1,0]]

}

CORNER_POS=[[2,8,17],[3,9,4],[12,10,19],[13,11,6],[0,20,16],[1,21,5],[14,22,18],[15,23,7]]
CORNER_COL=["WGO","WGR","YGO","YGR","WBO","WBR","YBO","YBR"]
CORNER_CORDINATE=[[0,0,1],[0,1,1],[1,0,1],[1,1,1],[0,0,0],[0,1,0],[1,0,0],[1,1,0]]


class Node(object):

    def __init__(self,parent=None,state=None):
        self.state = state
        self.parent = parent
        self.preMoves=[]
        self.preMove=None
        self.postMove=None
        self.level=0
        # self.visited = False
       
        
        self.f=0
        self.h=0
        self.g=0
      
        return
       

class cube:

  def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
    self.startState="WWWW RRRR GGGG YYYY OOOO BBBB"
    self.currentState=string
    self.currentStateArray=self.currentState.replace(" ", "")
    # To store random moves done in random()
    self.randomStore=[]
    self.moveStore={}
    self.BFS_start=[]
    self.parent={}
    self.nodesTraversed=0
    self.popCounter=0
    
  
    return

#Heuristics for Manhattan Distance
  def heuristics(self,state):
    
    l=0
    heuristic=0
    for i in CORNER_POS:
      ind=CORNER_POS.index(i)
      currentCord=CORNER_CORDINATE[ind]
      s=[]
      for k in i:
        s.append(state[k])
   

      # if not all(x in s for x in list(CORNER_COL[l])):
      if not set(s)==set(list(CORNER_COL[l])):
         
          for col in CORNER_COL:
            # if all(x in s for x in list(col)):
            if set(s)==set(list(col)):
              ind=CORNER_COL.index(col)
              break
              
      goalCord=CORNER_CORDINATE[ind]
      
      heuristic+=(abs(currentCord[0] - goalCord[0])+abs(currentCord[1] - goalCord[1])+abs(currentCord[2] - goalCord[2]))
      
      l+=1 

    return heuristic/4

#Function to implement A*
  def Astar(self,moves):

 
    # Create start and end node
  
    endNode = Node(None,self.currentStateArray)
    self.applyMovesStr(moves.split())

    startNode = Node(None,self.currentStateArray)
   
    startNode.g = startNode.h = startNode.f = 0
    endNode.g = endNode.h = endNode.f = 0
    # Initialize both open and closed list
    openList = []
    closedList = []
    
    # Add the start node
    openList.append(startNode)
    
    startTime=time.time()
    flag=0
    nodeCounter=0
    self.heuristics(self.currentStateArray)
    # Loop until you find the end
    while openList:
        
        # break
        # Get the current node
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index

        # Pop current off open list, add to closed list
        openList.pop(currentIndex)
        closedList.append(currentNode)
        # print(currentNode.state)
        nodeCounter+=1

        

        
        #  Found the goal
        self.currentStateArray=currentNode.state
        if self.isSolved():
            
            movesToSol = []
            self.randomStore=[]
            current = currentNode
            while current is not None:
              
                self.randomStore.append(current.state)
                movesToSol.append(current.preMove)
              
                current = current.parent
            self.randomStore.reverse()
            movesToSol.reverse()
            movesToSol.remove(None)
            print(' '.join(movesToSol))
            self.printRandom()
            print(nodeCounter)
            print(time.time()-startTime)
            break
            
        
        for move in MOVES.keys():
          if currentNode.preMove==INVERSE[move] or currentNode.preMove==COMPLEMENTS[move] or (currentNode.preMove==move and currentNode.parent.preMove==move):
            continue
          self.currentStateArray=currentNode.state
          f=0
          # children=[]
          childState=self.applyMove(move)
          # childState=self.norm()
          newNode=Node(currentNode,childState)
          newNode.preMove=move
          
          # children.append(newNode)
          # print(newNode.state)
          if self.isSolved():
            # flag=1
            newNode.g=currentNode.g
            # self.norm()
            newNode.h=self.heuristics(newNode.state)
            # print(newNode)
          # newNode.h=0
            newNode.f=newNode.h+newNode.g#Setting the f value to zero to get the goal popped out faster from open list
            
            openList.append(newNode)

            break

          

          
          for closedChild in closedList:
            if newNode.state==closedChild.state:
              f=1
              break
          if f==1:
            continue
          
          newNode.g=currentNode.g+1
          # self.norm()
          newNode.h=self.heuristics(newNode.state)
          # newNode.h=0
          newNode.f=newNode.g+newNode.h

          for openChild in openList:
            if newNode.state==openChild.state and newNode.g>openChild.g:
              f=1
              break
          if f==1:
            continue
          openList.append(newNode)


            
          
            
        if time.time()-startTime>=240:
          print("\n Time Limit exceeded!\n No solution reached.\n Please find the number of iterations and time conceded below:")
          # print(popCounter)
          print(nodeCounter)
          print(time.time()-startTime)
          break
    return





  #improve move functionality
  def checkMove(self,state,parent,move):
    temp=parent[state]
    if COMPLEMENTS.get(move)==temp[1]:
      return False
    elif INVERSE.get(move)==temp[1]:
      return False
    elif(move==temp[1] and move==temp[2]):
      return False

    
    return True
  def checkSameMove(self,state,parent,move):
    temp=parent[state]
    print(temp[0])
    print(''.join(self.BFS_start))
    if ''.join(self.BFS_start)!=temp[0]:
      temp2=parent[temp[0]]
      if move==temp[1] and move==temp2[1]:
        return False

    return True
  
  #check if two cube states are equal
  def equals(self, cubeOne,cubeTwo):
    self.currentStateArray=cubeOne
    cubeOne=self.norm()
    self.currentStateArray=cubeTwo
    cubeTwo=self.norm()
    return cubeOne==cubeTwo

#Function to print the goal path and moves for BFS and IDS
  def backtrace(self,parent, start, end):
    k=[]
   
    path = [end]
    movesToSol=[]
    while not self.equals(path[-1],start):
      
      # print
      par=parent[path[-1]]
 
      movesToSol.append(par[1])
      path.append(par[0])#Issue sort
      # print("reversed")
    movesToSol.reverse()
    # print(movesToSol)
    print(' '.join(movesToSol))
    # print(list(path[0]))
    path.reverse()
    return path,movesToSol

#Function For BFS
  def BFS(self,moves):

    parent={}
    visited=[]
    queue=deque()
    self.applyMovesStr(moves.split())
    Pcube=self.currentStateArray
    # self.norm()
    permutedCube=self.currentStateArray

    visited.append(permutedCube)
    queue.append(permutedCube)
    # print(queue)
    self.currentStateArray=permutedCube
    nodeCounter=0
    popCounter=0
    startTime=time.time()
    flag=0
    while queue:          # Creating loop to visit each node

   
      state = queue.popleft()
     
      if self.isSolved():
        self.randomStore=[]
       
        path,movesToSol=self.backtrace(parent, ''.join(permutedCube), ''.join(self.currentStateArray))
   

        self.currentStateArray=Pcube
        self.randomStore.append(self.currentStateArray)
        self.applyMovesToStore(movesToSol)
        self.printRandom()
        # print(popCounter)
        print(nodeCounter)
        print(time.time()-startTime)
        
        break

      for move in MOVES.keys():
        # print(move)
        
        if (popCounter>0 and not self.checkMove(''.join(state),parent,move)) : 
          continue
       
        else:
          # print("in else")
          self.applyMove(move)
          neighbour=self.norm()
          # neighbour=self.currentStateArray
          nodeCounter+=1
          if popCounter!=0:
              preMove=parent.get(''.join(state))[1]
              # print(preMove)
          else:
              preMove="S"
          if self.isSolved():
            flag=1
            
            parent[''.join(neighbour)]=[''.join(state),move]
            break
          self.currentStateArray=state
          # print(neighbour)
          if neighbour not in visited:
            
            visited.append(neighbour)
            queue.append(neighbour)
            # self.parent[''.join(neighbour)]=[]
            parent[''.join(neighbour)]=[''.join(state),move,preMove]
            
      
          
      popCounter+=1
      
        
      # iterationCount=iterationCount+1
      if time.time()-startTime>=240:
        print("\n Time Limit exceeded!\n No solution reached.\n Please find the number of iterations and time conceded below:")
        # print(popCounter)
        print(nodeCounter)
        print(time.time()-startTime)
        break
    return



#Function to implement IDS
  def IDS(self,moves):
    flag=0
    depth=0
   
    visited=[]
    queue=deque()
    self.applyMovesStr(moves.split())
    Pcube=self.currentStateArray
    self.norm()
    permutedCube=self.currentStateArray
    # print(self.currentStateArray)
    visited.append(permutedCube)
    queue.append(permutedCube)
    self.currentStateArray=permutedCube
    # self.print()
    startTime=time.time()
    # for i in range(maxDepth):
    while flag==0:
      
      
      if (self.DLS(permutedCube,depth)):
        self.randomStore=[]
   
        flag=1
       
        print("Depth: ",depth," d: ",self.nodesTraversed)
        print("IDS found a solution at depth ",depth)
        path,movesToSol=self.backtrace(self.parent, ''.join(permutedCube), ''.join(self.currentStateArray))

        self.currentStateArray=Pcube
        self.randomStore.append(Pcube)
        self.applyMovesToStore(movesToSol)
        self.printRandom()
        print(self.nodesTraversed)
        print(time.time()-startTime)
        break
  
      print("Depth: ",depth," d: ",self.nodesTraversed)
      self.parent.clear()
    
      self.popCounter=0
     
      depth+=1 #Increment Depth
      
    # return False
    return  

#Function Implementing depth limited search for IDS
  def DLS(self,src,maxDepth):
    # print("DLS")
    self.currentStateArray=src
    if self.isSolved() : 
    
      return True
  
        # If reached the maximum depth, stop recursing.
    if maxDepth <= 0 : return False
  
       
    for move in MOVES.keys():
     
        self.currentStateArray=src
        child=self.applyMove(move)
       
        if self.isSolved():
          self.parent[''.join(child)]=[''.join(src),move]
        
          return True
        
        self.nodesTraversed+=1
        if(self.DLS(child,maxDepth-1)):
     
          self.popCounter+=1
          self.parent[''.join(child)]=[''.join(src),move]
          return True
    return False


  


  
    #to normalise the given state 
  def norm(self):
    # print(self.currentStateArray)
    self.currentStateArray=''.join(self.currentStateArray)
    # print(self.currentStateArray)
    cTen=self.currentStateArray[10]
    cTwelve=self.currentStateArray[12]
    cNineteen=self.currentStateArray[19]
    cTenOpp=OPP.get(cTen)
    cTwelveOpp=OPP.get(cTwelve)
    cNineteenOpp=OPP.get(cNineteen)
    normState=self.currentStateArray
    for i in range(len(self.currentStateArray)):
      if self.currentStateArray[i]==cTen:
        normState=normState[:i] + 'G' + normState[i+1:]
      elif self.currentStateArray[i]==cTwelve:
        normState=normState[:i] + 'Y' + normState[i+1:]
      elif self.currentStateArray[i]==cNineteen:
        normState=normState[:i] + 'O' + normState[i+1:]
      if self.currentStateArray[i]==cTenOpp:
        normState=normState[:i] + 'B' + normState[i+1:]
      elif self.currentStateArray[i]==cTwelveOpp:
        normState=normState[:i] + 'W' + normState[i+1:]
      elif self.currentStateArray[i]==cNineteenOpp:
        normState=normState[:i] + 'R' + normState[i+1:]
     
    self.currentStateArray=normState
    # print(self.currentStateArray)

    return normState

  

  def clone(self):
    # your code
    return

    # apply a move to a state
  def applyMove(self, move):
    posChange=MOVES.get(move)
    # print(self.currentStateArray)
    afterMove=[]
    for i in posChange:
      afterMove.append(self.currentStateArray[i])
    self.currentStateArray=afterMove
  
    self.currentState=''.join(self.currentStateArray)
      # to make ['WWWW', 'GGGG', 'OOOO', 'YYYY', 'BBBB', 'RRRR']
    self.currentState=[self.currentState[i:i+4] for i in range(0, len(self.currentState), 4)] 


    return afterMove

    # apply a string sequence of moves to a state
  def applyMovesStr(self, alg):
    for move in alg:
      self.applyMove(move)
    
    return

  def applyMovesToStore(self, alg):
    # self.randomStore=[]
    for move in alg:
      self.applyMove(move)
      self.randomStore.append(self.currentStateArray)

    
    return

    # check if state is solved
  def isSolved(self):
    startStateList= self.startState.split()
    # # print (startStateList,self.currentState,self.currentStateArray)
    self.currentState=''.join(self.currentStateArray)
         # to make ['WWWW', 'GGGG', 'OOOO', 'YYYY', 'BBBB', 'RRRR']
    self.currentState=[self.currentState[i:i+4] for i in range(0, len(self.currentState), 4)]
    # print(self.currentState) 
    
    if all(face in self.currentState for face in startStateList):
      return True
    else:
     return False
  

    # print state of the cube
  def print(self):
    template =     ("    {}{}        \n"                                    
                    "    {}{}        \n"                         
                    "{}{}  {}{} {}{} {}{}  \n"                  
                    "{}{}  {}{} {}{} {}{}  \n"         
                    "    {}{}        \n"                          
                    "    {}{}        ")  

    printCube=[]
     #change cube stickers to satisfy template format
    for i in MOVES_PRINT:
        printCube.append(self.currentStateArray[i])
      
    print("\n")
    print(template.format(*printCube))
    return

 

    # shuffle the state using 'n' random moves
  def shuffle(self, n):
    randomMoves=random.choices(list(MOVES.keys()),k=int(n))
    self.applyMovesStr(randomMoves)
    
    return randomMoves

    # print() for random() to print maximum two cubes per line
  def printRandom(self):
    template =     ("    {}{}        \n"                                    
                    "    {}{}        \n"                         
                    " {}{} {}{} {}{} {}{}  \n"                  
                    " {}{} {}{} {}{} {}{}  \n"         
                    "    {}{}        \n"                          
                    "    {}{}        ")                           
    printCube=[]
    temp=[]
    k=0
    #change cube stickers to satisfy template format
    for k in self.randomStore:
      for i in MOVES_PRINT:
        printCube.append(k[i])
      temp.append(printCube)
      printCube=[]

    
    self.randomStore=temp  
   
    movestoSol=len(self.randomStore)
    #check to print maximum of 3 cubes in a row after solution state has been determined in random()
    if movestoSol % 3==0:
      for i in range(0,movestoSol,3):
        print("\n")
        print('\n'.join(' '.join(l) for l in zip(template.format(*self.randomStore[i]).split('\n'), template.format(*self.randomStore[i+1]).split('\n'),template.format(*self.randomStore[i+2]).split('\n'))))
        
    elif movestoSol % 3==1:
      for i in range(0,movestoSol-1,3):
        print("\n")
        print('\n'.join(' '.join(l) for l in zip(template.format(*self.randomStore[i]).split('\n'), template.format(*self.randomStore[i+1]).split('\n'),template.format(*self.randomStore[i+2]).split('\n'))))
        
      print("\n")
      i=i+3
      print(template.format(*self.randomStore[i]))
    elif movestoSol % 3 ==2:
      for i in range(0,movestoSol-2,3):
        print("\n")
        print('\n'.join(' '.join(l) for l in zip(template.format(*self.randomStore[i]).split('\n'), template.format(*self.randomStore[i+1]).split('\n'),template.format(*self.randomStore[i+2]).split('\n'))))
      print("\n")  
      i=i+3
      print('\n'.join(' '.join(l) for l in zip(template.format(*self.randomStore[i]).split('\n'), template.format(*self.randomStore[i+1]).split('\n'))))
    return


    # randomly walk through a shuffled state by 'n' moves per iteration to see if solution is achieved
  def random(self,n,moves):
  
    self.randomStore.clear()
    #apply given moveset to the start state of cube
    self.applyMovesStr(moves.split())
    permutedCube=self.currentStateArray
    flag=0
    iterationCount=0
    startTime=time.time()
    self.randomStore.append(permutedCube)
      # See if cube is in Solved state before applying random movesets to solve it
    if self.isSolved():
      print("\nCube is already in Solved State after initial Moveset is applied\n") 
      return

    #infinite loop till a solution is acheived or time exceeds 60 seconds
    while flag==0 and self.isSolved() is False:
      randomMoves=random.choices(list(MOVES.keys()),k=int(n))
      movesToSolve=[]
      # Loop to apply N moves chosen at random
      for move in randomMoves:
       self.applyMove(move)
      #  -===========================###########
       self.randomStore.append(self.currentStateArray)
       movesToSolve.append(move)
       if self.isSolved():
         flag=1
         break
      
      iterationCount=iterationCount+1
      if (time.time()-startTime)>=60:
        print("\n Time Limit exceeded!\n No solution reached.\n Please find the final MoveSet and number of iterations below:")
        break
      elif flag==1 or (time.time()-startTime)>=60:
        break
      
      self.randomStore.clear()
      self.randomStore.append(permutedCube)
      self.currentStateArray=permutedCube
         
    print("\n",' '.join(movesToSolve))
    self.printRandom() 

    print("\n",iterationCount,"\n",time.time()-startTime)
    return


# receive command line arguments from shell script and call the respective functions
n=len(sys.argv)
if n==2:
  if 'print' in sys.argv:
   qube=cube()
   qube.print()
elif n==3:
  if 'print' in sys.argv:
   qube=cube(sys.argv[2])
   qube.print()
  elif 'goal' in sys.argv:
   qube=cube(sys.argv[2])
   print(qube.isSolved())
  elif 'applyMove' in sys.argv:
    qube=cube()
    qube.applyMove(sys.argv[2])
    qube.print()
  elif 'applyMoveStr' in sys.argv:
    qube=cube()
    qube.applyMovesStr(sys.argv[2].split())
    qube.print()
  elif 'norm' in sys.argv:
    qube=cube(sys.argv[2])
    qube.norm()
    qube.print()
  elif 'shuffle' in sys.argv:
    qube=cube()
    randomMoves=qube.shuffle(sys.argv[2])
    print("\n",' '.join(randomMoves))
    qube.print()
  elif 'bfs' in sys.argv:
    qube=cube()
    qube.BFS(sys.argv[2])
    # qube.print()
  elif 'ids' in sys.argv:
    qube=cube()
    qube.IDS(sys.argv[2])
  elif 'astar' in sys.argv:
    qube=cube()
    qube.Astar(sys.argv[2])

elif n==4:
  if 'applyMove' in sys.argv:
    qube=cube(sys.argv[3])
    qube.applyMove(sys.argv[2])
    qube.print()
  elif 'applyMovesStr' in sys.argv:
    qube=cube(sys.argv[3])
    qube.applyMovesStr(sys.argv[2].split())
    qube.print()
  elif 'equals' in sys.argv:
    qube=cube(sys.argv[2])
    print(qube.equals(sys.argv[3]))
  elif 'random' in sys.argv:
    qube=cube()
    qube.random(sys.argv[3],sys.argv[2])

  

