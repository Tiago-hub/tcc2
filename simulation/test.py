#!/usr/bin/env python3
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
import model_test3 as model
from scipy.integrate import odeint, solve_ivp
import pickle

from pathlib import Path
import optparse
this_file_loc = os.path.abspath(__file__)
this_file_path = Path(this_file_loc)
simulation_folder = this_file_path.parents[0]
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
sys.path.append(f"{simulation_folder}/data_proccessing")
from parser_walk_jp import walk_parser

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk_jp.csv")
(opts, args) = p.parse_args()

walk_file = f"{simulation_folder}/data/{opts.filename}"
walk_data = walk_parser(walk_file)


G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
L = L1 + L2  # maximal length of the combined pendulum
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg
t_stop = 81  # how many seconds to simulate
history_len = 500  # how many trajectory points to display

total_mass = 73
total_height = 1.731
m1 = 0.615*1
m2 = 0.249*1
# M1 = 0.99
# M2 = 0.9
w1 = 0.270*2
w2 = 2*0.210 - 0*(0.210 - 2*0.09)/2
L1 = w1
L2 = w2
# w1=L1
# w2=L2
# L1 = 0.112
# L2 = 0.09
L = L1 + L2  # maximal length of the combined pendulum
I_1 = 0.0240
I_2 = 0.00297
# m1 = 5
# m2 = 5
# l1 = 1
# l2 = 1
# w1 = 1.5
# w2 = 1.5
with open("hip", "rb") as fp:   # Unpickling
    hip = pickle.load(fp)
with open("knee", "rb") as fp:   # Unpickling
    knee = pickle.load(fp)

hip = hip[:-22]
knee = knee[:-22]
walk_data['Hip Angle'] = walk_data['Hip Angle'][:-22]
walk_data['Knee Angle'] = walk_data['Knee Angle'][:-22]

hip = list(map(lambda x: x * I_1, hip))
knee = list(map(lambda x: x * I_2, knee))

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

hip_dict = {}
knee_dict = {}

for index in range(len(hip)):
    # hip_dict[t[index]] = hip[index]
    knee_dict[t[index]] = knee[index]
    # knee_dict[t[index]] = 0
    hip_dict[t[index]] = 0

print(f"mass1: {m1}; mass2: {m2}")
print(f"mass center 1: {w1}; mass center 2: {w2}")
print(f"rod end 1: {w1}; mass center 2: {w2}")
pendulum_model = model.double_pendulum(m1, m2, w1, w2, w1, w2,b1=0.5,b2=0.5, tal1=hip_dict, tal2=knee_dict)


def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    b1 = b2 = 0.001

    delta = state[2] - state[0]
    tal1 = state[4]
    tal2 = state[5]
    den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0])
                +tal2
                +b2*state[3]**2
                +tal1
                +b1*state[1]**2)
               / den1)

    dydx[2] = state[3]

    den2 = (L2/L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2])
                +tal2
                +b2*state[3]**2
                +tal1
                +b1*state[1]**2)
               / den2)

    dydx[4] = tal1
    dydx[5] = tal2
    return dydx



# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = np.deg2rad(0)
w1 = 0.0
th2 = np.deg2rad(0)
w2 = 0.0
tal1 = 0
tal2 = 0

# initial state

state = [th1, w1, th2, w2]

# integrate your ODE using scipy.integrate.
print(state)

y = integrate.odeint(pendulum_model.dpend_dt, state, t)
#y = solve_ivp(derivs, t, state, method="BDF", dense_output=True)

x1 = L1*sin(y[:, 0])
y1 = -L1*cos(y[:, 0])

x2 = L2*sin(y[:, 2]) + x1
y2 = -L2*cos(y[:, 2]) + y1

fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(autoscale_on=False, xlim=(-L, L), ylim=(-L, L))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], '.-', lw=1, ms=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    if i == 0:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(thisx[2])
    history_y.appendleft(thisy[2])

    line.set_data(thisx, thisy)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))
    return line, trace, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
plt.show()


fig = plt.figure()
ax = fig.add_subplot(3, 1, 1)
ax.plot(t, np.rad2deg(y[:,0]), 'b', label='hip(t)')
ax.plot(t, np.rad2deg(walk_data['Hip Angle']), 'g', label='Hip reference')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()

ax = fig.add_subplot(3, 1, 2)
ax.plot(t, np.rad2deg(y[:,2]), 'r', label='knee(t)')
ax.plot(t, np.rad2deg(walk_data['Knee Angle']), 'y', label='Knee reference')
ax.legend(loc='best')
ax.grid()

ax = fig.add_subplot(3, 1, 3)
ax.plot(t, hip, 'b', label='Angular Acceleration Hip')
# ax.plot(t,hip,'g', label='fuzzy hip')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, knee, 'r', label='Angular Acceleration knee')
# ax.plot(t,knee,'y', label='fuzzy knee')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
plt.show()