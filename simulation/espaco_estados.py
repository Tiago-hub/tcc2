import numpy as np
import matplotlib.pyplot as plt
import control
from scipy import signal

m1 = 1
m2 = 0.1
l1 = 0.4
l2 = 0.3
w1 = 0.6
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
B = np.array([[0.1,],[0,],[0,],[0,]])
C = np.array([[1,0,0,0],[0,0,1,0]])
D = np.array([[0],[0]])

sys = control.ss(A,B,C,D)
T, yout1 = control.step_response(sys,T=None,X0=0,input=0,output=0)
T, yout2 = control.step_response(sys,T=None,X0=0,input=0,output=1)

plt.plot(T, yout1, 'g', label='x1(t)')
plt.plot(T, yout2, 'b', label='x3(t)')

plt.show()