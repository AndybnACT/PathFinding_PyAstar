# -*- coding: utf-8 -*-
# Copyright (c) 2017 Copyright Holder All Rights Reserved.
# Author: Tao Chiu, HandsomeAndyCT@gmail.com

import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Implement with matplotlib 2.0.2
# Main Program: A*search.py

# Debugger
# from IPython.core import debugger
# debug = debugger.Pdb().set_trace
class Graphical_LIST_MAP(object):
    """The class records data from A*search program and plot the algorithm as an animation"""
    def __init__(self, LMap, start_path, endpoint):
        super(Graphical_LIST_MAP, self).__init__()

        # Graphic
        self._last_close = start_path
        self._next_close_arrow = None
        self._background_color = {".":"8", "#":"s"}
        self._FRAME = [{"Annotate":{},"Map":{}}]
        self._frame = 0
        self._startpoint = (start_path.x, start_path.y)
        self._destpoint = endpoint
        # plotting
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(1,1,1)
        self._ax.invert_yaxis()
        self._SAVE = False
        self._max = 10
        self._min = 0

        # Initialize
        for row in range(0,len(LMap)):
            for col in range(0,len(LMap[row])):
                if (row,col) == self._startpoint or (row,col) == self._destpoint:
                    self._FRAME[0]["Map"].update({(row,col): ("b", 1850, "h", 0.6,"black")})# parameters for plotting
                else:
                    self._FRAME[0]["Map"].update({(row,col): ("b", 1500, self._background_color[LMap[row][col]], 0.6,"black")})# parameters for plotting

    def UPDATE(self,new=None,old=None,close=None):
        self._FRAME.append({"Annotate":[],"Map":{}})
        self._frame += 1
        self._FRAME[self._frame]["Annotate"] = self._FRAME[self._frame-1]["Annotate"].copy()
        self._FRAME[self._frame]["Map"] = self._FRAME[self._frame-1]["Map"].copy()


        if self._next_close_arrow != None:
            self._FRAME[self._frame]["Annotate"].pop(self._next_close_arrow)
            self._next_close_arrow = None

        if close != None:
            self._FRAME[self._frame]["Map"][(self._last_close.x, self._last_close.y)] = ("b",1500,"X",0.6,self._last_close.Total_Estimation)
            self._FRAME[self._frame]["Map"][(close.x, close.y)] = ("b",1500,"*",0.6,close.Total_Estimation)
            self._last_close = close
            return

        if new != None:
            if old != None:
                if new.Current_cost < old.Current_cost:
                    self._next_close_arrow = ((old.parent.x, old.parent.y), (new.x, new.y))
                    self._FRAME[self._frame]["Annotate"][ self._next_close_arrow ] = "red"
                    self._FRAME[self._frame]["Annotate"].update( {((new.parent.x, new.parent.y), (new.x, new.y)): "black"} )
                    self._FRAME[self._frame]["Map"][(new.x, new.y)] = ("b",1500,"o",0.6,new.Total_Estimation)
                else:
                    self._next_close_arrow = ((new.parent.x, new.parent.y), (new.x, new.y))
                    self._FRAME[self._frame]["Annotate"][ self._next_close_arrow ] = "red"
            else:
                self._FRAME[self._frame]["Annotate"].update( {((new.parent.x, new.parent.y), (new.x, new.y)): "black"} )
                self._FRAME[self._frame]["Map"][(new.x, new.y)] = ("b",1500,"o",0.6,new.Total_Estimation)

    def ColorMap(self): # find the bound of the data set
        maximum = 0
        minimum = 1e10
        for frame in self._FRAME:
            for point in frame["Map"]:
                est_value = frame["Map"][point][4]
                if type(est_value) !=str:
                    if est_value >= maximum:
                        maximum = est_value
                    if est_value <= minimum:
                        minimum = est_value
        self._max = maximum
        self._min = minimum

    # For Animation
    def plotnum(self, frame_no):
        self._ax.clear()
        for point in self._FRAME[frame_no]["Map"]:
            func_in = self._FRAME[frame_no]["Map"][point]
            if func_in[4] == "b":
                color = "b"
            else:
                color = func_in[4]
            self._ax.scatter(point[0],point[1], c=color,vmin=self._min,vmax=self._max,cmap='rainbow', s=func_in[1], marker=func_in[2], alpha=func_in[3])
        for arrow in self._FRAME[frame_no]["Annotate"]:
            func_in = self._FRAME[frame_no]["Annotate"][arrow]
            self._ax.annotate("", xytext=arrow[0], xy=arrow[1],arrowprops=dict(arrowstyle="simple",
                                                                connectionstyle="arc3,rad=-0.2",
                                                                facecolor=func_in[0]),
            )
            if self._SAVE:
                plt.savefig("./A-star-%d.png" % frame_no, dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None)
    def animation(self,save=False,interval=500):
        self._SAVE = save
        self._ani = animation.FuncAnimation(self._fig, self.plotnum, frames=range(0,self._frame+1), interval=interval, repeat=False)
        plt.show()
