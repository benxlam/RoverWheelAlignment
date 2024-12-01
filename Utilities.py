import matplotlib.pyplot as ax
from matplotlib.patches import Circle
import numpy as np

def plotRoverState(ax, x,y, psi, phiL,phiR, w, r_ratio):
    # Plot the rover state
    # x,y are the position of the rover
    # theta1, theta2 are the angles of the wheels
    # w is the width of the rover
    # r_ratio is the size of the wheel circles, in fraction of w

    r = r_ratio*w

    #Plot the rover body
    dx = w/2 *np.cos(psi + np.pi/2)
    dy = w/2 *np.sin(psi + np.pi/2)
    ax.plot([x-dx, x+dx], [y-dy, y+dy], 'k-', linewidth=3)

    # Plot the rover center of mass and the body as a line
    ax.plot(x,y, 'ko')

    ax.quiver(x, y, np.cos(psi), np.sin(psi), scale=10)  # heading direction

    # Plot the wheels as a circle, denoting the angle 
    wheelPos1 = (x-dx, y-dy)
    wheelPos2 = (x+dx, y+dy)

    circle1 = Circle(wheelPos1, r, edgecolor='b', facecolor='none')
    circle2 = Circle(wheelPos2, r, edgecolor='r', facecolor='none')
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    #Show the angle markers 
    ax.plot([wheelPos1[0], wheelPos1[0]+r*np.cos(phiL)], 
             [wheelPos1[1], wheelPos1[1]+r*np.sin(phiL)], 
             'r-')
    ax.plot([wheelPos2[0], wheelPos2[0]+r*np.cos(phiR)], 
             [wheelPos2[1], wheelPos2[1]+r*np.sin(phiR)], 
             'b-')