import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from anime import Anime
from pid_class import PID
import sys, os
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
import model
from classes import NFN, neuron

m1 = 5
m2 = 5
l1 = 1
l2 = 1
w1 = 1.5
w2 = 1.5
pendulum_model = model.double_pendulum(m1, m2, l1, l2, w1, w2,)

def Gen2Cart(theta1, theta2, w1, w2):
    x1 = w1 * np.sin(theta1)
    y1 = -w1 * np.cos(theta1)
    x2 = x1 + w2 * np.sin(theta2)
    y2 = y1 + -1*w2*np.cos(theta2)
    return (x1, y1, x2, y2)

# neuron1 = neuron()
# neuron2 = neuron()
# neuron3 = neuron()

# network = NFN([neuron1,neuron2,neuron3])
# print(neuron1.calc(2))
# exit()

#-------------------------------Functions------------------------------------------------#

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
        result_solve_ivp = solve_ivp(pendulum_model.dpend_dt, t_span, y0)
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

with open(f'./data.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow([f'kp = {kp}',f'ki = {ki}',f'kd = {kd}'])
    writer.writerow(['time','angle 1','velocity 1','angle 2','velocity 2','torque 1','torque 2'])
    for i in range(len(result[0])):
        writer.writerow([t[i],result[0][i],result[1][i],result[2][i],result[3][i],result[4][i],result[5][i]])

    
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(t, result[0], 'b', label='x1(t)')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, result[2], 'r', label='x3(t)')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
ax = fig.add_subplot(2, 1, 2)
ax.plot(t, result[4], 'b', label='T1(t)')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, result[5], 'r', label='T2(t)')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
plt.show()

# x1,y1,x2,y2 = Gen2Cart(result[0],result[2],w1,w2)

# anime_handler = Anime(x1=x1,x2=x2,y1=y1,y2=y2)
# anime_handler.generateAnimation()
