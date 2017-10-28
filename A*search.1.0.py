# -*- coding: utf-8 -*-
# Copyright (c) 2017 Copyright Holder All Rights Reserved.
# Author: Tao Chiu, HandsomeAndyCT@gmail.com
# References: http://www.policyalmanac.org/games/aStarTutorial.htm
#             https://www.dropbox.com/sh/hvavm91kdpuo9rt/AAAPFDVT7JmlsPzp32rthxUka?dl=0&preview=HW1.docx
from sys import version_info
assert version_info >= (3,0) , "version error, try python 3 or higher"

# Debugger
# debug = debugger.Pdb().set_trace
# from IPython.core import debugger

# User modify area
ANIMATION = False # Turn on/off animation
SAVE_ANIMATION = False # Save pngs to current directory or not
ANIMATION_TIME_INTERVAL = 100 # mili-sec between each output
MAP_LOCATION = "./Map.txt"

if ANIMATION:
    from mplib_1_0 import Graphical_LIST_MAP # the file should be in pysearchpath
if SAVE_ANIMATION:
    if not ANIMATION:
        raise TypeError("Turn on the animation if you want to save it")
# PATH object: to record the order relationship of nodes and all of the estimated values
class PATH(object):
    def __init__(self,parent,LOC,move=0):
        self._parent = parent
        self._x = LOC[0]
        self._y = LOC[1]

        if parent != None:#non-root nodes
            if move == 0:
                raise AttributeError("must have a distance from last node")
            else:
                self._cost = move + parent.Current_cost # path length from start to n --> g(n)
        else:# root nodes
            self._cost = 0
        #! DEST is defined outside of the class
        self._est_dis = ((DEST[0]-self.x)**2 + (DEST[1]-self.y)**2)**0.5# distance from n to the goal --> h(n) (Euclidean distance)
        self._total_est_dis = self.Remaining_distance + self.Current_cost # -->f(n)

    # Location Properties
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    # Distance Properties
    # F(n) = H(n) + G(n)
    @property
    def Remaining_distance(self): #H(n)
        return self._est_dis
    @property
    def Current_cost(self): #G(n)
        return self._cost
    @property
    def Total_Estimation(self): #F(n)
        return self._total_est_dis

    # Tree Properties
    @property
    def parent(self):
        if self._parent == None:
            print("root node")
        else:
            return self._parent

    def __str__(self):
        return "node point (%d,%d) of a path with f(n)=h(n)+g(n) <=> %f=%f+%f" \
        %(self.x,self.y,self.Total_Estimation,self.Current_cost,self.Remaining_distance)

########################### FUNCTION SWITCH ##################################
def append_to_open(List_Map): # if the point hasn't been reached before
    new_open = PATH(new_point, new_open_loc, direction[direc]) # add to the path
    List_Map[new_open_loc[0]][new_open_loc[1]] = ["O", new_open]# record on the map
    OPEN.append(new_open)# append to the open list
    if ANIMATION:
        GOUT.UPDATE(new=new_open) #record data to plot

def compare_cost(List_Map):# if the point has already been appended to the opne list
    new_consider = PATH(new_point, new_open_loc, direction[direc])
    if ANIMATION:
        GOUT.UPDATE(new=new_consider,old=List_Map[new_open_loc[0]][new_open_loc[1]][1]) #record data to plot
    # check if the cost of this path to the node is lower than before
    if new_consider.Current_cost < List_Map[new_open_loc[0]][new_open_loc[1]][1].Current_cost:
        # update the node so that the path have a lower cost
        OPEN.remove(List_Map[new_open_loc[0]][new_open_loc[1]][1]) # remove the old point from the map
        OPEN.append(new_consider)# append the new one to the open list
        List_Map[new_open_loc[0]][new_open_loc[1]][1] = new_consider # record on the map
########################### FUNCTION SWITCH ##################################


#initialize
#read data from file
try:
    fd = open(MAP_LOCATION,'r') # open the file containing map informations
    Map = [[value for value in line if value != '\n'] for line in fd.readlines()] # transfer into a list
    fd.close() # close the file
except:
    print("MAP file not found or format error")
    print("Creating an example file")
    fd = open(MAP_LOCATION,'w')
    fd.write("S.....\n......\n......\n####..\n..E...")
    fd.close()
    raise
# List_Map is a map recording the status of nodes (new/closed/open/barrier)
# it will also record the pointer to the coressponding PATH object
# The program takes the adventages of 2D list to
# directly reach graph nodes from its spatial property

List_Map = list(map(list,zip(*Map))) # transpose
# find the starting and ending points
START = tuple((x, y) for x in range(len(List_Map)) for y in range(len(List_Map[x])) if List_Map[x][y] == 'S')[0] # starting point
DEST = tuple((x, y) for x in range(len(List_Map)) for y in range(len(List_Map[x])) if List_Map[x][y] == 'E')[0] # ending point
List_Map[START[0]][START[1]] = List_Map[DEST[0]][DEST[1]]= '.'



direction = {(-1,1):1.4, (-1,0):1, (0,1):1, (1,1):1.4, (1,0):1, (1,-1):1.4, (0,-1):1, (-1,-1):1.4} # cost of each direction
limit = (len(List_Map),len(List_Map[0])) #bound of the map, the map should be in the rectangle shape
OPEN = [] # open list
CLOSED = [] # close list
path_switch={ # used in the 'direction' loop, a function switch
    ".":append_to_open, # if it hasn't been reached before
    "O":compare_cost,   # if it has been appended to the opne list
}

#start computing
print("START: Finding The Shortest Path")
FOUND = False
OPEN.append(PATH(None,START)) # add the starting point to the open list
if ANIMATION:
    GOUT = Graphical_LIST_MAP(List_Map,OPEN[0],DEST)  #record data to plot
while len(OPEN) > 0:

    # find the node with the lowest cost
    new_point = min(OPEN, key= lambda x: x.Total_Estimation)

    # switch it to the CLOSED list
    OPEN.remove(new_point)
    CLOSED.append(new_point)
    List_Map[new_point.x][new_point.y] = ["X", new_point] # record to the map(X means CLOSED)
    if ANIMATION:
        GOUT.UPDATE(close=new_point)

    # stop the loop when the target was found
    if CLOSED[-1].x == DEST[0] and CLOSED[-1].y == DEST[1]:
        FOUND = True
        print("FOUND")
        break

    # search for each possible directions
    for direc in direction:
        new_open_loc = (new_point.x + direc[0],new_point.y + direc[1])

        # if it is within the boundary
        if limit[0] > new_open_loc[0] >= 0 and limit[1] > new_open_loc[1] >= 0:
            try: # function switch: determine wether the point has been reached before(in the open list)/walkable or not
                path_switch[List_Map[new_open_loc[0]][new_open_loc[1]][0]](List_Map)
            except KeyError:
                pass

#output
if not FOUND:
    print("NOT FOUND: Can not reach the destination")
print("=======================================")
output = []
road = CLOSED[-1]
while road != None and FOUND:
    print(road)
    output.append((road.x, road.y))
    road = road.parent # output the path reaching the destination
print("OUTPUT::\n================================")
output.reverse()
print(output)
if ANIMATION:
    GOUT.ColorMap() # find the max/min data to create colormap
    GOUT.animation(SAVE_ANIMATION,interval=ANIMATION_TIME_INTERVAL) # output the animation
