import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def pend(x, t, a,b,g,d,e,z,n,th):
    x1, x2, x3, x4 = x
    dxdt = np.array([x2, (-1/(a-((b*z)/e)*np.cos(x1-x3)**2))*((b/e)*x2**2*np.sin(x1-x3)*np.cos(x1-x3)-((b*th)/e)*np.cos(x1-x3)*np.sin(x3)+g*x4**2*np.sin(x1-x3)+d*np.sin(x1)), x4, (1/(e-((b*z/a)*np.cos(x1-x3)**2)))*(((g*z)/a)*x4**2*np.cos(x1-x3)*np.sin(x1-x3)+(((d*z)/a)*np.sin(x1)*np.cos(x1-x3)+n*x2**2*np.sin(x1-x3)-th*np.sin(x3)))])
    return dxdt

m1 = 5
m2 = 5
l1 = 0.4
l2 = 0.3
w1 = 0.6
g = 9.8
a,b,g,d,e,z,n,th = [m1*l1**2+m2*w1**2,w1*l2,w1*l2,m1*l1*g+m2*w1*g,m2*l2**2,w1*l2,w1*l2,m2*l2*g]
y0 = [0.01, 0, 0, 0]
t = np.linspace(0, 20, 1001)
sol = odeint(pend, y0, t, args=(a,b,g,d,e,z,n,th))

plt.plot(t, sol[:, 0], 'b', label='x1(t)')
plt.plot(t, sol[:, 1], 'g', label='x2(t)')
plt.plot(t, sol[:, 2], 'r', label='x3(t)')
plt.plot(t, sol[:, 3], 'y', label='x4(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()
