#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import pickle


this_file_loc = os.path.abspath(__file__)
this_file_path = Path(this_file_loc)
simulation_folder = this_file_path.parents[0]
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
sys.path.append(f"{simulation_folder}/data_proccessing")

from numpy import sin, cos
import numpy as np
from scipy.integrate import odeint, solve_ivp
from pid_class import PID
import matplotlib.pyplot as plt
import csv
import optparse
import collections
import model2 as model
from real_walk_train_jp import get_angles_trainned
from parser_walk_jp import walk_parser
from parser_walk_jp import walk_interpolation

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk1.csv")
(opts, args) = p.parse_args()

walk_file = f"{simulation_folder}/data/{opts.filename}"
walk_data = walk_parser(walk_file)

#constants
total_mass = 73
total_height = 1.731
m1 = 0.615*1
m2 = 0.249*1
# m1 = 0.99
# m2 = 0.9
w1 = 0.224
w2 = 0.210 - (0.210 - 2*0.09)/2
l1 = 0.112
l2 = 0.09
I_1 = 0.0240
I_2 = 0.00297
# m1 = 5
# m2 = 5
# l1 = 1
# l2 = 1
# w1 = 1.5
# w2 = 1.5
pendulum_model = model.double_pendulum(m1, m2, l1, l2, w1, w2,b1=0,b2=0)
y0 = [0, 0, 0, 0, 0, 0]  # Initial state of the system
dt = 0.1
t = list(range(101))
t = np.arange(0.0, 100, dt)
t = walk_data['time']

M1 = m1
M2 = m2
L1 = l1
L2 = l2
G = 9.8
def derivs(t, state):

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
                +b2*state[1]**2)
               / den2)

    dydx[4] = tal1
    dydx[5] = tal2
    return dydx

#hip, knee = get_angles_trainned().values()
# with open("hip", "wb") as fp:   #Pickling
#     pickle.dump(hip, fp)
# with open("knee", "wb") as fp:   #Pickling
#     pickle.dump(knee, fp)

with open("hip", "rb") as fp:   # Unpickling
    hip = pickle.load(fp)
with open("knee", "rb") as fp:   # Unpickling
    knee = pickle.load(fp)
#files
#walk_data = walk_interpolation(walk_parser(walk_file),0.1)

result = [[], [], [], [], [], []]
for j in range(len(result)):
    result[j].append(y0[j])
tal1 = hip[0]
tal2 = knee[0]
# tal1 = 0
# tal2 = 0
counter = 0
for i in range(len(t)):
    #print(i)
    if i != 0:
        t_span = (t[i-1], t[i])
        result_solve_ivp = solve_ivp(pendulum_model.dpend_dt, t_span, y0, method="BDF", dense_output=True)
        last_column = result_solve_ivp.y.shape[1] - 1
        # print(t_span)
        # print(result_solve_ivp)
        # print(result_solve_ivp.y[0, last_column])
        # print(result_solve_ivp.y[1, last_column])
        # print(result_solve_ivp.y[2, last_column])
        # print(result_solve_ivp.y[3, last_column])
        if(result_solve_ivp.success == False):
            # exit()
            pass
        if counter>1:
            counter = 0
            tal1 = hip[i]
            tal2 = knee[i]
            # tal1 = 0
            # tal2 = 0
            #tal2 = 0

        y0 = [result_solve_ivp.y[0, last_column],
              result_solve_ivp.y[1, last_column],
              result_solve_ivp.y[2, last_column],
              result_solve_ivp.y[3, last_column],
              tal1,
              tal2
              ]
        # print(y0)
        for j in range(len(result)):
            result[j].append(y0[j])
            if y0[j] != 0:
                #print (y0)
                #exit()
                pass
        counter += 1

for i in range(len(result[0])):
    result[0][i] = np.rad2deg(result[0][i])
    result[2][i] = np.rad2deg(result[2][i])
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(t, result[0], 'b', label='hip(t)')
ax.plot(t, np.rad2deg(walk_data['Hip Angle']), 'g', label='Hip reference')
ax.plot(t, result[2], 'r', label='knee(t)')
ax.plot(t, np.rad2deg(walk_data['Knee Angle']), 'y', label='Knee reference')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
ax = fig.add_subplot(2, 1, 2)
ax.plot(t, result[4], 'b', label='Angular Acceleration Hip')
ax.plot(t,hip,'g', label='fuzzy hip')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, result[5], 'r', label='Angular Acceleration knee')
ax.plot(t,knee,'y', label='fuzzy knee')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
plt.show()
