# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:43:09 2015

@author: stephane
"""

#from every cine file and associated Sdata, generates a graphic representation of all the data, by drawing the box and the different plane of measurements

from math import pi,cos,sin
import numpy as np
import matplotlib.patches as patch
import matplotlib.axes as axes
from matplotlib.collections import PatchCollection

import matplotlib.pyplot as plt

import stephane.display.graphes as graphes
import stephane.mdata.Sdata_manip as Sdata_manip

#number of figures : one for PIV, one for Bubbles
# one with box and one without box ?

def graphic(Slist):
    """
    Represent graphically the various experimental runs by their angle of view
         each graph correspond to a experimental configuration. They are distinguable by the used stroke
         (still looking for other criterions)
    INPUT
    -----
    Slist : Sdata list
        List of Sdata (Sdata is a rich header associated to each cine file after processing)
    OUTPUT
    -----
    figs : dict
        keys corresponds to fig number, associated values to a default figure name based on x and y legends.
        Autogenerated from output of stephane.display.graphes.legende
    """
    
    #find all the different experimental configurations (now only given by the total stroke S)
    axes=[]
    figures=[]
    strokes = []
    c=0;
    
    for S in Slist:
        if not S.param.stroke in strokes:
            stroke = S.param.stroke
            strokes.append(stroke)
            c+=1
            figures.append(c)
            axes.append(frames(c,Stroke=int(stroke),box=(stroke!=100.)))
    
    print(strokes)
#    graphic_run(ax)
    for S in Slist:
        if S.fileCine.find('Polymer')>0:
            color='b'
        else:
            color='r'

        stroke=S.param.stroke
        i = strokes.index(stroke)
        draw(S,figures[i],axes[i],color=color)
    
    figs={}
    for i,fig in enumerate(figures):    
        graphes.set_fig(fig)
        figs.update(graphes.legende('Pictural representation, S = '+str(strokes[i])+' mm','',''))
        
    return figs

def frames(fignum,Stroke=300,W=260.,H=550.,box=False):
    """
    generates the frame of the experiment (grid + box)
    drawing of the box is in option
    INPUT
    -----
    fignum : int
        number of figure to draw on
    Stroke : float
        Distance in mm between the start and the stop positions of the moving grid. 
        Its value is stored in Sdata.param.Stroke
    W : float. default value 260.
        Width of the box in mm. Default value correponds to the acrylic box used in 2015
    H : float. default value 550.
        Height of the box in mm. Default value correponds to the acrylic box used in 2015
    OUTPUT
    -----
    ax : plt.axes object
        axe corresponding to the drawing.
    """
    
#    ax = axes.Axes(fig,frame)
    graphes.set_fig(fignum)
    ax = plt.gca()

    #draw the box : vertical position of the box is set manually
    zmin=-380

    if box:
        rect = patch.Rectangle((- W/2,zmin),W,H,facecolor='w',edgecolor='k',linewidth=3)
        ax.add_patch(rect) 
    
    #draw the grid
    Z_start = 0
    Z_end = Z_start - Stroke
    draw_grid(ax,0,Z_start)
    draw_grid(ax,0,Z_end,facecolor='b')
    
    ax.set_aspect('equal')

    #set the axis limits    
    e=50
    graphes.set_axes(-e-W/2,W/2+e,-e+zmin,H+zmin+e)
    graphes.refresh()
    
    return ax
    
def draw_grid(ax,x0,y0,M=50,D=10,N=5,facecolor='y',edgecolor='k',linewidth=1):
    
    positions = [(i*M+x0-D/2,y0) for i in range(-(N//2),N//2+1)]
   # grid = []
    for p in positions:
        print(p)
        square = patch.Rectangle(p,D,D,facecolor=facecolor,edgecolor=edgecolor,linewidth=linewidth)    
        ax.add_patch(square)
   #     grid.append(square)    
   # print(grid)
   # p = PatchCollection(grid,)
   # ax.add_collection(p)    
    
def draw(S,fignum,ax,color='r'):
    graphes.set_fig(fignum)
    print((S.fileCine))
    if hasattr(S.param,'im_ref'):
        angle = S.param.angle*pi/180
        fx = S.param.fx
        (Xpix,Zpix) = np.shape(S.param.im_ref)
        
        if S.param.typeview == 'sv':
            #vertical plane, the horizontal position is given py Xplane
            x0 = S.param.Xplane
            X=0
            Z = (Xpix*sin(angle)+Zpix*cos(angle))*fx
            
            zmin = -(S.param.x0*sin(angle)+S.param.y0*cos(angle))*fx
           # zmax = zmin+Z
            z0 = zmin        
        else:
            z0 = S.param.Zplane
            Z = 0
            X = max([Xpix,Zpix])*fx
            x0 = -S.param.x0*fx
        
        print([x0,z0,X,Z])
        graphic_run(ax,x0,z0,X,Z,color=color)
    #find the plane of measurement from Sdata file and     
    else:
        print('No reference image given')
    
    pass    
    
def graphic_run(ax,x0=0,z0=0,X=0,Z=200,color='r'):
    #a run is represented graphycally by a red line with two small black line at each extremity

#    style = patch.ArrowStyle.BarAB()
    arrow = patch.Arrow(x0,z0,X,Z,width=.0,color=color,linewidth=1)
    ax.add_patch(arrow)
    
    ratio=20        
    ledge = patch.Arrow(x0-Z/ratio,z0-X/ratio,2*Z/ratio,2*X/ratio,width=.0,color='k',linewidth=1)
    redge = patch.Arrow(x0+X-Z/ratio,z0+Z-X/ratio,2*Z/ratio,2*X/ratio,width=.0,color='k',linewidth=1)
    ax.add_patch(ledge)
    ax.add_patch(redge)
    
    graphes.refresh()
    
def example():
    Slist = Sdata_manip.load_all()
    graphic(Slist)
    
    graphes.save_figs(figs,savedir='./Figures/')
    
    