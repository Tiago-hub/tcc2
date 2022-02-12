import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from anime import Anime
from pid_class import PID

#-------------------------------Functions------------------------------------------------#


def Gen2Cart(theta1, theta2, w1, w2):
    x1 = w1 * np.sin(theta1)
    y1 = -w1 * np.cos(theta1)
    x2 = x1 + w2 * np.sin(theta2)
    y2 = y1 + -1*w2*np.cos(theta2)
    return (x1, y1, x2, y2)


def pend(t, x, a, b, g, d, e, z, n, th):
    x1, x2, x3, x4, tal1, tal2 = x
    dxdt = np.array([   x2,
                        (-1/(a-((b*z)/e)*np.cos(x1-x3)**2))*((b/e)*x2**2*np.sin(x1-x3)*np.cos(x1-x3)-((b*th)/e)*np.cos(x1-x3)*np.sin(x3)+g*x4**2*np.sin(x1-x3)+d*np.sin(x1)) + tal1 - 0.15*0.5*x2*x2,
                        x4,
                        (1/(e-((b*z/a)*np.cos(x1-x3)**2)))*(((g*z)/a)*x4**2*np.cos(x1-x3)*np.sin(x1-x3)+(((d*z)/a)*np.sin(x1)*np.cos(x1-x3)+n*x2**2*np.sin(x1-x3)-th*np.sin(x3))) + tal2 - 0.15*0.5*x4*x4,
                        tal1,
                        tal2])
    return dxdt


m1 = 5
m2 = 5
l1 = 1
l2 = 1
w1 = 1.5
w2 = 1.5
g = 9.8
a, b, g, d, e, z, n, th = [m1*l1**2+m2*w1**2, w1*l2,
                           w1*l2, m1*l1*g+m2*w1*g, m2*l2**2, w1*l2, w1*l2, m2*l2*g]

p = (a, b, g, d, e, z, n, th)  # Parameters of the system

y0 = [0, 0, 0, 0, 0, 0]  # Initial state of the system
dt = 0.1
t = np.arange(0.0, 100, dt)

ku = 1
tu = 2.89-0.56
kp = 0.6*ku
ki = 1.2 * ku/tu
kd = 0.075*ku*tu

#kp, ki, kd = 1,0,0
print(kp,ki,kd)
controller_angle_1_1 = PID(Kp=kp, Ki=ki, Kd=kd, setpoint=1, sample_time=None, output_limits=(-10,10))
#controller_angle_1_2 = PID(Kp=1, Ki=0.0, Kd=0.0, setpoint=1, sample_time=None, output_limits=(-10,10))
controller_angle_2_1 = PID(Kp=kp, Ki=ki, Kd=kd, setpoint=0, sample_time=None, output_limits=(-10,10))
#controller_angle_2_2 = PID(Kp=1, Ki=0.0, Kd=0.0, setpoint=0, sample_time=None, output_limits=(-10,10))
result = [[], [], [], [], [], []]
for j in range(len(result)):
    result[j].append(y0[j])
tal1 = 0
tal2 = 0
counter = 0
for i in range(len(t)):
    #print(i)
    if i != 0:
        t_span = (t[i-1], t[i])
        result_solve_ivp = solve_ivp(pend, t_span, y0, args=p)
        last_column = result_solve_ivp.y.shape[1] - 1
        if counter>1:
            counter = 0
            tal1 = controller_angle_1_1(input_=y0[0], dt=dt*1)# + controller_angle_1_2(input_=y0[2], dt=dt*10)
            tal2 = controller_angle_2_1(input_=y0[2], dt=dt*1)# + controller_angle_2_2(input_=y0[0], dt=dt*10)
        y0 = [result_solve_ivp.y[0, last_column],
              result_solve_ivp.y[1, last_column],
              result_solve_ivp.y[2, last_column],
              result_solve_ivp.y[3, last_column],
              tal1,
              tal2
              ]
        for j in range(len(result)):
            result[j].append(y0[j])
        counter += 1

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(t, result[0], 'b', label='x1(t)')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, result[2], 'r', label='x3(t)')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
plt.show()

# x1,y1,x2,y2 = Gen2Cart(result[0],result[2],w1,w2)

# anime_handler = Anime(x1=x1,x2=x2,y1=y1,y2=y2)
# anime_handler.generateAnimation()
