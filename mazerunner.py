from colorama import Fore
def create_maze(filename):
    file=open(filename,'r')
    lines = file.read().split('\n')
    maze=[]
    tary=-1
    for line in lines:
        tary+=1
        maz_line=[]
        for i in range(0,len(line),2):
            if line[i]=='E':
                maz_line.append('X')
                target=(i/2,tary)
            elif line[i]=='S':
                maz_line.append(' ')
                sarx=i/2
                sary=tary
            else:
                maz_line.append(line[i])
                

        maze.append(maz_line)
    y=len(maze)-1
    x=len(maze[0])-1
    return(maze,target,x,y,sarx,sary)
    

def choose_road(crossroads,pos):
    min_dist=((((target[0]-pos[0])**2)+((target[1]-pos[1])**2))**0.5)+20
    for cood in crossroads:
        dist=((((target[0]-int(cood[0])))**2)+((target[1]-int(cood[1]))**2))**0.5
       
        if dist<min_dist:
            min_dist=dist
            min_cood=cood
    crossroads.remove(min_cood)
    return(min_cood)   

class Agent:
    def __init__(self):
        self.start = (0,0)
        self.pos= (0,0)
        self.vision=[]
        self.past_cood=[]
        self.crossroads=[]

    def rewrite_vis(self,vision):
        self.vision=[]
        for y_diff in range(-1,2):
            for x_diff in range(-1,2):
                
                cood=(-1,-1)
                if self.pos[1]+y_diff>=0 and self.pos[1]+y_diff<=bounds[1] and self.pos[0]+x_diff>=0 and self.pos[0]+x_diff<=bounds[0]:
                    
                    if x_diff==0 and y_diff==-1:
                        if maze[self.pos[1]-1][self.pos[0]] in [' ','X']:
                            cood=(self.pos[0],self.pos[1]-1)
                          
                    if x_diff==-1 and y_diff==0:
                        if maze[self.pos[1]][self.pos[0]-1] in [' ','X']:
                            cood=(self.pos[0]-1,self.pos[1])
                         
                    if x_diff==1 and y_diff==0:
                        if maze[self.pos[1]][self.pos[0]+1] in [' ','X']:
                            cood=(self.pos[0]+1,self.pos[1])  
                  
                    if x_diff==0 and y_diff==1:
                        if maze[self.pos[1]+1][self.pos[0]] in [' ','X']:
                            cood=(self.pos[0],self.pos[1]+1) 

                if cood not in self.past_cood and cood!=(-1,-1):
                    self.vision.append(cood)

        return(self.vision)

filename='maze1.txt'
init=create_maze(filename)
target=(init[1])
bounds=(init[2],init[3])
maze=init[0]
Agent=Agent()
start=(init[4],init[5])
Agent.start=(int(start[0]),int(start[1]))
Agent.pos=Agent.start
stuck=False
print ('Maze: ')
for row in maze:
    for cell in row:
        print (cell,end=' ')
    print ('')
print ('')

while  Agent.pos != target and not stuck:
    Agent.vision=Agent.rewrite_vis(Agent.vision)

    if  len(Agent.vision)==0 :
        if Agent.crossroads==[]:
            print ('Error- Maze Unsolvable')
            stuck=True

        else:
            Agent.past_cood.append(Agent.pos)
            Agent.crossroads=Agent.crossroads+Agent.vision
            cood=choose_road(Agent.crossroads,Agent.pos)
            
            Agent.pos=cood
          
            
    if len(Agent.vision)==1:
        Agent.past_cood.append(Agent.pos)
        Agent.pos=Agent.vision[0]
        
    if len(Agent.vision)>1:
        Agent.past_cood.append(Agent.pos)
        Agent.crossroads=Agent.crossroads+Agent.vision
        cood=choose_road(Agent.crossroads,Agent.pos)
        Agent.pos=cood

if not stuck:
    print ('Solved Maze: ')
    for cood in Agent.past_cood:
        maze[int(cood[1])][int(cood[0])]=","

    for row in maze:
        for cell in row:
            if  cell=="," or cell=="X":
                print  (Fore.RED+cell,end=' ')
                print (Fore.RESET, end='')
            else:
                print (cell,end=' ')
        print ('')
    print('')

