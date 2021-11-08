import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def pend(x, t, A,B,C,D):
    x1, x2, x3, x4 = x
    #dxdt = np.array([x2, (-1/(a-((b*z)/e)*np.cos(x1-x3)**2))*((b/e)*x2**2*np.sin(x1-x3)*np.cos(x1-x3)-((b*th)/e)*np.cos(x1-x3)*np.sin(x3)+g*x4**2*np.sin(x1-x3)+d*np.sin(x1)), x4, (1/(e-((b*z/a)*np.cos(x1-x3)**2)))*(((g*z)/a)*x4**2*np.cos(x1-x3)*np.sin(x1-x3)+(((d*z)/a)*np.sin(x1)*np.cos(x1-x3)+n*x2**2*np.sin(x1-x3)-th*np.sin(x3)))])
    dxdt = np.array([x2, A*x1+B*x3, x4, C*x1+D*x3])
    return dxdt

m1 = 5
m2 = 5
l1 = 0.4
l2 = 0.3
w1 = 0.6
g = 9.8
a,b,ga,d,e,z = [m1*l1**2+m2*w1**2,m2*w1*l2,m1*g*l1+m2*g*w1,m2*w1*l2,m2*l2**2,m2*g*l2]
A = -1*ga*(1/(a-((b*d)/e)))
B = ((b*z)/e)*(1/(a-((b*d)/e)))
C = ((d*ga)/a)*(1/(((-d*b)/a)+e))
D = -1*z*(1/(((-d*b)/a)+e))
print(A,B,C,D)
y0 = [0.1, 0, -0.02, 0]
t = np.linspace(0, 20, 1001)
sol = odeint(pend, y0, t, args=(A,B,C,D))

plt.plot(t, sol[:, 0], 'b', label='x1(t)')
plt.plot(t, sol[:, 1], 'g', label='x2(t)')
plt.plot(t, sol[:, 2], 'r', label='x3(t)')
plt.plot(t, sol[:, 3], 'y', label='x4(t)')
# plt.xlim([0, 2.5])
# plt.ylim([-20, 20])
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()