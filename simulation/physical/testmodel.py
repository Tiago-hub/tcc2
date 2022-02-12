from model import double_pendulum
import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt

pendulum = double_pendulum(1,1,1,1,1.1,1.1,0,0,0.0005,0.0005,0.01,0.01)
pendulum.set_initial_conditions([0,0,0,0,0,0])
# print(pendulum.dxdt())

y0 = [0, 0, 0, 0, 0, 0]  # Initial state of the system
dt = 0.01
t = np.arange(0.0, 1, dt)

result = [[], [], [], [], [], []]
for j in range(len(result)):
    result[j].append(y0[j])
tal1 = 0
tal2 = 0
counter = 0
for i in range(len(t)):
    print(i)
    if i != 0:
        t_span = (t[i-1], t[i])
        result_solve_ivp = solve_ivp(pendulum.dxdt, t_span, y0)
        last_column = result_solve_ivp.y.shape[1] - 1
        if counter>1:
            counter = 0
            #tal1 = controller_angle_1_1(input_=y0[0], dt=dt*1)# + controller_angle_1_2(input_=y0[2], dt=dt*10)
            #tal2 = controller_angle_2_1(input_=y0[2], dt=dt*1)# + controller_angle_2_2(input_=y0[0], dt=dt*10)
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