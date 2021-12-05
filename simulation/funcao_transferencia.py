import numpy as np
import matplotlib.pyplot as plt
import control
from scipy import signal
from scipy.signal import ss2tf
import matplotlib.pyplot as plt 
from matplotlib import animation 
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib.animation import PillowWriter
from anime import Anime
import slycot
#-------------------------------Functions------------------------------------------------#

def Gen2Cart(theta1,theta2,w1,w2):
    x1 = w1 * np.sin(theta1)
    y1 = -w1 * np.cos(theta1)
    x2 = x1 + w2 * np.sin(theta2)
    y2 = y1 + -1*w2*np.cos(theta2)
    return (x1,y1,x2,y2)

#------------------------------main code---------------------------------------------------#
m1 = 1
m2 = 0.1
l1 = 1.1
l2 = 1
w1 = 1.3
w2 = 1.2
g = 9.8
a,b,ga,d,e,z = [m1*l1**2+m2*w1**2,m2*w1*l2,m1*g*l1+m2*g*w1,m2*w1*l2,m2*l2**2,m2*g*l2]
a21 = -1*ga*(1/(a-((b*d)/e)))
a23 = ((b*z)/e)*(1/(a-((b*d)/e)))
a41 = ((d*ga)/a)*(1/(((-d*b)/a)+e))
a43 = -1*z*(1/(((-d*b)/a)+e))
a11,a12,a13,a14 = [0,1,0,0]
a22,a24=[0,0]
a31,a32,a33,a34=[0,0,0,1]
a42,a44=[0,0]

A = np.array([[a11,a12,a13,a14],[a21,a22,a23,a24],[a31,a32,a33,a34],[a41,a42,a43,a44]])
B = np.array([[0,],[0,],[0.2,],[0,]])
C = np.array([[1,0,0,0],[0,0,1,0]])
D = np.array([[0],[0]])

#sys = (ss2tf(A, B, C, D))

sys1 = control.ss(A,B,C,D)
sys2 = control.tf(sys1)
print(sys1)
print(sys2)